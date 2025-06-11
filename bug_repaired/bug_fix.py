# -*- coding: utf-8 -*-
"""
Created on Sat Apr  5 21:15:15 2025

@author: An Wen
"""

import re
import os
import shutil
import subprocess
import time
from import_export.save_code import save_the_test_cases
from api_call.gpt_api import large_model_response
import openai
from post_process.private_method_reflect import reflect_private_method_calls
from post_process.package_import_add import add_package_and_import, add_package_and_import_auto
from generate_test_cases.test_cases_generation import generate_test_case
from post_process.convert_T_type import covert_T_type

def compile_and_run_java(test_file_path, test_file_path_run, test_class_name):
    """使用 Maven 编译并运行 Java 测试用例，失败后调用大模型重新生成测试代码，最多尝试十次"""
    test_dir = os.path.dirname(test_file_path_run)
    maven_path = shutil.which("mvn")
    javac_path = shutil.which("javac")

    if not os.path.exists(os.path.join(test_dir, "pom.xml")):
        print(f"❌ 找不到 pom.xml：{test_dir}")
        return None, None, None, None

    # 首先执行 mvn clean compile 来编译核心代码
    print("\n🚀 开始编译核心代码：mvn clean compile")
    compile_core = subprocess.run(
        [maven_path, "clean", "compile"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir
    )
    
    if compile_core.returncode != 0:
        print("❌ 核心代码编译失败：")
        print(compile_core.stdout + "\n" + compile_core.stderr)
        return compile_core.returncode, None, compile_core.stdout + "\n" + compile_core.stderr, None

    # 然后使用 javac 直接编译测试类，获取详细的语法错误
    compile_result = subprocess.run(
        # [javac_path, "-verbose", "-Xlint:all", test_file_path],
		[maven_path, "test-compile", f"-Dtest={test_class_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir
    )

    compile_log = compile_result.stdout + "\n" + compile_result.stderr
    print("❌ 测试类编译结果：")
    print(compile_log)  # 始终打印编译日志

    # 如果 javac 编译失败，直接返回编译错误
    if compile_result.returncode != 0:
        print("❌ 测试类编译失败：")
        return compile_result.returncode, None, compile_log, None

    # 如果 javac 编译成功，再使用 Maven 运行测试
    print("\n🚀 开始执行测试：mvn test")
    test_result = subprocess.run(
        [maven_path, "test", "-X", f"-Dtest={test_class_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=test_dir
    )

    # 合并日志
    test_log = (test_result.stdout or "") + "\n" + (test_result.stderr or "")

    # 用正则提取测试统计
    match = re.search(r"Tests run: (\d+), Failures: (\d+), Errors: (\d+)", test_log)
    if match:
        failures = int(match.group(2))
        errors = int(match.group(3))
        if failures == 0 and errors == 0:
            print("✅ 测试全部通过！")
            print("\n🚀 开始执行验证：mvn clean verify")
            verify_result = subprocess.run(
                [maven_path, "clean", "verify"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=test_dir
            )

            verify_log = (verify_result.stdout or "") + "\n" + (verify_result.stderr or "")
            print(verify_log)

            if "BUILD SUCCESS" in verify_log:
                print("✅ 验证成功！")
            else:
                print("❌ 验证失败")
                return 0, 1, compile_log, verify_log
            return 0, 0, compile_log, test_log
        else:
            print(f"❌ 测试有失败或错误（Failures: {failures}, Errors: {errors}）")
            # print(test_log)  # 打印测试错误信息
            return 0, 1, compile_log, test_log

    # 没有统计行时再判断 BUILD SUCCESS/FAILURE
    if "BUILD SUCCESS" in test_log:
        print("✅ 构建成功，但未检测到测试统计信息")
        return 0, 0, compile_log, test_log
    elif "BUILD FAILURE" in test_log:
        print("❌ 构建失败")
        # print(test_log)  # 打印构建失败信息
        return 0, 1, compile_log, test_log
    else:
        print("⚠️ 未能判断测试结果，默认成功")
        return 0, 0, compile_log, test_log

# def extract_error_message(compile_log, test_log):
#     error_message = ""
    
#     # 打印原始编译日志，用于调试
#     print("\n=== 原始编译日志 ===")
#     print(compile_log)
#     print("=== 编译日志结束 ===\n")
    
#     # 处理 compile_log
#     if compile_log:
#         # 提取 javac 编译错误 - 匹配文件路径后的错误信息，包括错误行和指向行
#         error_blocks = re.findall(r"([^\n]*\.java:\d+: 错误:.*?)(?:\n\s+.*?\n\s+\^|\n|$)", compile_log, re.DOTALL)
#         print("\n=== 匹配到的 javac 错误 ===")
#         print(error_blocks)
#         print("=== javac 错误结束 ===\n")
        
#         if error_blocks:
#             # 添加错误解释
#             error_explanations = []
#             for error in error_blocks:
#                 if "需要<标识符>" in error:
#                     error_explanations.append("语法错误：在 throws 子句中的逗号后面缺少异常类型")
#                 elif "需要';'" in error:
#                     error_explanations.append("语法错误：异常类型重复声明，需要分号结束语句")
#                 else:
#                     error_explanations.append(error)
            
#             error_message += "编译错误：\n" + "\n".join(error_explanations) + "\n\n"
    
#     # 只有在没有编译错误的情况下才处理测试错误
#     if not error_message and test_log:
#         # 提取测试错误
#         test_errors = re.findall(r"\[ERROR\].*?(?=\n|$)", test_log)
#         if test_errors:
#             error_message += "测试错误：\n" + "\n".join(test_errors)
    
#     return error_message if error_message else "未找到具体错误信息"

def fix_bug(messages_with_response, test_file_path, test_class_name, compile_log, test_log, method_signature, dependency_classes):
    if messages_with_response is None:
        messages_with_response = []

    fix_bug_times = 1
    max_retries = 5
    retry_delay = 10  # 初始等待时间（秒）
    
    while fix_bug_times <= 30:
        fix_bug_times += 1
        print(f"$$$$$$$$$$$$$$$$$$第{fix_bug_times}次生成或修复$$$$$$$$$$$$$$$$$$\n\n")
        
        with open(test_file_path, 'r', encoding='utf-8') as f:
            test_code = f.read()
        
        prompt_fix_bug = f"""第{fix_bug_times-1}次生成或修复的经过后处理的测试用例如下：
    {test_code}
    该测试用例编译与运行失败，完整编译日志如下：
    {compile_log}
    完整测试日志如下：
    {test_log}
    请根据编译和测试日志，在保持整体结构不变的前提下修复测试用例中的错误。
    """
        print(prompt_fix_bug)
        messages_with_response.append({"role": "user", "content": prompt_fix_bug})

        for attempt in range(max_retries):
            try:
                response = large_model_response(messages_with_response, 0.7)
                messages_with_response.append({"role": "assistant", "content": response})
                break
            except openai.error.RateLimitError as e:
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    wait_time = retry_delay * (attempt + 1)  # 指数退避
                    print(f"⚠️ 遇到速率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("❌ 达到最大重试次数，无法完成请求")
                    return False, fix_bug_times  # 直接返回失败状态和重试次数

        test_file_path, test_file_path_run = save_the_test_cases(response, test_class_name)
        # reflect_private_method_calls(test_file_path, test_class_name, method_signature)
        # add_package_and_import(test_file_path, test_class_name, dependency_classes)
        add_package_and_import_auto(test_file_path, test_class_name, package_info, path)
        compile_result_code, test_result_code, compile_log, test_log = compile_and_run_java(test_file_path, test_file_path_run, test_class_name)
        if compile_result_code == 0 and test_result_code == 0:
            return True, fix_bug_times
        # else:
        #     fix_bug_times += 1
    
    return False, fix_bug_times  # 如果超过最大重试次数，返回失败状态

def re_generate_last_prompt(
                messages,
                pre_process_java_code,
                select,
                test_class_name,
                method_signature,
                dependency_classes,
                path,
                package_info
                ):
    if messages is None:
        messages = []

    re_generate_times = 1
    max_retries = 5
    retry_delay = 10  # 初始等待时间（秒）
    # max_generate_times = 10
    # max_generate_times = 15
    max_generate_times = 30
    
    while re_generate_times <= max_generate_times:
    # while re_generate_times <= 1:
        print(f"$$$$$$$$$$$$$$$$$$第{re_generate_times}次重新生成$$$$$$$$$$$$$$$$$$\n\n")
        for attempt in range(max_retries):
            try:
                # 只重新执行最后一个Prompt
                response = large_model_response(messages, 0.2)
                break
            except openai.error.RateLimitError as e:
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    wait_time = retry_delay * (attempt + 1)  # 指数退避
                    print(f"⚠️ 遇到速率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("❌ 达到最大重试次数，无法完成请求")
                    return False, re_generate_times  # 直接返回失败状态和重试次数

        test_file_path, test_file_path_run = save_the_test_cases(response, test_class_name)
        print("\n\n%%%%%%%%%%%%反射私有方法%%%%%%%%%%%%")
        reflect_private_method_calls(test_file_path, test_class_name, method_signature)
        print("\n\n%%%%%%%%%%%%添加包和导入%%%%%%%%%%%%")
        print("[package_info]:", package_info)
        # covert_T_type(test_file_path, test_class_name, method_signature)
        # add_package_and_import(test_file_path, test_class_name, dependency_classes)
        add_package_and_import_auto(test_file_path, test_class_name, package_info, path)
        compile_result_code, test_result_code, compile_log, test_log = compile_and_run_java(test_file_path, test_file_path_run, test_class_name)
        if compile_result_code == 0 and test_result_code == 0:
            return True, re_generate_times
        else:
            re_generate_times += 1
    
    print("⚠️ 重试已达最大次数")
    return False, re_generate_times  # 如果超过最大重试次数，返回失败状态

def re_generate_all_prompt(pre_process_java_code, java_prompt_synthesis_result, select, test_class_name, method_signature, dependency_classes, path, package_info):

    re_generate_times = 1
    max_retries = 5
    retry_delay = 10  # 初始等待时间（秒）
    # max_generate_times = 10
    max_generate_times = 30
    
    while re_generate_times <= max_generate_times:
    # while re_generate_times <= 1:
        print(f"$$$$$$$$$$$$$$$$$$第{re_generate_times}次重新生成$$$$$$$$$$$$$$$$$$\n\n")
        for attempt in range(max_retries):
            try:
                # 重新执行所有Prompt
                java_generate_test_cases_result, messages, messages_with_response = generate_test_case(
                    pre_process_java_code, java_prompt_synthesis_result, select, test_class_name)
                statement_tests_result = java_generate_test_cases_result[-1]
                response = statement_tests_result
                break
            except openai.error.RateLimitError as e:
                if attempt < max_retries - 1:  # 如果不是最后一次尝试
                    wait_time = retry_delay * (attempt + 1)  # 指数退避
                    print(f"⚠️ 遇到速率限制，等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
                else:
                    print("❌ 达到最大重试次数，无法完成请求")
                    return False, re_generate_times  # 直接返回失败状态和重试次数

        test_file_path, test_file_path_run = save_the_test_cases(response, test_class_name)
        reflect_private_method_calls(test_file_path, test_class_name, method_signature)
        # covert_T_type(test_file_path, test_class_name, method_signature)
        # add_package_and_import(test_file_path, test_class_name, dependency_classes)
        add_package_and_import_auto(test_file_path, test_class_name, package_info, path)
        compile_result_code, test_result_code, compile_log, test_log = compile_and_run_java(test_file_path, test_file_path_run, test_class_name)
        if compile_result_code == 0 and test_result_code == 0:
            return True, re_generate_times
        else:
            re_generate_times += 1
    
    print("⚠️ 重试已达最大次数")
    return False, re_generate_times  # 如果超过最大重试次数，返回失败状态
    
    
    
    
    
