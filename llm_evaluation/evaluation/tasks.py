"""评估任务定义"""
import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class EvaluationTask:
    """评估任务"""
    task_id: str
    name: str
    description: str
    test_file: str
    prompt_template: str
    evaluation_criteria: List[str]
    max_score: int = 100

# 定义所有评估任务
EVALUATION_TASKS = [
    EvaluationTask(
        task_id="task1",
        name="数据概览与质量评估",
        description="测试模型理解数据结构和评估数据质量的能力",
        test_file="normal_operation_3days.xlsx",
        prompt_template="task1_data_overview",
        evaluation_criteria=[
            "正确识别数据维度和时间范围",
            "准确计算基础统计量",
            "识别数据质量问题",
            "生成合适的可视化",
            "代码可运行性"
        ],
        max_score=100
    ),
    
    EvaluationTask(
        task_id="task2",
        name="时序模式分析",
        description="测试模型发现时序模式和规律的能力",
        test_file="normal_operation_3days.xlsx",
        prompt_template="task2_pattern_analysis",
        evaluation_criteria=[
            "识别日内充电模式",
            "发现设备差异",
            "相关性分析准确性",
            "可视化效果",
            "洞察深度"
        ],
        max_score=100
    ),
    
    EvaluationTask(
        task_id="task3",
        name="异常检测",
        description="测试模型检测各类异常的能力",
        test_file="abnormal_operation_3days.xlsx",
        prompt_template="task3_anomaly_detection",
        evaluation_criteria=[
            "检测设备故障",
            "识别数据缺失",
            "发现异常峰值",
            "异常原因分析",
            "处理建议合理性"
        ],
        max_score=100
    ),
    
    EvaluationTask(
        task_id="task4",
        name="业务洞察",
        description="测试模型提取业务价值的能力",
        test_file="normal_operation_3days.xlsx",
        prompt_template="task4_business_insights",
        evaluation_criteria=[
            "设备效率计算",
            "优化建议质量",
            "业务理解深度",
            "建议可行性",
            "价值量化能力"
        ],
        max_score=100
    ),
    
    EvaluationTask(
        task_id="task5",
        name="综合报告生成",
        description="测试模型生成完整分析报告的能力",
        test_file="cumulative_discharge_1day.xlsx",
        prompt_template="task5_comprehensive_report",
        evaluation_criteria=[
            "报告结构完整性",
            "执行摘要质量",
            "分析深度",
            "可视化专业性",
            "建议实用性"
        ],
        max_score=100
    )
]

def get_task_by_id(task_id: str) -> EvaluationTask:
    """根据ID获取任务"""
    for task in EVALUATION_TASKS:
        if task.task_id == task_id:
            return task
    raise ValueError(f"Task {task_id} not found")

def get_all_tasks() -> List[EvaluationTask]:
    """获取所有任务"""
    return EVALUATION_TASKS