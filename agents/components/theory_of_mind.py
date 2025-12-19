from .base import BaseComponent

class TheoryOfMindComponent(BaseComponent):
    def __init__(self):
        super().__init__("Theory of Mind (Player Analysis)")
        # 存储对每个玩家的简单评价
        self.player_profiles = {} # {pid: "怀疑是坏人，因为..."}

    def on_bind(self):
        # 初始化所有玩家
        # 注意：这里可能需要拿到总人数，暂时假设逻辑在运行时动态处理
        pass

    def get_prompt_injection(self, game_state, action_type) -> str:
        if not self.player_profiles:
            return "目前你对其他玩家还没有明确的判断。"
        
        summary = "你对其他玩家的私人分析笔记:\n"
        for pid, analysis in self.player_profiles.items():
            summary += f"Player {pid}: {analysis}\n"
        
        summary += "\n(请根据最新局势更新这些判断)"
        return summary

    def on_event(self, event_type, data):
        # 这里可以扩展更复杂的逻辑，比如每次投票结束后，让 LLM 专门跑一次分析
        # 简化版：我们假设 thinking 中包含了分析，这里暂时只做被动存储
        # 真正的高级用法是：在后台触发一个独立的 LLM call 来更新 profiles
        pass
        
    # 可扩展：增加一个 update_profile 方法，允许主 Agent 显式更新对某人的看法
    def update_profile(self, target_pid, analysis):
        self.player_profiles[target_pid] = analysis