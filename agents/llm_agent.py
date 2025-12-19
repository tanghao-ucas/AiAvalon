import openai
from typing import List, Any, Optional
from .base import BaseAgent
from .schemas import SpeechAction, VoteTeamAction, ProposeTeamAction, QuestAction, AssassinateAction
from config.prompts import SYSTEM_PROMPT
from .components.base import BaseComponent

class LLMAgent(BaseAgent):
    def __init__(
        self, 
        player_id: int, 
        role: Any, 
        model_name: str,          # 实际传给 API 的模型名 (如 gpt-4-1106-preview)
        api_key: str,             # 该 Agent 专用的 API Key
        base_url: Optional[str] = None, # 可选的 Base URL
        components: List[BaseComponent] = None
    ):
        super().__init__(player_id, role)
        
        self.model_name = model_name
        self.name = f"Player {player_id}"
        
        # === 核心修改：使用传入的配置初始化 Client ===
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url # 如果为 None，OpenAI 库会使用默认地址
        )
        
        self.components = components or []
        for component in self.components:
            component.bind(self)

    # ... (listen_broadcast 方法保持不变) ...
    def listen_broadcast(self, event_type: str, data: Any):
        for component in self.components:
            if component.should_trigger(event_type):
                component.on_event(event_type, data)

    # ... (_build_system_prompt 方法保持不变) ...
    def _build_system_prompt(self, game_state):
        role_info = getattr(self.role, 'vision_text', "")
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

    def _call_llm(self, game_state, user_prompt, response_model, action_type="generic"):
        system_prompt = self._build_system_prompt(game_state)
        
        context_injections = []
        for component in self.components:
            injection = component.get_prompt_injection(game_state, action_type)
            if injection:
                context_injections.append(f"--- [{component.name}] ---\n{injection}")
        
        if context_injections:
            user_prompt = "\n".join(context_injections) + f"\n\n=== 你的任务 ===\n{user_prompt}"

        # 使用 self.model_name 而不是全局 config
        completion = self.client.beta.chat.completions.parse(
            model=self.model_name, 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format=response_model,
        )
        response = completion.choices[0].message.parsed
        
        self.listen_broadcast("internal_thought", response.thinking)
        return response

    # ... (其余行为方法 speak, vote 等保持不变) ...
    def speak(self, game_state, discussion_log):
        prompt = f"现在是讨论阶段。\n本轮已有的发言:\n{discussion_log}\n请简短发言。"
        resp = self._call_llm(game_state, prompt, SpeechAction, action_type="speak")
        return resp.content
    
    def propose_team(self, game_state, team_size):
        prompt = f"请提名 {team_size} 名玩家。"
        resp = self._call_llm(game_state, prompt, ProposeTeamAction, action_type="propose")
        return resp

    def vote(self, game_state, proposed_team):
        prompt = f"提名队伍: {proposed_team}。请投票。"
        resp = self._call_llm(game_state, prompt, VoteTeamAction, action_type="vote")
        return resp.decision

    def do_quest(self, game_state):
        prompt = "任务执行阶段。Good必须success。"
        resp = self._call_llm(game_state, prompt, QuestAction, action_type="quest")
        if self.role.alignment == "Good": resp.outcome = "success"
        return resp

    def assassinate(self, game_state):
        prompt = "刺杀阶段。找出梅林。"
        resp = self._call_llm(game_state, prompt, AssassinateAction, action_type="assassinate")
        return resp.target_id