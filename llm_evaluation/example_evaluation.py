"""
评估示例脚本 - 展示如何使用评估框架
"""
import os
import yaml
from evaluation.tasks import get_task_by_id
from evaluation.metrics import EvaluationMetrics

def load_prompts():
    """加载提示词模板"""
    with open('config/prompts.yaml', 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def simulate_llm_response(task_id: str):
    """模拟LLM响应（实际使用时替换为真实的API调用）"""
    # 这里仅作示例，返回模拟的响应
    if task_id == "task1":
        return """
根据数据分析，该Excel文件包含了储能设备的充电数据：

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 读取数据
df = pd.read_excel('data/samples/normal_operation_3days.xlsx')

# 1. 数据基本信息
print("数据维度:", df.shape)
print("时间范围:", df['时间'].min(), "到", df['时间'].max())
print("采样间隔:", (df['时间'][1] - df['时间'][0]).total_seconds() / 60, "分钟")

# 2. 数据质量检查
missing_values = df.isnull().sum()
print("\\n缺失值统计:")
print(missing_values[missing_values > 0])

# 3. 基础统计描述
device_cols = [col for col in df.columns if 'PCS' in col]
stats = df[device_cols].describe()
print("\\n基础统计信息:")
print(stats)

# 4. 数据分布可视化
plt.figure(figsize=(15, 10))

# 子图1: 时序趋势
plt.subplot(2, 2, 1)
for i, col in enumerate(device_cols[:5]):  # 显示前5个设备
    plt.plot(df['时间'], df[col], label=col[:10], alpha=0.7)
plt.xlabel('时间')
plt.ylabel('充电量 (kWh)')
plt.title('设备充电量时序趋势')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.xticks(rotation=45)

# 子图2: 数据分布箱线图
plt.subplot(2, 2, 2)
df[device_cols].boxplot(rot=90)
plt.title('各设备充电量分布')
plt.ylabel('充电量 (kWh)')

# 子图3: 相关性热力图
plt.subplot(2, 2, 3)
correlation = df[device_cols].corr()
sns.heatmap(correlation, cmap='coolwarm', center=0, square=True)
plt.title('设备间相关性热力图')

# 子图4: 日平均充电量
plt.subplot(2, 2, 4)
df['日期'] = df['时间'].dt.date
daily_avg = df.groupby('日期')[device_cols].mean()
daily_avg.plot(kind='bar', stacked=True)
plt.title('日平均充电量')
plt.xlabel('日期')
plt.ylabel('平均充电量 (kWh)')

plt.tight_layout()
plt.show()

# 5. 数据质量评估报告
print("\\n数据质量评估报告:")
print(f"- 数据完整性: {(1 - df.isnull().sum().sum() / df.size) * 100:.2f}%")
print(f"- 设备数量: {len(device_cols)} 个")
print(f"- 数据时长: {(df['时间'].max() - df['时间'].min()).days} 天")
print(f"- 总记录数: {len(df)} 条")
```

数据分析发现：
1. 数据包含30个PCS设备，时间跨度3天，15分钟采样间隔
2. 数据质量良好，无缺失值
3. 充电量呈现明显的日内周期性模式
4. 不同设备间存在较强相关性，可能受统一调度影响
"""
    else:
        return "模拟的LLM响应内容..."

def evaluate_response(task_id: str, response: str):
    """评估LLM响应"""
    task = get_task_by_id(task_id)
    metrics = {}
    
    # 提取代码部分
    code_blocks = []
    in_code = False
    current_code = []
    for line in response.split('\n'):
        if line.strip().startswith('```python'):
            in_code = True
            current_code = []
        elif line.strip() == '```' and in_code:
            in_code = False
            code_blocks.append('\n'.join(current_code))
        elif in_code:
            current_code.append(line)
    
    # 评估代码质量
    if code_blocks:
        code = '\n'.join(code_blocks)
        metrics['code_quality'] = EvaluationMetrics.evaluate_code_quality(code)
        metrics['visualization'] = EvaluationMetrics.evaluate_visualization_quality(code)
    
    # 评估数据理解
    expected_patterns = ['时间范围', '采样间隔', '设备数量', '数据质量', '缺失值']
    metrics['data_understanding'] = EvaluationMetrics.evaluate_data_understanding(
        response, expected_patterns
    )
    
    # 评估业务洞察（如果适用）
    if task_id in ['task4', 'task5']:
        metrics['business_insights'] = EvaluationMetrics.evaluate_business_insights(response)
    
    # 计算总分
    total_score, detailed_scores = EvaluationMetrics.calculate_total_score(metrics, task_id)
    
    return {
        'task_id': task_id,
        'total_score': total_score,
        'detailed_scores': detailed_scores,
        'metrics': metrics
    }

def main():
    """主函数"""
    print("="*60)
    print("LLM时序数据分析能力评估示例")
    print("="*60)
    
    # 选择评估任务
    task_id = "task1"
    task = get_task_by_id(task_id)
    
    print(f"\n任务: {task.name}")
    print(f"描述: {task.description}")
    print(f"测试文件: {task.test_file}")
    
    # 获取LLM响应（这里使用模拟）
    print("\n获取LLM响应...")
    response = simulate_llm_response(task_id)
    
    # 评估响应
    print("\n评估响应质量...")
    evaluation_result = evaluate_response(task_id, response)
    
    # 显示结果
    print(f"\n总分: {evaluation_result['total_score']:.2f}/100")
    print("\n详细得分:")
    for component, score in evaluation_result['detailed_scores'].items():
        print(f"  - {component}: {score:.2%}")
    
    print("\n评估标准:")
    for criterion in task.evaluation_criteria:
        print(f"  - {criterion}")
    
    print("\n" + "="*60)
    print("评估完成！")
    
    # 实际使用建议
    print("\n实际使用时的步骤：")
    print("1. 将simulate_llm_response()替换为真实的LLM API调用")
    print("2. 批量运行所有任务，收集各模型的响应")
    print("3. 使用评估框架自动打分")
    print("4. 生成对比报告和可视化")
    print("5. 人工审核关键指标，调整权重")

if __name__ == "__main__":
    main()