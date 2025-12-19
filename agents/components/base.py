from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, List

if TYPE_CHECKING:
    from agents.llm_agent import LLMAgent
    from engine.state import GameState

class BaseComponent(ABC):
    def __init__(self, name: str, triggers: List[str] = None):
        self.name = name
        # 如果为 None 或包含 "all"，则视为监听所有事件
        self.triggers = triggers if triggers else ["all"]
        self.agent: 'LLMAgent' = None

    def bind(self, agent: 'LLMAgent'):
        self.agent = agent
        self.on_bind()

    def on_bind(self):
        pass

    @abstractmethod
    def get_prompt_injection(self, game_state: 'GameState', action_type: str) -> str:
        return ""

    def should_trigger(self, event_type: str) -> bool:
        """判断当前事件是否需要触发此组件"""
        if "all" in self.triggers:
            return True
        return event_type in self.triggers

    def on_event(self, event_type: str, data: Any):
        """
        处理广播事件
        event_type: 事件类型 (e.g., 'public_speech', 'vote_result')
        data: 原始数据字典或字符串
        """
        pass