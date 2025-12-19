from abc import ABC, abstractmethod
from typing import Any, Dict, List
from engine.state import GameState

class AgentContext:
    """用于在组件间传递数据的上下文对象"""
    def __init__(self, game_state: GameState, role_info: str, raw_prompt: str):
        self.game_state = game_state
        self.role_info = role_info
        self.system_prompts: List[str] = [] # 组件注入的系统级指令
        self.context_data: List[str] = []   # 组件注入的上下文信息(如RAG内容)
        self.raw_prompt = raw_prompt        # 当前动作的基础提示词

class AgentComponent(ABC):
    @abstractmethod
    def name(self) -> str:
        pass

    def on_register(self, agent):
        """当组件被安装到 Agent 时调用"""
        self.agent = agent

    def on_turn_start(self, context: AgentContext):
        """回合开始/构建 Prompt 阶段：可以在这里注入 Prompt"""
        pass

    def on_action_end(self, action_type: str, action_content: Any, result: Any):
        """动作结束后：用于更新记忆或学习"""
        pass