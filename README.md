# AiAvalon

Ai_Avalon/
├── data/
│   └── rules.txt           # 完整的阿瓦隆规则 Prompt 上下文
├── config/
│   ├── settings.py         # 模型配置 (OpenAI/Anthropic API Key)
│   └── prompts.py          # Prompt 模板 (Jinja2 或 f-string)
├── engine/                 # 游戏核心 (Game Master)
│   ├── game.py             # 状态机：发牌->讨论->提案->投票->任务->刺杀
│   ├── roles.py            # 角色类：定义阵营、视野信息
│   └── state.py            # 数据类：存储全局游戏记录 (Board)
├── agents/                 # 玩家智能体
│   ├── base.py             # 接口定义
│   ├── llm_agent.py        # 核心：调用 LLM，维护 memory/thinking
│   └── schemas.py          # Pydantic 模型 (用于结构化输出)
├── utils/
│   └── logger.py           # 日志系统
├── main.py                 # 启动入口
└── requirements.txt