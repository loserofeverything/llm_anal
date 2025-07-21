import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_test_datasets():
    """创建不同场景的测试数据集"""
    
    # 确保目录存在
    os.makedirs('data/samples', exist_ok=True)
    
    # 1. 正常运行数据（3天）
    print("创建正常运行数据...")
    start_date = datetime(2025, 7, 1)
    time_intervals = 15  # 15分钟间隔
    days = 3
    
    timestamps = []
    current = start_date
    for _ in range(days * 24 * 60 // time_intervals):
        timestamps.append(current)
        current += timedelta(minutes=time_intervals)
    
    # 创建正常充电模式（白天充电多，晚上充电少）
    normal_data = pd.DataFrame()
    normal_data['时间'] = timestamps
    
    # 为5个集装箱的6个PCS设备生成数据
    for container in range(1, 6):
        for pcs in range(1, 7):
            col_name = f"{container}号集装箱{pcs:02d}PCS 当天交流充电电量"
            # 生成具有日内模式的数据
            hour_of_day = pd.Series([t.hour for t in timestamps])
            base_pattern = 50 + 40 * np.sin((hour_of_day - 6) * np.pi / 12)
            noise = np.random.normal(0, 5, len(timestamps))
            normal_data[col_name] = np.maximum(0, base_pattern + noise)
    
    normal_data.to_excel('data/samples/normal_operation_3days.xlsx', index=False)
    
    # 2. 包含异常的数据
    print("创建包含异常的数据...")
    abnormal_data = normal_data.copy()
    
    # 设备故障：2号集装箱03PCS在第二天停止工作
    fault_start = days * 24 * 4  # 第二天开始
    abnormal_data.loc[fault_start:, '2号集装箱03PCS 当天交流充电电量'] = 0
    
    # 数据缺失：3号集装箱所有设备在某些时段缺失
    missing_start = 50
    missing_end = 70
    for pcs in range(1, 7):
        col_name = f"3号集装箱{pcs:02d}PCS 当天交流充电电量"
        abnormal_data.loc[missing_start:missing_end, col_name] = np.nan
    
    # 异常峰值：4号集装箱01PCS出现异常高值
    spike_indices = [100, 150, 200]
    abnormal_data.loc[spike_indices, '4号集装箱01PCS 当天交流充电电量'] = 150
    
    abnormal_data.to_excel('data/samples/abnormal_operation_3days.xlsx', index=False)
    
    # 3. 累计数据（单天）
    print("创建累计放电量数据...")
    cumulative_data = pd.DataFrame()
    cumulative_timestamps = []
    current = start_date
    for _ in range(48):  # 30分钟间隔，一天数据
        cumulative_timestamps.append(current)
        current += timedelta(minutes=30)
    
    cumulative_data['时间'] = cumulative_timestamps
    
    # 累计值应该单调递增
    for container in range(1, 6):
        for pcs in range(1, 7):
            col_name = f"{container}号集装箱{pcs:02d}PCS 累积交流放电电量"
            base_value = 1000 + container * 100 + pcs * 10
            increment = np.random.uniform(0, 5, len(cumulative_timestamps))
            cumulative_data[col_name] = base_value + np.cumsum(increment)
    
    cumulative_data.to_excel('data/samples/cumulative_discharge_1day.xlsx', index=False)
    
    print("测试数据集创建完成！")
    
    # 创建数据说明文档
    description = """# 测试数据集说明

## 1. normal_operation_3days.xlsx
- 时间范围：3天
- 数据间隔：15分钟
- 特征：正常的日内充电模式，白天充电量高，夜间充电量低
- 用途：测试基础分析能力

## 2. abnormal_operation_3days.xlsx
- 基于正常数据，包含以下异常：
  - 设备故障：2号集装箱03PCS第二天开始停止工作
  - 数据缺失：3号集装箱所有设备在某时段数据缺失
  - 异常峰值：4号集装箱01PCS出现异常高值
- 用途：测试异常检测能力

## 3. cumulative_discharge_1day.xlsx
- 时间范围：1天
- 数据间隔：30分钟
- 特征：累计放电量，单调递增
- 用途：测试对累计值的理解能力
"""
    
    with open('data/samples/README.md', 'w') as f:
        f.write(description)

if __name__ == "__main__":
    create_test_datasets()