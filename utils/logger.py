import logging
import sys

# 定义颜色代码
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def setup_logger(name="Avalon"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # 避免重复添加handler
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(message)s') # 简化输出，只看内容
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

logger = setup_logger()

def log_speech(player_id, content):
    logger.info(f"{Colors.CYAN}[Player {player_id} 发言]{Colors.ENDC}: {content}")

def log_system(content):
    logger.info(f"{Colors.WARNING}[系统]{Colors.ENDC} {content}")

def log_action(content):
    logger.info(f"{Colors.GREEN}[行动]{Colors.ENDC} {content}")

def log_thinking(player_id, content):
    # 实际运行时可以隐藏思考过程，debug模式开启
    logger.info(f"{Colors.BLUE}[Player {player_id} 思考]{Colors.ENDC}: {content}")