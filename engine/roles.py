from abc import ABC, abstractmethod

class Role(ABC):
    def __init__(self, is_evil: bool, name: str):
        self.is_evil = is_evil
        self.name = name
        self.alignment = "Evil" if is_evil else "Good"
        # 视野文本现在由外部计算后注入，或者在这里保留逻辑
        self.vision_text = "" 

    @abstractmethod
    def get_vision_prompt(self, my_id: int, all_players_roles: dict) -> str:
        pass

# --- 角色类定义 (保持不变) ---
class Servant(Role):
    def __init__(self): super().__init__(False, "Loyal Servant")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        return "你没有任何特殊信息。你只知道自己是好人。"

class Minion(Role):
    def __init__(self): super().__init__(True, "Minion of Mordred")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        teammates = [pid for pid, role in all_roles.items() if role.is_evil and pid != my_id]
        return f"你的坏人队友是: {teammates}。"

class Merlin(Role):
    def __init__(self): super().__init__(False, "Merlin")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        evils = []
        for pid, role in all_roles.items():
            if pid == my_id: continue
            if role.is_evil and role.name != "Mordred":
                evils.append(pid)
        return f"作为梅林，你感应到邪恶力量来自: {evils} (注意：如果莫德雷德在场，你看不到他)。"

class Percival(Role):
    def __init__(self): super().__init__(False, "Percival")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        targets = []
        for pid, role in all_roles.items():
            if role.name in ["Merlin", "Morgana"]:
                targets.append(pid)
        return f"你看到了两个神秘的身影: {targets}。其中一个是梅林，一个是莫甘娜，你需要分辨谁是真预言家。"

class Assassin(Role):
    def __init__(self): super().__init__(True, "Assassin")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        teammates = [pid for pid, role in all_roles.items() if role.is_evil and pid != my_id]
        return f"你是刺客。你的队友是: {teammates}。任务阶段无论胜负，如果好人即将胜利，你可以尝试刺杀梅林来反败为胜。"

class Morgana(Role):
    def __init__(self): super().__init__(True, "Morgana")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        teammates = [pid for pid, role in all_roles.items() if role.is_evil and pid != my_id]
        return f"你是莫甘娜。你的队友是: {teammates}。你要假装自己是梅林来迷惑派西维尔。"

class Mordred(Role):
    def __init__(self): super().__init__(True, "Mordred")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        teammates = [pid for pid, role in all_roles.items() if role.is_evil and pid != my_id]
        return f"你是莫德雷德。梅林看不到你的身份。你的队友是: {teammates}。"

# --- 工厂方法 ---
def get_role_by_name(name: str) -> Role:
    name_map = {
        "Loyal Servant": Servant,
        "Minion": Minion,
        "Merlin": Merlin,
        "Percival": Percival,
        "Assassin": Assassin,
        "Morgana": Morgana,
        "Mordred": Mordred
    }
    cls = name_map.get(name)
    if not cls:
        raise ValueError(f"Unknown role name: {name}")
    return cls()