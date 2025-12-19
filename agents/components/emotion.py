from .base import BaseComponent

class EmotionComponent(BaseComponent):
    def __init__(self, initial_mood="Calm"):
        super().__init__("Emotion System")
        self.mood = initial_mood
        self.mood_history = []

    def get_prompt_injection(self, game_state, action_type) -> str:
        """注入当前情绪，影响 LLM 的语气"""
        return f"""当前心情: 【{self.mood}】
请在你的发言或思考中体现这种情绪。不要直接说“我很{self.mood}”，而是通过语气词、标点符号或措辞来表现。
"""

    def on_event(self, event_type, data):
        """根据游戏事件改变情绪"""
        # 简单的情绪状态机示例
        if event_type == "vote_result":
            # data: {'approved': bool, 'votes': {...}}
            if not data['approved']:
                self.mood = "Frustrated" # 投票不通过，感到挫败
            else:
                self.mood = "Hopeful" # 队伍出发，充满希望
        
        elif event_type == "quest_result":
            # data: {'success': bool, 'fails': int}
            is_good = (self.agent.role.alignment == "Good")
            quest_success = data['success']
            
            if is_good:
                if quest_success:
                    self.mood = "Excited"
                else:
                    self.mood = "Angry" # 任务失败，好人愤怒
            else:
                if quest_success:
                    self.mood = "Nervous" # 任务成功，坏人紧张
                else:
                    self.mood = "Smug" # 任务失败，坏人得意
                    
        self.mood_history.append(self.mood)