# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 16:53:58 2025

@author: An Wen
"""

import re
from language_switch.language_switcher import get_text

# 定义一个用于存储统计信息的字典
java_analysis_result = {
    "total_executable": 0,            # 可执行语句总数
    "executable_statements":[],       # 可执行语句
    "decision_points_count": 0,       # 决策点数量（如 if/while/for 等）
    "conditions_decision": [],        # 所有控制流语句中的条件表达式
    "conditions_count": 0,            # 布尔条件表达式个数
    "conditions_condition": [],       # 提取出的布尔条件表达式内容
    "branch_count": 0                 # 提取出的控制流分支数量
}

# 语句覆盖
def count_executable_statements(pre_process_java_code):
    """
    基于识别不可执行语句来反推出可执行语句。
    已假设代码已预处理（即注释、空行已删除）。
    """
    # 拆分代码为所有语句（以分号为终结符号）
    all_statements = re.split(r';', pre_process_java_code)
    all_statements = [stmt.strip() + ';' for stmt in all_statements if stmt.strip()]
    # 不可执行语句的模式（如声明类、方法、package、import、空块等）
    non_exec_patterns = [
        r'^\s*package\s+[\w\.]+;',
        r'^\s*import\s+[\w\.]+;',
        r'^\s*(public|private|protected)?\s*(static\s+)?(final\s+)?class\s+\w+',
        r'^\s*(public|private|protected)?\s*(static\s+)?(final\s+)?[\w<>\[\]]+\s+\w+\s*\([^)]*\)\s*\{?',  # 方法定义
        r'^\s*\{$',      # 单独的大括号
        r'^\s*\}$',
    ]

    non_executable_statements = []
    for stmt in all_statements:
        if any(re.match(pattern, stmt) for pattern in non_exec_patterns):
            non_executable_statements.append(stmt)

    total_statements = len(all_statements)
    total_non_executable = len(non_executable_statements)
    total_executable = total_statements - total_non_executable

    executable_statements = [
        stmt for stmt in all_statements if stmt not in non_executable_statements
    ]

    
    print(f"\n{get_text('extracted_executable_statements_count')}: {total_executable}")
    print(f"\n{get_text('extracted_executable_statements')}: {executable_statements}")
    java_analysis_result["total_executable"] =  total_executable
    java_analysis_result["executable_statements"] =  executable_statements

# 决策覆盖
def decision(pre_process_java_code):
    decision_points_count = 0  # 控制流决策点个数
    conditions_decision = []  # 存储所有匹配到的条件表达式

    # 注意顺序：先匹配 'else if'，再匹配 'if'
    condition_patterns = [
        r'else\s+if\s*\((.*?)\)',  # 注意这里的空格和顺序
        r'if\s*\((.*?)\)',
        r'switch\s*\((.*?)\)',
        r'for\s*\((.*?)\)',
        r'while\s*\((.*?)\)'
    ]

    for pattern in condition_patterns:
        matches = re.findall(pattern, pre_process_java_code)
        conditions_decision.extend(matches)
        decision_points_count += len(matches)

    print(f"\n{get_text('extracted_decision_points_count', decision_points_count)}")
    java_analysis_result["decision_points_count"] =  decision_points_count
    java_analysis_result["conditions_decision"] =  conditions_decision

# 条件覆盖
def condition(pre_process_java_code):
    conditions_condition = []

    # 正确的顺序，先 else if，再 if
    condition_patterns = [
        r'else\s+if\s*\((.*?)\)', 
        r'if\s*\((.*?)\)',
        r'while\s*\((.*?)\)',
        r'for\s*\((.*?);(.*?);(.*?)\)'  # 拆出 for 的三个部分
    ]

    for pattern in condition_patterns:
        matches = re.findall(pattern, pre_process_java_code)
        if 'for' in pattern:
            # for 是一个元组列表 (init, condition, update)
            for match in matches:
                if len(match) > 1:
                    conditions_condition.append(match[1].strip())  # 提取中间部分作为布尔条件
        else:
            conditions_condition.extend([m.strip() for m in matches])

    conditions_count = len(conditions_condition)
    print(f"\n{get_text('extracted_conditions_count', conditions_count)}")
    java_analysis_result["conditions_count"] =  conditions_count
    java_analysis_result["conditions_condition"] =  conditions_condition

# 分支覆盖
def branch(pre_process_java_code):
    branch_count = 0
    branch_structures = []

    # 移除注释，避免误匹配
    code = re.sub(r'//.*?(\n|$)', '', pre_process_java_code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    # 1. if 和 else if（每个有 2 个分支）
    if_patterns = [
        (r'\belse\s+if\s*\((.*?)\)', 2, 'else if'),
        (r'\bif\s*\((.*?)\)', 2, 'if')
    ]
    for pattern, count, label in if_patterns:
        matches = re.findall(pattern, code)
        branch_count += len(matches) * count
        branch_structures.extend([f"{label}({m})" for m in matches])

    # 2. while 和 for 循环（每个有 2 个分支）
    loop_patterns = [
        (r'\bwhile\s*\((.*?)\)', 2, 'while'),
        (r'\bfor\s*\((.*?)\)', 2, 'for')
    ]
    for pattern, count, label in loop_patterns:
        matches = re.findall(pattern, code)
        branch_count += len(matches) * count
        branch_structures.extend([f"{label}({m})" for m in matches])

    # 3. switch-case（每个 case 是 1 个分支，default 是 1 个分支）
    switch_matches = re.findall(r'\bswitch\s*\((.*?)\)', code)
    case_matches = re.findall(r'\bcase\s+(.*?):', code)
    default_matches = re.findall(r'\bdefault\s*:', code)
    branch_count += len(case_matches) + len(default_matches)
    branch_structures.extend([f"switch({m})" for m in switch_matches])
    branch_structures.extend([f"case {m}:" for m in case_matches])
    branch_structures.extend(["default:"] * len(default_matches))

    # 4. catch 结构（每个 catch 是一个异常分支）
    catch_matches = re.findall(r'\bcatch\s*\((.*?)\)', code)
    branch_count += len(catch_matches)
    branch_structures.extend([f"catch({m})" for m in catch_matches])

    print(f"\n{get_text('extracted_branch_count', branch_count)}")
    print(f"\n{get_text('extracted_branch_structures', branch_structures)}")

    java_analysis_result["branch_count"] =  branch_count
    java_analysis_result["branch_structures"] =  branch_structures

def static_code_analysis_extra(pre_process_java_code,select):
    if select == 1:
        count_executable_statements(pre_process_java_code)
    if select == 2:
        condition(pre_process_java_code)
    if select == 3:
        branch(pre_process_java_code)
    if select ==4:
        decision(pre_process_java_code)
    return java_analysis_result