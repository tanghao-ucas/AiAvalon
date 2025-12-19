from pydantic import BaseModel, Field
from typing import Literal, Optional

# 通用思考模式
class CognitiveResponse(BaseModel):
    thinking: str = Field(..., description="你的内心独白和逻辑推理过程，只有你自己知道。")

# 1. 发言阶段输出
class SpeechAction(CognitiveResponse):
    content: str = Field(..., description="公开说的话，不要暴露只有你知道的秘密信息，除非是有意为之。")

# 2. 提案阶段输出 (队长)
class ProposeTeamAction(CognitiveResponse):
    player_ids: list[int] = Field(..., description="你提名的玩家ID列表。")

# 3. 投票阶段输出 (全体)
class VoteTeamAction(CognitiveResponse):
    decision: Literal["approve", "reject"] = Field(..., description="批准或拒绝当前队伍。")

# 4. 任务执行输出 (队伍成员)
class QuestAction(CognitiveResponse):
    outcome: Literal["success", "fail"] = Field(..., description="任务结果。好人只能投success。")

# 5. 刺杀阶段 (刺客)
class AssassinateAction(CognitiveResponse):
    target_id: int = Field(..., description="你认为是梅林的玩家ID。")