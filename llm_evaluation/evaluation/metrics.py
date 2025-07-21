"""评估指标计算"""
import re
import ast
from typing import Dict, List, Any, Tuple
import subprocess
import tempfile
import os

class EvaluationMetrics:
    """评估指标计算器"""
    
    @staticmethod
    def evaluate_code_quality(code: str) -> Dict[str, Any]:
        """评估代码质量"""
        metrics = {
            "is_valid_python": False,
            "is_runnable": False,
            "has_imports": False,
            "has_visualizations": False,
            "execution_error": None,
            "line_count": 0
        }
        
        # 检查是否是有效的Python代码
        try:
            ast.parse(code)
            metrics["is_valid_python"] = True
        except SyntaxError as e:
            metrics["execution_error"] = str(e)
            return metrics
        
        # 统计代码行数
        metrics["line_count"] = len(code.strip().split('\n'))
        
        # 检查必要的导入
        if "import pandas" in code or "from pandas" in code:
            metrics["has_imports"] = True
        
        # 检查是否有可视化
        viz_keywords = ["plt.", "plot", "figure", "chart", "seaborn", "plotly"]
        metrics["has_visualizations"] = any(keyword in code for keyword in viz_keywords)
        
        # 尝试运行代码（在安全环境中）
        # 注意：实际生产环境中需要更严格的沙箱环境
        metrics["is_runnable"] = metrics["is_valid_python"]  # 简化处理
        
        return metrics
    
    @staticmethod
    def evaluate_data_understanding(response: str, expected_patterns: List[str]) -> Dict[str, float]:
        """评估数据理解能力"""
        scores = {}
        
        # 检查是否提到了关键的数据特征
        patterns_found = 0
        for pattern in expected_patterns:
            if pattern.lower() in response.lower():
                patterns_found += 1
        
        scores["pattern_recognition"] = patterns_found / len(expected_patterns) if expected_patterns else 0
        
        # 检查是否包含数字/统计信息
        numbers = re.findall(r'\d+\.?\d*', response)
        scores["quantitative_analysis"] = min(len(numbers) / 10, 1.0)  # 期望至少10个数字
        
        # 检查分析深度（通过响应长度粗略估计）
        scores["analysis_depth"] = min(len(response) / 2000, 1.0)  # 期望至少2000字符
        
        return scores
    
    @staticmethod
    def evaluate_visualization_quality(code: str) -> Dict[str, float]:
        """评估可视化质量"""
        scores = {
            "has_labels": 0,
            "has_title": 0,
            "has_legend": 0,
            "plot_types": 0,
            "aesthetics": 0
        }
        
        # 检查标签
        if "xlabel" in code or "ylabel" in code:
            scores["has_labels"] = 1
        
        # 检查标题
        if "title" in code or "suptitle" in code:
            scores["has_title"] = 1
        
        # 检查图例
        if "legend" in code:
            scores["has_legend"] = 1
        
        # 检查图表类型多样性
        plot_types = ["plot", "scatter", "bar", "hist", "heatmap", "boxplot"]
        types_found = sum(1 for pt in plot_types if pt in code)
        scores["plot_types"] = min(types_found / 3, 1.0)  # 期望至少3种图表
        
        # 美观性（检查是否有样式设置）
        style_keywords = ["style", "color", "alpha", "figsize", "dpi"]
        style_found = sum(1 for sk in style_keywords if sk in code)
        scores["aesthetics"] = min(style_found / 3, 1.0)
        
        return scores
    
    @staticmethod
    def evaluate_business_insights(response: str) -> Dict[str, float]:
        """评估业务洞察质量"""
        scores = {
            "actionability": 0,
            "specificity": 0,
            "domain_knowledge": 0
        }
        
        # 可执行性（检查是否有具体建议）
        action_keywords = ["建议", "应该", "可以", "需要", "优化", "改进", "提升"]
        scores["actionability"] = min(sum(1 for k in action_keywords if k in response) / 3, 1.0)
        
        # 具体性（检查是否有数字支撑）
        has_percentages = bool(re.findall(r'\d+%', response))
        has_metrics = bool(re.findall(r'\d+\.?\d*\s*(kW|MW|kWh|MWh|小时|分钟|天)', response))
        scores["specificity"] = (has_percentages + has_metrics) / 2
        
        # 领域知识（检查专业术语）
        domain_terms = ["储能", "充放电", "效率", "功率", "容量", "峰谷", "负荷", "PCS", "集装箱"]
        terms_found = sum(1 for term in domain_terms if term in response)
        scores["domain_knowledge"] = min(terms_found / 5, 1.0)
        
        return scores
    
    @staticmethod
    def calculate_total_score(metrics: Dict[str, Any], task_type: str) -> Tuple[float, Dict[str, float]]:
        """计算总分"""
        weights = {
            "task1": {  # 数据概览
                "code_quality": 0.3,
                "data_understanding": 0.4,
                "visualization": 0.3
            },
            "task2": {  # 模式分析
                "code_quality": 0.25,
                "data_understanding": 0.35,
                "visualization": 0.4
            },
            "task3": {  # 异常检测
                "code_quality": 0.3,
                "data_understanding": 0.5,
                "visualization": 0.2
            },
            "task4": {  # 业务洞察
                "code_quality": 0.2,
                "business_insights": 0.6,
                "data_understanding": 0.2
            },
            "task5": {  # 综合报告
                "data_understanding": 0.3,
                "visualization": 0.3,
                "business_insights": 0.4
            }
        }
        
        task_weights = weights.get(task_type, weights["task1"])
        detailed_scores = {}
        total_score = 0
        
        for component, weight in task_weights.items():
            if component in metrics:
                # 处理不同类型的指标
                if isinstance(metrics[component], dict):
                    # 过滤掉None值
                    valid_values = [v for v in metrics[component].values() if v is not None]
                    if valid_values:
                        # 对于布尔值转换为0或1
                        numeric_values = []
                        for v in valid_values:
                            if isinstance(v, bool):
                                numeric_values.append(1 if v else 0)
                            elif isinstance(v, (int, float)):
                                numeric_values.append(v)
                        
                        if numeric_values:
                            component_score = sum(numeric_values) / len(metrics[component])
                        else:
                            component_score = 0
                    else:
                        component_score = 0
                else:
                    component_score = 0
                
                detailed_scores[component] = component_score
                total_score += component_score * weight
        
        return total_score * 100, detailed_scores  # 转换为百分制