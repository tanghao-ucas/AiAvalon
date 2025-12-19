import openai
from .base import BaseAgent
from .schemas import SpeechAction, VoteTeamAction, ProposeTeamAction, QuestAction
from config.prompts import SYSTEM_PROMPT, ROLE_PROMPTS

class LLMAgent(BaseAgent):
    def __init__(self, player_id, role, config):
        self.id = player_id
        self.role = role
        self.memory = []  # 存储对话历史
        self.thinking_history = [] # 存储内心独白 (类似狼人杀代码中的 thinkingHistory)
        self.client = openai.OpenAI(api_key=config.api_key)

    def _build_system_prompt(self, game_state):
        # 构建动态的 System Prompt
        role_info = ROLE_PROMPTS.get(self.role.name, "").format(
            teammates=self.role.get_visible_teammates(),
            minions=self.role.get_known_evils(),
            merlins=self.role.get_merlin_candidates()
        )
        
        return SYSTEM_PROMPT.format(
            player_id=self.id,
            role_name=self.role.name,
            alignment=self.role.alignment,
            role_specific_info=role_info,
            num_players=game_state.num_players,
            quest_round=game_state.current_quest,
            team_size=game_state.current_team_size,
            vote_track=game_state.vote_track,
            quest_history=game_state.history_str,
            last_vote_result=game_state.last_vote_str
        )

    def speak(self, game_state, discussion_log):
        # 类似 PlayerServer.speak
        prompt = f"现在是讨论阶段。\n之前的发言:\n{discussion_log}\n请简短发言，分析局势或伪装自己。"
        response = self._call_llm(game_state, prompt, response_model=SpeechAction)
        self.thinking_history.append(response.thinking)
        return response.content

    def vote(self, game_state, proposed_team):
        # 类似 PlayerServer.vote
        prompt = f"队长 Player {game_state.leader_id} 提名的队伍是: {proposed_team}。\n请决定同意(approve)还是反对(reject)。"
        response = self._call_llm(game_state, prompt, response_model=VoteTeamAction)
        self.thinking_history.append(response.thinking)
        return response.decision

    def _call_llm(self, game_state, user_prompt, response_model):
        system_prompt = self._build_system_prompt(game_state)
        
        # 注入之前的内心独白，保持人设一致性 (Critical for consistency)
        if self.thinking_history:
            thought_context = "\n".join([f"Round {i} Thought: {t}" for i, t in enumerate(self.thinking_history[-5:])])
            user_prompt += f"\n\n回顾你之前的思考:\n{thought_context}"

        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o",  # 或者其他支持 Structured Outputs 的模型
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=response_model,
        )
        return completion.choices[0].message.parsed