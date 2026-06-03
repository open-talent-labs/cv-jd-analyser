# cv-jd-analyser

AI 赋能的简历与职位描述深度匹配分析引擎。

## 项目结构

```
cv-jd-analyser/
├── .github/workflows/   # CI/CD 自动化流水线
├── src/
│   ├── main.py          # 应用主入口
│   ├── api/             # API 层（FastAPI 路由）
│   ├── core/            # 核心业务逻辑（匹配、解析、Agent）
│   └── utils/           # 工具函数
├── tests/               # 单元测试
├── scripts/             # 脚本工具
├── requirements.txt     # 依赖管理
└── .env.example         # 环境变量模板
```

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 配置 API Key
cp .env.example .env
# 编辑 .env 填入你的 API Key

# 运行应用
python src/main.py
```

## 功能特性

- 📄 PDF 简历解析与结构化信息抽取
- 🔍 简历与 JD 语义匹配评分
- 🤖 多 Agent 深度分析（HR 视角 / Tech Lead 视角 / Career Coach 视角）
- 🚀 支持本地 LLM 推理加速（vLLM / TensorRT-LLM）
- 📊 可视化匹配报告
