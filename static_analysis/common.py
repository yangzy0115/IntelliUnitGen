# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 14:17:18 2025

@author: An Wen
"""
import re
from language_switch.language_switcher import get_text

# 解析 Java 代码结构
def parse_java_code_structure(java_code):
    conditions = []
    exceptions = []
    functions = []
    classes = []

    # 提取判定节点
    condition_patterns = [
        r'if\s*\((.*?)\)',
        r'else if\s*\((.*?)\)',
        r'switch\s*\((.*?)\)',
        r'for\s*\((.*?)\)',
        r'while\s*\((.*?)\)'
    ]
    
    for pattern in condition_patterns:
        conditions.extend(re.findall(pattern, java_code))
    
    # 提取 try-catch 异常处理
    exception_patterns = [
        r'try\s*{',
        r'catch\s*\((.*?)\)'  # 提取 catch 语句
    ]
    for pattern in exception_patterns:
        exceptions.extend(re.findall(pattern, java_code))
    
    # 提取类定义
    class_pattern = r'(?:public\s+|protected\s+|private\s+|abstract\s+|final\s+)?class\s+(\w+)'


    classes.extend(re.findall(class_pattern, java_code))
    
    # 提取方法定义（修正正则表达式以排除构造方法、避免匹配非方法体的关键词）
    function_pattern = r'(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:final\s+)?(?:[\w<>\[\]]+)\s+(?!if|while|for|switch)(\w+)\s*\((.*?)\)\s*(?:throws\s+\S+)?\s*\{'  
    functions.extend(re.findall(function_pattern, java_code))
    
    print(f"\n{get_text('extracted_decision_nodes')} :  {conditions}")
    print(f"\n{get_text('extracted_exception_handling')} : {exceptions}")
    print(f"\n{get_text('extracted_class_name')} : {classes}")
    print(f"\n{get_text('extracted_method_name')} : {functions}")
    
    return conditions, exceptions, functions, classes

# 提取函数输入参数
def extract_function_input_parameters(java_code):
    function_pattern = r'(?:(public|private|protected)\s+)?(?:static\s+)?(?:final\s+)?(?:[\w<>\[\]]+)\s+(?!if|while|for|switch)(\w+)\s*\((.*?)\)\s*(?:throws\s+\S+)?\s*\{'  
    function_matches = re.findall(function_pattern, java_code)
    function_details = []
    
    for match in function_matches:
        modifier = match[0] if match[0] else "default"  # 如果没有修饰符，设为default
        func_name = match[1]
        inputs = match[2].split(',')
        inputs = [input.strip() for input in inputs if input.strip()]
        function_details.append({
            "function_name": func_name, 
            "parameters": inputs,
            "modifier": modifier
        })
    
    print(f"\n{get_text('extracted_method_info')}: {function_details}")
    return function_details
"""
def static_code_analysis_common(pre_process_java_code):
    parse_java_code_structure(pre_process_java_code)
    extract_function_input_parameters(pre_process_java_code)
"""


def static_code_analysis_common(pre_process_java_code):
    conditions, exceptions, functions, classes = parse_java_code_structure(pre_process_java_code)
    function_details = extract_function_input_parameters(pre_process_java_code)

    return {
        "classes": classes or [],
        "functions": functions or [],
        "function_details": function_details or [],
        "conditions": conditions or [],
        "exceptions": exceptions or []
    }
