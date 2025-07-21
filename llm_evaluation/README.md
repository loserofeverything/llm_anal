# 大模型时序数据分析能力评估项目

## 项目结构
```
llm_evaluation/
├── README.md                 # 项目说明
├── config/                   # 配置文件
│   ├── models.yaml          # 模型配置
│   └── prompts.yaml         # 提示词模板
├── data/                    # 测试数据
│   ├── samples/             # 数据样本
│   └── ground_truth/        # 标准答案
├── evaluation/              # 评估脚本
│   ├── __init__.py
│   ├── tasks.py             # 评估任务定义
│   ├── metrics.py           # 评估指标
│   └── runner.py            # 评估执行器
├── results/                 # 评估结果
│   └── reports/             # 分析报告
└── notebooks/               # Jupyter笔记本
    └── analysis.ipynb       # 结果分析
```

## 快速开始

1. 准备测试数据
2. 配置要评估的模型
3. 运行评估脚本
4. 分析评估结果

## 评估维度

- 数据理解能力
- 分析深度
- 可视化质量
- 代码可运行性
- 业务洞察价值