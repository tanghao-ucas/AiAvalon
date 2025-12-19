from pydantic import BaseModel
from typing import List, Optional, Dict

class QuestResult(BaseModel):
    round: int
    team: List[int]
    leader: int
    votes: Dict[int, str] # player_id -> "approve"/"reject"
    succeeded: bool
    fail_count: int

class GameState(BaseModel):
    """
    当前游戏的全局快照（所有Agent可见的公共信息）
    """
    num_players: int
    current_quest: int = 1         # 当前是第几个任务 (1-5)
    vote_track: int = 0            # 当前连续投票失败次数 (0-5)
    leader_id: int                 # 当前队长ID
    
    quest_results: List[bool] = [] # 已完成任务的结果 [True, False, ...]
    history_log: List[QuestResult] = [] # 详细的历史记录
    
    # 阿瓦隆标准人数配置表 (玩家数 -> 每轮任务所需人数)
    # Key: total players, Value: [q1, q2, q3, q4, q5]
    BOARD_CONFIG: Dict[int, List[int]] = {
        5: [2, 3, 2, 3, 3],
        6: [2, 3, 4, 3, 4],
        7: [2, 3, 3, 4, 4], # 注：第4个任务通常需2fail，此处简化
        8: [3, 4, 4, 5, 5],
        9: [3, 4, 4, 5, 5],
        10: [3, 4, 4, 5, 5]
    }

    @property
    def current_team_size(self) -> int:
        """获取当前任务需要的人数"""
        if self.num_players not in self.BOARD_CONFIG:
            return 3 # 默认fallback
        return self.BOARD_CONFIG[self.num_players][self.current_quest - 1]

    @property
    def history_str(self) -> str:
        """格式化历史记录供Prompt使用"""
        if not self.history_log:
            return "暂无历史记录"
        
        summary = ""
        for h in self.history_log:
            res = "成功" if h.succeeded else "失败"
            summary += f"R{h.round} (队长P{h.leader}): 任务{res}, 队伍{h.team}, 投票详情{h.votes}\n"
        return summary

    @property
    def last_vote_str(self) -> str:
        if not self.history_log:
            return "无"
        last = self.history_log[-1]
        return str(last.votes)