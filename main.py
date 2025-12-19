import os
import random
import time
from engine.game import AvalonGame
from engine.state import GameState
from engine.roles import assign_roles
from agents.llm_agent import LLMAgent
from config.settings import settings
from utils.logger import log_system

def load_rules():
    rule_path = os.path.join(os.path.dirname(__file__), 'data', 'rules.txt')
    try:
        with open(rule_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "规则文件未找到。"

def main():
    log_system("=== AI Avalon 启动 ===")
    
    # 1. 游戏配置
    NUM_PLAYERS = 5
    
    # 2. 初始化游戏引擎
    game_state = GameState(
        num_players=NUM_PLAYERS,
        leader_id=random.randint(0, NUM_PLAYERS-1)
    )
    
    # 3. 分配角色
    role_map = assign_roles(NUM_PLAYERS)
    
    # 4. 初始化 Agents
    players = []
    log_system(f"正在初始化 {NUM_PLAYERS} 个 AI 玩家...")
    for pid in range(NUM_PLAYERS):
        role = role_map[pid]
        # 这里实例化 LLMAgent (来自你之前生成的代码或 llm_agent.py)
        # 确保传入 settings 以获取 API key
        agent = LLMAgent(pid, role, settings) 
        players.append(agent)
        print(f"Player {pid}: {role.name} ({role.alignment})") # Debug用，实际玩的时候隐藏

    log_system("角色分配完毕，游戏开始！")
    time.sleep(1)

    # 5. 启动游戏主循环
    # 假设 engine/game.py 中有一个 AvalonGame 类来控制流程
    # 这里我们简单模拟一下如何调用 engine (或者直接在这里写主循环如果 game.py 没写完)
    
    game_engine = AvalonGame(players, game_state)
    game_engine.run()

if __name__ == "__main__":
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("错误: 未设置 OPENAI_API_KEY 环境变量。")
    else:
        main()