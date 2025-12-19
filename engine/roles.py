from abc import ABC, abstractmethod
from typing import List, Type

class Role(ABC):
    def __init__(self, is_evil: bool, name: str):
        self.is_evil = is_evil
        self.name = name
        self.alignment = "Evil" if is_evil else "Good"

    @abstractmethod
    def get_vision_prompt(self, my_id: int, all_players_roles: dict[int, 'Role']) -> str:
        """
        生成该角色看到的特殊信息 Prompt
        all_players_roles: {player_id: Role_Instance}
        """
        pass

# --- 基础角色 ---

class Servant(Role):
    def __init__(self): super().__init__(False, "Loyal Servant")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        return "你没有任何特殊信息。你只知道自己是好人。"

class Minion(Role):
    def __init__(self): super().__init__(True, "Minion of Mordred")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        # 普通坏人看到所有其他坏人（除了奥伯伦，这里暂简化为看到所有坏人）
        teammates = [pid for pid, role in all_roles.items() if role.is_evil and pid != my_id]
        return f"你的坏人队友是: {teammates}。"

# --- 特殊角色 ---

class Merlin(Role):
    def __init__(self): super().__init__(False, "Merlin")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        # 梅林看到坏人，但看不到莫德雷德
        evils = []
        for pid, role in all_roles.items():
            if pid == my_id: continue
            if role.is_evil and role.name != "Mordred":
                evils.append(pid)
        return f"作为梅林，你感应到邪恶力量来自: {evils} (注意：如果莫德雷德在场，你看不到他)。"

class Percival(Role):
    def __init__(self): super().__init__(False, "Percival")
    def get_vision_prompt(self, my_id, all_roles) -> str:
        # 派西维尔看到梅林和莫甘娜
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

# 角色分配辅助函数
import random
def assign_roles(num_players: int) -> dict[int, Role]:
    # 简化的配置策略
    if num_players == 5:
        # 3好人 (梅林, 派, 忠臣) vs 2坏人 (莫甘娜/刺客, 莫德雷德/爪牙)
        # 简化版：梅林, 派, 忠臣 vs 刺客, 莫甘娜
        pool = [Merlin(), Percival(), Servant(), Assassin(), Morgana()]
    elif num_players == 6:
        pool = [Merlin(), Percival(), Servant(), Servant(), Assassin(), Morgana()]
    else:
        # 默认填充
        pool = [Merlin(), Assassin()] + [Servant()] * (num_players - 2)
        # 确保坏人比例 (约1/3)
        num_evil = (num_players + 2) // 3
        # ... 这里可以写更复杂的配置逻辑
    
    random.shuffle(pool)
    return {i: role for i, role in enumerate(pool[:num_players])}