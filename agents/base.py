from abc import ABC, abstractmethod
from engine.state import GameState
from engine.roles import Role

class BaseAgent(ABC):
    def __init__(self, player_id: int, role: Role):
        self.id = player_id
        self.role = role

    @abstractmethod
    def speak(self, game_state: GameState, discussion_history: str) -> str:
        """
        发言阶段
        return: 发言内容字符串
        """
        pass

    @abstractmethod
    def propose_team(self, game_state: GameState, team_size: int) -> list[int]:
        """
        队长提议阶段
        return: 玩家ID列表
        """
        pass

    @abstractmethod
    def vote_for_team(self, game_state: GameState, proposed_team: list[int]) -> str:
        """
        对队伍投票
        return: "approve" 或 "reject"
        """
        pass

    @abstractmethod
    def do_quest(self, game_state: GameState) -> str:
        """
        执行任务
        return: "success" 或 "fail"
        """
        pass

    @abstractmethod
    def assassinate(self, game_state: GameState) -> int:
        """
        刺杀阶段 (仅刺客)
        return: 目标玩家ID
        """
        pass