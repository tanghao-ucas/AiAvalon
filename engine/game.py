import time
from engine.state import QuestResult
from utils.logger import log_system, log_action, log_speech

class AvalonGame:
    def __init__(self, players, game_state):
        self.players = players
        self.state = game_state
        self.is_over = False

    def broadcast(self, event_type: str, data: Any):
        """
        向所有玩家广播事件。
        data 可以是字典，也可以是字符串，取决于事件类型。
        """
        # 1. 打印日志方便人类观看
        if event_type == "system_log":
            log_system(data)
        
        # 2. 传递给 Agent
        for player in self.players:
            player.listen_broadcast(event_type, data)

    def run(self):
        self.broadcast("system_log", f"游戏开始！5人局配置...")
        
        while not self.is_over:
            self.play_round()
            
            success_count = sum(1 for res in self.state.quest_results if res)
            fail_count = sum(1 for res in self.state.quest_results if not res)

            if fail_count >= 3:
                self.game_end(evil_win=True, reason="3个任务失败")
            elif success_count >= 3:
                self.enter_assassination_phase()
            
            if self.state.vote_track >= 5:
                self.game_end(evil_win=True, reason="5次投票流局")

    def play_round(self):
        leader = self.players[self.state.leader_id]
        self.broadcast("system_log", f"\n--- 第 {self.state.current_quest} 轮任务开始 ---")
        self.broadcast("game_phase", {"phase": "round_start", "round": self.state.current_quest, "leader": leader.id})

        # 1. 讨论阶段
        discussion_log = ""
        for player in self.players:
            content = player.speak(self.state, discussion_log)
            
            # === 广播发言 ===
            # 将完整的发言对象广播出去
            speech_data = {"player_id": player.id, "content": content}
            self.broadcast("public_speech", speech_data)
            
            log_speech(player.id, content)
            discussion_log += f"Player {player.id}: {content}\n"

        # 2. 提案阶段
        proposal = leader.propose_team(self.state, self.state.current_team_size)
        team = proposal.player_ids
        
        # === 广播提案 ===
        self.broadcast("team_proposal", {"leader": leader.id, "team": team})
        log_action(f"队长提名: {team}")

        # 3. 投票阶段
        votes = {}
        approve_count = 0
        for player in self.players:
            decision = player.vote(self.state, team)
            votes[player.id] = decision
            if decision == "approve": approve_count += 1
        
        passed = approve_count > len(self.players) / 2
        
        # === 广播投票结果 ===
        # 包含每个人的票型和最终结果
        vote_data = {
            "votes": votes, 
            "approved": passed, 
            "approve_count": approve_count,
            "team": team
        }
        self.broadcast("vote_result", vote_data)
        log_action(f"投票结果: {votes} ({'通过' if passed else '不通过'})")
        
        if passed:
            self.state.vote_track = 0
            self.run_mission(team, leader.id, votes)
        else:
            self.state.vote_track += 1
            self.state.leader_id = (self.state.leader_id + 1) % len(self.players)
            # 记录流局
            self.state.history_log.append(QuestResult(
                round=self.state.current_quest, team=team, leader=leader.id,
                votes=votes, succeeded=False, fail_count=-1
            ))

    def run_mission(self, team_ids, leader_id, votes):
        fails = 0
        for pid in team_ids:
            player = self.players[pid]
            action = player.do_quest(self.state)
            if action.outcome == 'fail': fails += 1
        
        is_success = (fails == 0)
        self.state.quest_results.append(is_success)
        
        # === 广播任务结果 ===
        quest_data = {"round": self.state.current_quest, "success": is_success, "fail_count": fails, "team": team_ids}
        self.broadcast("quest_result", quest_data)
        
        log_system(f"任务结果: {'成功' if is_success else '失败'} (失败票: {fails})")
        
        self.state.history_log.append(QuestResult(
            round=self.state.current_quest, team=team_ids, leader=leader_id,
            votes=votes, succeeded=is_success, fail_count=fails
        ))

        self.state.current_quest += 1
        self.state.leader_id = (self.state.leader_id + 1) % len(self.players)

    def enter_assassination_phase(self):
        self.broadcast("game_phase", "assassination")
        # ... (刺杀逻辑同前，略)

    def game_end(self, evil_win, reason):
        self.is_over = True
        self.broadcast("game_end", {"evil_win": evil_win, "reason": reason})