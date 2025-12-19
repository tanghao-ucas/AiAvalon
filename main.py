import os
import yaml
import random
from engine.game import AvalonGame
from engine.state import GameState
from engine.roles import get_role_by_name
from agents.llm_agent import LLMAgent
from agents.components import create_component
from utils.logger import log_system

def load_yaml(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Config file not found: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    log_system("=== AI Avalon 启动 (Multi-Key Support) ===")
    
    # 1. 加载配置
    try:
        players_config = load_yaml("config/players.yaml")
        models_registry = load_yaml("config/models.yaml")
    except Exception as e:
        log_system(f"配置加载失败: {e}")
        return

    player_list_conf = players_config.get("players", [])
    num_players = len(player_list_conf)
    
    # 2. 预先实例化角色
    role_map = {}
    for p_conf in player_list_conf:
        role_map[p_conf['id']] = get_role_by_name(p_conf['role'])
    
    # 3. 初始化 Agents
    players = []
    all_roles_dict = role_map.copy() # 用于计算视野
    
    log_system(f"正在初始化 {num_players} 个 AI 玩家...")
    
    for p_conf in player_list_conf:
        pid = p_conf['id']
        name = p_conf.get('name', f"Player {pid}")
        role = role_map[pid]
        
        # A. 计算视野
        role.vision_text = role.get_vision_prompt(pid, all_roles_dict)
        
        # B. 获取模型配置
        model_key = p_conf.get('model')
        if model_key not in models_registry:
            raise ValueError(f"玩家 {name} 指定的模型 '{model_key}' 未在 config/models.yaml 中定义！")
        
        model_conf = models_registry[model_key]
        
        # 从注册表中提取具体的连接信息
        real_model_name = model_conf.get('model_name', model_key)
        api_key = model_conf.get('api_key')
        base_url = model_conf.get('base_url') # 可能为 None

        # 简单的环境变量回退 (如果yaml里填的是 $ENV_VAR)
        if api_key and api_key.startswith("$"):
            env_var = api_key[1:]
            api_key = os.getenv(env_var)
            if not api_key:
                raise ValueError(f"环境变量 {env_var} 未设置")

        # C. 组装组件
        components = []
        for c_conf in p_conf.get('components', []):
            try:
                comp = create_component(
                    c_conf.get('type'), 
                    c_conf.get('params', {}), 
                    c_conf.get('triggers', ["all"])
                )
                components.append(comp)
            except Exception as e:
                print(f"[Warning] 组件加载失败 {name}: {e}")

        # D. 实例化 Agent (传入专属 API 配置)
        agent = LLMAgent(
            player_id=pid,
            role=role,
            model_name=real_model_name,
            api_key=api_key,
            base_url=base_url,
            components=components
        )
        agent.name = name
        players.append(agent)
        print(f"[{name}] Init Success | Model: {model_key} -> {real_model_name}")

    log_system("初始化完毕，游戏开始！")

    # 4. 启动游戏
    game_state = GameState(
        num_players=num_players,
        leader_id=random.randint(0, num_players-1)
    )
    game_engine = AvalonGame(players, game_state)
    game_engine.run()

if __name__ == "__main__":
    main()