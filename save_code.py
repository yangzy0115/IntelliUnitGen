# -*- coding: utf-8 -*-
"""
Created on Sun Apr  6 10:13:27 2025

@author: An Wen
"""

import re
import os
import sys
import tkinter as tk
from tkinter import filedialog


# === 模块级路径变量 ===
save_base_dir = None
run_base_dir = None

# === 路径选择函数 ===
def set_global_paths():
    global save_base_dir, run_base_dir

    root = tk.Tk()
    root.withdraw()

    save_base_dir = filedialog.askdirectory(title="请选择 Java 测试代码保存路径")
    if not save_base_dir:
        print("❌ 未选择保存路径，程序终止")
        sys.exit()

    run_base_dir = filedialog.askdirectory(title="请选择项目运行路径（用于编译）")
    if not run_base_dir:
        print("❌ 未选择运行路径，程序终止")
        sys.exit()

    print(f"✅ 保存路径: {save_base_dir}")
    print(f"✅ 编译路径: {run_base_dir}")

# === 路径获取函数 ===
def get_test_file_path(test_class_name):
    global save_base_dir, run_base_dir

    if save_base_dir is None or run_base_dir is None:
        print("❗ 未设置保存路径，请先调用 set_global_paths()")
        sys.exit()

    test_file_dir = save_base_dir
    test_file_dir_run = run_base_dir

    test_file_path = os.path.join(test_file_dir, test_class_name)
    test_file_path_run = os.path.join(test_file_dir_run, test_class_name)

    os.makedirs(test_file_dir, exist_ok=True)
    return test_file_dir, test_file_path, test_file_path_run


def extract_java_code(statement_tests):
    match = re.search(r"```(?:java)?\s*(.*?)```", statement_tests, re.DOTALL)
    if match:
        return match.group(1).strip()
    else:
        print("❗ 未找到 Java 代码块。")
        return ""
    
def save_java_test(statement_tests, test_class_name):
    # print("save_java_testsave_java_testsave_java_testsave_java_test")
    """
    解析并保存 Java 测试代码，确保加入 Apache 许可证头。
    """
    print("============================解析并保存 Java 测试代码 ===========================")
    test_file_dir, test_file_path, test_file_path_run = get_test_file_path(test_class_name)
    
    # print("test_file_pathtest_file_pathtest_file_pathtest_file_path", test_file_path)
    
    # **确保只保存 Java 代码**
    java_code_cleaned = extract_java_code(statement_tests)  # 只提取 Java 代码部分
    print("========================java_code_cleaned=================================")
    print(java_code_cleaned)

    # **Apache 许可证头**
    apache_license = """/*
 * Licensed to the Apache Software Foundation (ASF) under one or more
 * contributor license agreements. See the NOTICE file distributed with
 * this work for additional information regarding copyright ownership.
 * The ASF licenses this file to You under the Apache License, Version 2.0
 * (the "License"); you may not use this file except in compliance with
 * the License. You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
"""

    # **确保最终保存的 Java 代码带有许可证**
    final_java_code = apache_license + "\n" + java_code_cleaned
    print("=======================final_java_code==================================")
    print(final_java_code)

    # **确保目录存在**
    os.makedirs(test_file_dir, exist_ok=True)

    # **写入文件**
    try:
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(final_java_code)  # 仅保存提取出的 Java 代码，并添加许可证
        print(f"✅ JUnit 测试代码已成功保存到 {test_file_path}")
    except Exception as e:
        print(f"❌ 保存测试代码失败: {e}")
        
    return test_file_path, test_file_path_run


def save_the_test_cases(statement_tests, test_class_name):
    test_file_path, test_file_path_run = save_java_test(statement_tests, test_class_name)
    return test_file_path, test_file_path_run




# def get_test_file_path(test_class_name):
#     """生成并返回测试文件路径（使用相对路径，基于 Now 目录）"""

#     # 当前工作目录，适用于交互环境
#     current_dir = os.getcwd()

#     # 回到 Now 目录（假设当前目录是 Now/Code 或其下）
#     now_dir = os.path.abspath(os.path.join(current_dir, ".."))

#     # 拼接目标路径
#     test_file_dir = os.path.join(
#         now_dir,
#         "Experiment",
#         "commons-cli-master",
#         "commons-cli-master （statement_coverage）",
#         "src", "test", "java", "org", "apache", "commons", "cli"
#     )
    
#     test_file_dir_run = os.path.join(
#         now_dir,
#         "Experiment",
#         "commons-cli-master",
#         "commons-cli-master （statement_coverage）"
#     )

#     test_file_path = os.path.join(test_file_dir, test_class_name)
#     test_file_path_run = os.path.join(test_file_dir_run, test_class_name)

#     os.makedirs(test_file_dir, exist_ok=True)

#     return test_file_dir, test_file_path, test_file_path_run




    