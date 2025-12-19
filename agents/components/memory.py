from .base import BaseComponent

class MemoryComponent(BaseComponent):
    def __init__(self, max_items=5):
        super().__init__("Memory & Reflection")
        self.thinking_history = []
        self.max_items = max_items

    def get_prompt_injection(self, game_state, action_type) -> str:
        if not self.thinking_history:
            return ""
        
        # 获取最近的几次思考，保持连贯性
        recent = self.thinking_history[-self.max_items:]
        history_str = "\n".join([f"- {t}" for t in recent])
        return f"你之前的思考逻辑 (请保持连贯):\n{history_str}"

    def on_event(self, event_type, data):
        if event_type == "thinking_generated":
            self.thinking_history.append(data)