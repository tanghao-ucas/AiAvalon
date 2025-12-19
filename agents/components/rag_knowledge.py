from .base import BaseComponent

class RAGComponent(BaseComponent):
    def __init__(self, knowledge_base_path="data/strategy_db.txt"):
        super().__init__("Strategic Knowledge (RAG)")
        self.kb_path = knowledge_base_path
        self.loaded_strategies = []
        # 模拟加载数据
        self._load_mock_data()

    def _load_mock_data(self):
        # 实际项目中这里应该是 Vector DB 的检索逻辑
        self.loaded_strategies = [
            "如果我是梅林：第一轮尽量投赞成，不要表现得太全知全能。",
            "如果我是刺客：重点观察那些投票行为异常坚定的人。",
            "5人局逻辑：只要出现一个红票（reject），该队伍通常就有坏人。"
        ]

    def get_prompt_injection(self, game_state, action_type) -> str:
        # 根据当前角色过滤相关策略
        my_role = self.agent.role.name
        
        relevant_tips = []
        for tip in self.loaded_strategies:
            if my_role in tip or "5人局" in tip:
                relevant_tips.append(tip)
        
        if not relevant_tips:
            return ""

        return "参考历史高玩策略:\n" + "\n".join([f"* {tip}" for tip in relevant_tips])