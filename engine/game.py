import random
from engine.roles import AssignRoles
from agents.llm_agent import LLMAgent

class AvalonGame:
    def __init__(self, config):
        self.players = []
        self.config = config
        self.round = 1
        self.vote_track = 0
        self.quest_results = [] # [True, False, ...]
        self.logs = []
    
    def setup(self, num_players=5):
        # 1. 分配角色
        roles = AssignRoles(num_players)
        # 2. 初始化 Agent
        for pid in range(num_players):
            agent = LLMAgent(pid, roles[pid], self.config)
            self.players.append(agent)
        self.leader_idx = random.randint(0, num_players - 1)

    def play(self):
        while not self.is_game_over():
            self.play_round()
    
    def play_round(self):
        leader = self.players[self.leader_idx]
        print(f"\n--- 第 {self.round} 轮任务开始，队长: Player {leader.id} ---")

        # 1. 讨论阶段 (简化版：每人发言一轮)
        discussion_log = ""
        for player in self.players:
            speech = player.speak(self.get_state(), discussion_log)
            log = f"Player {player.id}: {speech}"
            discussion_log += log + "\n"
            print(log)

        # 2. 提案阶段
        team_size = self.get_quest_team_size()
        proposal = leader.propose_team(self.get_state(), team_size) # 需在Agent实现
        print(f"队长提名: {proposal.player_ids}")

        # 3. 投票阶段
        votes = {}
        for player in self.players:
            vote = player.vote(self.get_state(), proposal.player_ids)
            votes[player.id] = vote
        
        print(f"投票结果: {votes}")
        
        if self.check_vote_pass(votes):
            self.vote_track = 0
            # 4. 任务阶段
            self.run_mission(proposal.player_ids)
        else:
            self.vote_track += 1
            self.leader_idx = (self.leader_idx + 1) % len(self.players)
            print("投票未通过，轮换队长。")
            if self.vote_track >= 5:
                print("连续5次流局，坏人胜利！")
                self.game_over = True

    def run_mission(self, team_ids):
        fails = 0
        for pid in team_ids:
            player = self.players[pid]
            # 只有坏人可以选择 Fail，好人强制 Success (在 Prompt 或 Agent 逻辑中限制)
            action = player.do_quest(self.get_state()) 
            if action.outcome == 'fail':
                fails += 1
        
        success = fails == 0 # (注：7人以上第4轮需要2个fail，需特殊处理)
        self.quest_results.append(success)
        print(f"任务结果: {'成功' if success else '失败'} (失败票数: {fails})")
        self.round += 1
        self.leader_idx = (self.leader_idx + 1) % len(self.players)

    # ... check_win_condition 等辅助函数