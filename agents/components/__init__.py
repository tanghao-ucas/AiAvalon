from .base import BaseComponent
from .memory import MemoryComponent
from .theory_of_mind import TheoryOfMindComponent
from .rag_knowledge import RAGComponent
from .emotion import EmotionComponent

# 组件映射表
COMPONENT_MAP = {
    "memory": MemoryComponent,
    "theory_of_mind": TheoryOfMindComponent,
    "rag": RAGComponent,
    "emotion": EmotionComponent
}

def create_component(name: str, params: dict = None, triggers: list = None) -> BaseComponent:
    if params is None: params = {}
    cls = COMPONENT_MAP.get(name)
    if not cls: raise ValueError(f"Unknown component: {name}")
    
    # 将 triggers 注入组件实例
    # 注意：所有组件的 __init__ 必须接受 triggers 参数，或者我们在实例化后赋值
    # 最稳妥是修改 BaseComponent.__init__ (上面已做)，并在具体的子类 super().__init__ 传递
    instance = cls(**params, triggers=triggers) 
    return instance