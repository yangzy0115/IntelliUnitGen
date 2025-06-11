# -*- coding: utf-8 -*-
"""
Created on Fri Apr  4 11:16:45 2025

@author: An Wen
"""

# from api_call.wenxin_api import large_model_response
from api_call.gpt_api import large_model_response

java_generate_test_cases_result = []
# statement_tests_result = []


# 语句覆盖
def step_by_step_prompt_statment_coverage2(pre_process_java_code, java_prompt_synthesis_result):
    
    # print("==================", java_prompt_synthesis_result)
    prompt_step0 = java_prompt_synthesis_result[0]
    print("【step0:系统提示 Prompt】\n",prompt_step0) 
    messages = [{"role": "user", "content": prompt_step0}]
    system_response = large_model_response(messages,0.2)
    print("【step0:系统提示 completion】\n",system_response)
    java_generate_test_cases_result.append(system_response)
    
    prompt_step1 = java_prompt_synthesis_result[1]
    print("【step1:结构信息 Prompt】\n",prompt_step1)
    messages.append({"role": "assistant", "content": system_response})
    messages.append = [
    {"role": "system", "content": "你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"},
    {"role": "user", "content":prompt_step1}
]
    # messages.append({"role": "user", "content": prompt_step1})
    illustrate_information = large_model_response(messages,0.7)
    print("【step1:结构信息 completion】\n", illustrate_information)
    java_generate_test_cases_result.append(illustrate_information)
    # return 
    
    prompt_step2 = java_prompt_synthesis_result[2]
    print("【step2:依赖关系 Prompt】\n",prompt_step2)
    messages.append({"role": "assistant", "content": illustrate_information})
    messages.append = [
    {"role": "system", "content": "你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"},
    {"role": "user", "content":prompt_step2}
]
    # messages.append({"role": "user", "content": prompt_step2})
    dependent_information = large_model_response(messages,0.7)
    print("【step2:依赖关系 completion】\n", dependent_information)
    java_generate_test_cases_result.append(dependent_information)
    # return 
    
    prompt_step3 = java_prompt_synthesis_result[3]
    print("【step3:分析可执行语句 Prompt】\n",prompt_step3)
    messages.append({"role": "assistant", "content": dependent_information})
    messages.append = [
    {"role": "system", "content": "你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"},
    {"role": "user", "content": prompt_step3}
]
    # messages.append({"role": "user", "content": prompt_step3})
    executable_statement = large_model_response(messages,0.7)
    print("【step3:分析可执行语句 completion】\n", executable_statement)
    java_generate_test_cases_result.append(executable_statement)
    # return
    
    prompt_step4 = java_prompt_synthesis_result[4]
    print("【step4:分析执行条件 Prompt】\n",prompt_step3)
    messages.append({"role": "assistant", "content": executable_statement})
    messages.append = [
    {"role": "system", "content": "你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"},
    {"role": "user", "content": prompt_step4}
]
    # messages.append({"role": "user", "content": prompt_step4})
    execution_condition = large_model_response(messages,0.7)
    print("【step4:执行条件 completion】\n", execution_condition)
    java_generate_test_cases_result.append(execution_condition)
    #  return
    
    prompt_step5 = java_prompt_synthesis_result[5]
    print("【step5:生成测试用例 Prompt】\n",prompt_step4)
    messages.append({"role": "assistant", "content": execution_condition})
    messages.append = [
    {"role": "system", "content": "你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"},
    {"role": "user", "content": prompt_step5}
]
    # messages.append({"role": "user", "content": prompt_step5})
    statement_tests = large_model_response(messages,0.7)
    print("【step5:语句覆盖测试用例 completion】\n", statement_tests)
    java_generate_test_cases_result.append(statement_tests)
    # print(messages)

    return

# 语句覆盖
def step_by_step_prompt_statment_coverage(pre_process_java_code, java_prompt_synthesis_result):
    
    messages = []
    # print("================================================================================")
    # print(java_prompt_synthesis_result)
    response = ""
    for prompt in java_prompt_synthesis_result:
        if len(response) != 0:
            messages.append({"role": "assistant", "content": response})
        prompt_role  = prompt["role"]
        prompt_content  = prompt["content"]
        messages.append({"role": prompt_role, "content": prompt_content})
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(prompt_content)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # response = large_model_response(messages, 0.7)
        response = large_model_response(messages, 0.2)
    messages_with_response = messages.copy()
    messages_with_response.append({"role": "assistant", "content": response})
    print("================================================================================")
    print(messages_with_response)
    print(response)
    java_generate_test_cases_result.append(response)

    return messages, messages_with_response

# 条件覆盖    
def step_by_step_prompt_condition_coverage(pre_process_java_code, java_prompt_synthesis_result):
    prompt_step0 = java_prompt_synthesis_result[0]
    print("【step0:系统提示 Prompt】\n",prompt_step0)
    messages = [{"role": "user", "content": prompt_step0}]
    system_response = large_model_response(messages,0.5)
    print("【step0:系统提示 completion】\n",system_response)
    java_generate_test_cases_result.append(system_response)
    
    prompt_step1 = java_prompt_synthesis_result[1]
    print("【step1:结构信息 Prompt】\n",prompt_step1)
    messages.append({"role": "assistant", "content": system_response})
    messages.append({"role": "user", "content": prompt_step1})
    illustrate_information = large_model_response(messages,0.5)
    print("【step1:结构信息 completion】\n", illustrate_information)
    java_generate_test_cases_result.append(illustrate_information)
    # return 
    
    prompt_step2 = java_prompt_synthesis_result[2]
    print("【step2:依赖关系 Prompt】\n",prompt_step2)
    messages.append({"role": "assistant", "content": illustrate_information})
    messages.append({"role": "user", "content": prompt_step2})
    dependent_information = large_model_response(messages,0.5)
    print("【step2:依赖关系 completion】\n", dependent_information)
    java_generate_test_cases_result.append(dependent_information)
    # return 
    
    prompt_step3 = java_prompt_synthesis_result[3]
    print("【step3:提取布尔表达式中的独立条件 Prompt】\n",prompt_step3)
    messages.append({"role": "assistant", "content": illustrate_information})
    messages.append({"role": "user", "content": prompt_step3})
    executable_statement = large_model_response(messages,0.5)
    print("【step3:提取布尔表达式中的独立条件 completion】\n", executable_statement)
    java_generate_test_cases_result.append(executable_statement)
    # return
    
    prompt_step4 = java_prompt_synthesis_result[4]
    print("【step4:对独立条件进行分析 Prompt】\n",prompt_step4)
    messages.append({"role": "assistant", "content": executable_statement})
    messages.append({"role": "user", "content": prompt_step4})
    execution_condition = large_model_response(messages,0.5)
    print("【step4:分析独立条件 completion】\n", execution_condition)
    java_generate_test_cases_result.append(execution_condition)
    #  return
    
    prompt_step5 = java_prompt_synthesis_result[5]
    print("【step5:生成测试用例 Prompt】\n",prompt_step5)
    messages.append({"role": "assistant", "content": execution_condition})
    messages.append({"role": "user", "content": prompt_step5})
    statement_tests = large_model_response(messages,0.2)
    print("【step5:条件覆盖测试用例 completion】\n", statement_tests)
    java_generate_test_cases_result.append(statement_tests)

    return messages

# 分支覆盖    
def step_by_step_prompt_branch_coverage(pre_process_java_code, java_prompt_synthesis_result):
    prompt_step0 = java_prompt_synthesis_result[0]
    print("【step0:系统提示 Prompt】\n",prompt_step0)
    messages = [{"role": "user", "content": prompt_step0}]
    system_response = large_model_response(messages,0.5)
    print("【step0:系统提示 completion】\n",system_response)
    java_generate_test_cases_result.append(system_response)
    
    prompt_step1 = java_prompt_synthesis_result[1]
    print("【step1:结构信息 Prompt】\n",prompt_step1)
    messages.append({"role": "assistant", "content": system_response})
    messages.append({"role": "user", "content": prompt_step1})
    illustrate_information = large_model_response(messages,0.5)
    print("【step1:结构信息 completion】\n", illustrate_information)
    java_generate_test_cases_result.append(illustrate_information)
    # return 
    
    prompt_step2 = java_prompt_synthesis_result[2]
    print("【step2:依赖关系 Prompt】\n",prompt_step2)
    messages.append({"role": "assistant", "content": illustrate_information})
    messages.append({"role": "user", "content": prompt_step2})
    dependent_information = large_model_response(messages,0.5)
    print("【step2:依赖关系 completion】\n", dependent_information)
    java_generate_test_cases_result.append(dependent_information)
    # return 
    
    prompt_step3 = java_prompt_synthesis_result[3]
    print("【step3:分析触发条件 Prompt】\n",prompt_step3)
    messages.append({"role": "assistant", "content": dependent_information})
    messages.append({"role": "user", "content": prompt_step3})
    executable_statement = large_model_response(messages,0.5)
    print("【step3:触发条件分析 completion】\n", executable_statement)
    java_generate_test_cases_result.append(executable_statement)
    # return
    
    prompt_step4 = java_prompt_synthesis_result[4]
    print("【step4:生成测试用例 Prompt】\n",prompt_step4)
    messages.append({"role": "assistant", "content": executable_statement})
    messages.append({"role": "user", "content": prompt_step4})
    statement_tests = large_model_response(messages,0.2)
    print("【step4:条件覆盖测试用例 completion】\n", statement_tests)
    java_generate_test_cases_result.append(statement_tests)


    #  return

# 决策覆盖    
def step_by_step_prompt_decision_coverage(pre_process_java_code, java_prompt_synthesis_result):
    prompt_step0 = java_prompt_synthesis_result[0]
    print("【step0:系统提示 Prompt】\n",prompt_step0)
    messages = [{"role": "user", "content": prompt_step0}]
    system_response = large_model_response(messages,0.5)
    print("【step0:系统提示 completion】\n",system_response)
    java_generate_test_cases_result.append(system_response)
    
    prompt_step1 = java_prompt_synthesis_result[1]
    print("【step1:结构信息 Prompt】\n",prompt_step1)
    messages.append({"role": "assistant", "content": system_response})
    messages.append({"role": "user", "content": prompt_step1})
    illustrate_information = large_model_response(messages,0.5)
    print("【step1:结构信息 completion】\n", illustrate_information)
    java_generate_test_cases_result.append(illustrate_information)
    # return 
    
    prompt_step2 = java_prompt_synthesis_result[2]
    print("【step2:依赖关系 Prompt】\n",prompt_step2)
    messages.append({"role": "assistant", "content": illustrate_information})
    messages.append({"role": "user", "content": prompt_step2})
    dependent_information = large_model_response(messages,0.5)
    print("【step2:依赖关系 completion】\n", dependent_information)
    java_generate_test_cases_result.append(dependent_information)
    # return 
    
    prompt_step3 = java_prompt_synthesis_result[3]
    print("【step3:分析不同情况的输入 Prompt】\n",prompt_step3)
    messages.append({"role": "assistant", "content": dependent_information})
    messages.append({"role": "user", "content": prompt_step3})
    executable_statement = large_model_response(messages,0.5)
    print("【step3:分析不同情况的输入 completion】\n", executable_statement)
    java_generate_test_cases_result.append(executable_statement)
    # return
    
    prompt_step4 = java_prompt_synthesis_result[4]
    print("【step4:生成测试用例 Prompt】\n",prompt_step4)
    messages.append({"role": "assistant", "content": executable_statement})
    messages.append({"role": "user", "content": prompt_step4})
    statement_tests = large_model_response(messages,0.2)
    print("【step4:条件覆盖测试用例 completion】\n", statement_tests)
    java_generate_test_cases_result.append(statement_tests)


    #  return
    
# 路径覆盖    
def step_by_step_prompt_path_coverage(pre_process_java_code, java_prompt_synthesis_result):
    prompt_step0 = java_prompt_synthesis_result[0]
    print("【step0:系统提示 Prompt】\n",prompt_step0)
    messages = [{"role": "user", "content": prompt_step0}]
    system_response = large_model_response(messages,0.5)
    print("【step0:系统提示 completion】\n",system_response)
    java_generate_test_cases_result.append(system_response)
    
    prompt_step1 = java_prompt_synthesis_result[1]
    print("【step1:结构信息 Prompt】\n",prompt_step1)
    messages.append({"role": "assistant", "content": system_response})
    messages.append({"role": "user", "content": prompt_step1})
    illustrate_information = large_model_response(messages,0.5)
    print("【step1:结构信息 completion】\n", illustrate_information)
    java_generate_test_cases_result.append(illustrate_information)
    # return 
    
    prompt_step2 = java_prompt_synthesis_result[2]
    print("【step2:依赖关系 Prompt】\n",prompt_step2)
    messages.append({"role": "assistant", "content": illustrate_information})
    messages.append({"role": "user", "content": prompt_step2})
    dependent_information = large_model_response(messages,0.5)
    print("【step2:依赖关系 completion】\n", dependent_information)
    java_generate_test_cases_result.append(dependent_information)
    # return 
    
    prompt_step3 = java_prompt_synthesis_result[3]
    print("【step3:计算环路复杂度 Prompt】\n",prompt_step3)
    messages.append({"role": "assistant", "content": dependent_information})
    messages.append({"role": "user", "content": prompt_step3})
    executable_statement = large_model_response(messages,0.5)
    print("【step3:环路复杂度计算 completion】\n", executable_statement)
    java_generate_test_cases_result.append(executable_statement)
    # return
    
    prompt_step4 = java_prompt_synthesis_result[4]
    print("【step4:设计触发条件 Prompt】\n",prompt_step4)
    messages.append({"role": "assistant", "content": executable_statement})
    messages.append({"role": "user", "content": prompt_step4})
    execution_condition = large_model_response(messages,0.5)
    print("【step4:触发条件设计 completion】\n", execution_condition)
    java_generate_test_cases_result.append(execution_condition)
    #  return
    
    prompt_step5 = java_prompt_synthesis_result[5]
    print("【step5:生成测试用例 Prompt】\n",prompt_step5)
    messages.append({"role": "assistant", "content": execution_condition})
    messages.append({"role": "user", "content": prompt_step5})
    statement_tests = large_model_response(messages,0.2)
    print("【step5:条件覆盖测试用例 completion】\n", statement_tests)
    java_generate_test_cases_result.append(statement_tests)


    return
    
def generate_test_case(pre_process_java_code, java_prompt_synthesis_result, select,test_class_name):
    if select == 1:
        messages, messages_with_response = step_by_step_prompt_statment_coverage(pre_process_java_code, java_prompt_synthesis_result)

    if select == 2:
        step_by_step_prompt_condition_coverage(pre_process_java_code, java_prompt_synthesis_result)

    if select == 3:
        step_by_step_prompt_branch_coverage(pre_process_java_code, java_prompt_synthesis_result)

    if select == 4:
        step_by_step_prompt_decision_coverage(pre_process_java_code, java_prompt_synthesis_result)

    if select == 5:
        step_by_step_prompt_path_coverage(pre_process_java_code, java_prompt_synthesis_result)
    
    return java_generate_test_cases_result, messages, messages_with_response