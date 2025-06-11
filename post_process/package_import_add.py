import os
import re

# Java 标准类/关键字映射到 import 的映射表（可根据需要扩展）
JAVA_IMPORT_MAP = {
    # Collections
    "List": "java.util.*",
    "ArrayList": "java.util.ArrayList",
    "LinkedList": "java.util.LinkedList",
    "Vector": "java.util.Vector",
    "Stack": "java.util.Stack",
    "Queue": "java.util.Queue",
    "Deque": "java.util.Deque",
    "PriorityQueue": "java.util.PriorityQueue",
    "Map": "java.util.Map",
    "HashMap": "java.util.HashMap",
    "TreeMap": "java.util.TreeMap",
    "LinkedHashMap": "java.util.LinkedHashMap",
    "WeakHashMap": "java.util.WeakHashMap",
    "Set": "java.util.Set",
    "HashSet": "java.util.HashSet",
    "TreeSet": "java.util.TreeSet",
    "LinkedHashSet": "java.util.LinkedHashSet",
    "Properties": "java.util.Properties",
    "Objects": "java.util.Objects",
    
    # Functional Interfaces
    "Consumer": "java.util.function.Consumer",
    "Supplier": "java.util.function.Supplier",
    "Function": "java.util.function.Function",
    "Predicate": "java.util.function.Predicate",
    "BiFunction": "java.util.function.BiFunction",
    "BiConsumer": "java.util.function.BiConsumer",
    "BiPredicate": "java.util.function.BiPredicate",
    "UnaryOperator": "java.util.function.UnaryOperator",
    "BinaryOperator": "java.util.function.BinaryOperator",
    
    # Reflection
    "Array": "java.lang.reflect.Array",
    "Method": "java.lang.reflect.Method",
    "Field": "java.lang.reflect.Field",
    "Constructor": "java.lang.reflect.Constructor",
    "Modifier": "java.lang.reflect.Modifier",
    "Proxy": "java.lang.reflect.Proxy",
    "InvocationTargetException": "java.lang.reflect.InvocationTargetException",
    # "IllegalAccessException": "java.lang.reflect.IllegalAccessException",
    # "NoSuchMethodException": "java.lang.reflect.NoSuchMethodException",
    # "NoSuchFieldException": "java.lang.reflect.NoSuchFieldException",
    
    # IO & NIO
    "FileInputStream": "java.io.FileInputStream",
    "FileOutputStream": "java.io.FileOutputStream",
    "BufferedReader": "java.io.BufferedReader",
    "BufferedWriter": "java.io.BufferedWriter",
    "FileReader": "java.io.FileReader",
    "FileWriter": "java.io.FileWriter",
    "InputStream": "java.io.InputStream",
    "OutputStream": "java.io.OutputStream",
    "Reader": "java.io.Reader",
    "StringBuffer": "java.io.StringReader",
    
    "Writer": "java.io.Writer",
    "File": "java.io.File",
    "Path": "java.nio.file.Path",
    "Paths": "java.nio.file.*",
    "Files": "java.nio.file.Files",
    "DirectoryStream": "java.nio.file.DirectoryStream",
    "WatchService": "java.nio.file.WatchService",
    
    # Networking
    "URL": "java.net.URL",
    "URLConnection": "java.net.URLConnection",
    "HttpURLConnection": "java.net.HttpURLConnection",
    "Socket": "java.net.Socket",
    "ServerSocket": "java.net.ServerSocket",
    "DatagramSocket": "java.net.DatagramSocket",
    "InetAddress": "java.net.InetAddress",
    "InetSocketAddress": "java.net.InetSocketAddress",
    
    # Utilities
    "Arrays": "java.util.Arrays",
    "Collections": "java.util.Collections",
    "Date": "java.util.Date",
    "Calendar": "java.util.Calendar",
    "TimeZone": "java.util.TimeZone",
    "Locale": "java.util.Locale",
    "Random": "java.util.Random",
    "UUID": "java.util.UUID",
    "Optional": "java.util.Optional",
    "Stream": "java.util.stream.Stream",
    "Collectors": "java.util.stream.Collectors",
    
    # Exceptions
    "IOException": "java.io.IOException",
    "FileNotFoundException": "java.io.FileNotFoundException",
    "IllegalStateException": "java.lang.IllegalStateException",
    "IllegalArgumentException": "java.lang.IllegalArgumentException",
    "NullPointerException": "java.lang.NullPointerException",
    "IndexOutOfBoundsException": "java.lang.IndexOutOfBoundsException",
    "ArrayIndexOutOfBoundsException": "java.lang.ArrayIndexOutOfBoundsException",
    "ClassCastException": "java.lang.ClassCastException",
    "NumberFormatException": "java.lang.NumberFormatException",
    "UnsupportedOperationException": "java.lang.UnsupportedOperationException",
    "ConcurrentModificationException": "java.util.ConcurrentModificationException",
    "InvalidPathException": "java.nio.file.InvalidPathException",
    "MalformedURLException": "java.net.MalformedURLException",
    "InterruptedException": "java.lang.InterruptedException",
    "CloneNotSupportedException": "java.lang.CloneNotSupportedException",
    
    # Built-in types (no import needed)
    "System.out": None,
    "System.err": None,
    "String": None,
    "long": None,
    "int": None,
    "boolean": None,
    "char": None,
    "byte": None,
    "short": None,
    "float": None,
    "double": None,
    "void": None
}

def add_package_and_import(test_file_path, test_class_name, dependency_classes=None):
    """
    添加 package 声明 + 自动根据依赖类添加 import 语句
    """
    # 自动推导包名（从 java/ 之后的目录结构构造）
    path_parts = test_file_path.replace("\\", "/").split('/')
    if "java" not in path_parts:
        print("[错误] 无法从路径中推断包名：路径中不包含 'java'")
        return

    java_index = path_parts.index("java")
    package_parts = path_parts[java_index + 1:-1]  # 去掉 'java' 和文件名部分
    package_name = ".".join(package_parts)

    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 检查是否已有 package 声明
    # has_package = any(line.strip().startswith("package ") for line in lines)
    updated_lines = []
    # if not has_package:
    #     # 添加 package 声明
    #     package_line = f"package {package_name};\n\n"
    #     updated_lines.append(package_line)
    #     print(f"[完成] 添加 package 声明：{package_line.strip()}")

    # 添加 import 语句（若提供了 dependency_classes）
    if dependency_classes:
        imports = set()
        for cls in dependency_classes:
            full_import = JAVA_IMPORT_MAP.get(cls)
            if full_import:
                imports.add(f"import {full_import};\n")
        if imports:
            updated_lines.extend(sorted(imports))
            updated_lines.append("\n")
            print(f"[完成] 添加 {len(imports)} 个 import 语句。")
        else:
            print("[提示] 未添加任何 import 语句。")

    # 添加原始内容
    updated_lines.extend(lines)

    # 写回文件
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

def extract_types_from_code(java_code):
    """
    从 Java 源码中提取所有可能的类型名，包括内部类
    """
    # 匹配大写字母开头的单词（类名/接口名/泛型等）
    type_pattern = re.compile(r'\b([A-Z][A-Za-z0-9_]*)\b')
    # 匹配内部类引用（如 AbstractHelpFormatter.Builder）
    inner_class_pattern = re.compile(r'\b([A-Z][A-Za-z0-9_]*)\.([A-Z][A-Za-z0-9_]*)\b')
    
    # 排除 Java 关键字和常用类型
    exclude = {
        'public', 'private', 'protected', 'class', 'interface', 'enum', 'void', 'static', 'final', 'abstract',
        'return', 'if', 'else', 'for', 'while', 'switch', 'case', 'break', 'continue', 'try', 'catch', 'finally',
        'new', 'extends', 'implements', 'throws', 'throw', 'import', 'package', 'true', 'false', 'null', 'this', 'super',
        'Test', 'Override'
    }
    
    # 提取所有类型名
    types = set()
    inner_classes = {}  # 存储内部类信息 {inner_class_name: outer_class_name}
    
    # 提取内部类引用
    for match in inner_class_pattern.finditer(java_code):
        outer_class, inner_class = match.groups()
        if outer_class not in exclude and inner_class not in exclude:
            inner_classes[inner_class] = outer_class
            types.add(inner_class)  # 只添加内部类名
    
    # 提取普通类名
    for match in type_pattern.finditer(java_code):
        name = match.group(1)
        if name not in exclude and name not in inner_classes:  # 避免重复添加内部类
            types.add(name)
    
    return types, inner_classes

def add_package_and_import_auto(test_file_path, test_class_name, package_info, path):
    """
    自动扫描源码提取类型名并补全 import，处理项目中的类和同名类冲突
    
    Args:
        test_file_path: 测试文件路径
        test_class_name: 测试类名
        package_info: 项目包信息字典 {package_name: [class_names]}
        path: 被测试类的路径，用于解决同名类冲突
    """
    # 自动推导包名
    path_parts = test_file_path.replace("\\", "/").split('/')
    if "java" not in path_parts:
        print("[错误] 无法从路径中推断包名：路径中不包含 'java'")
        return

    java_index = path_parts.index("java")
    package_parts = path_parts[java_index + 1:-1]
    package_name = ".".join(package_parts)

    # 获取被测试类的包名
    test_class_package = None
    # 从path中提取被测试类的包名
    path_parts = path.replace("\\", "/").split('/')
    if "java" in path_parts:
        java_index = path_parts.index("java")
        test_package_parts = path_parts[java_index + 1:-1]  # 去掉 'java' 和文件名部分
        test_class_package = ".".join(test_package_parts)
        print(f"[调试] 被测试类的包名：{test_class_package}")

    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    code = "".join(lines)

    # 检查是否已有 package 声明
    has_package = any(line.strip().startswith("package ") for line in lines)
    updated_lines = []
    
    # 保留 package 声明
    package_line = None
    for line in lines:
        if line.strip().startswith("package "):
            package_line = line
            break
    
    if package_line:
        updated_lines.append(package_line)
        updated_lines.append("\n")
    elif not has_package:
        package_line = f"package {package_name};\n\n"
        updated_lines.append(package_line)
        print(f"[完成] 添加 package 声明：{package_line.strip()}")

    # 提取所有类型名和内部类信息
    types, inner_classes = extract_types_from_code(code)
    # 移除当前测试类名
    print(f"[调试] 当前测试类名：{test_class_name}")
    types.discard(test_class_name.replace('.java', ''))
    print(f"[调试] 从代码中提取到的类型：{sorted(types)}")
    if inner_classes:
        print(f"[调试] 发现的内部类：{inner_classes}")

    # 提取已 import 的类型，避免重复
    imported_types = set()
    existing_imports = []
    for line in lines:
        if line.strip().startswith("import "):
            imported = line.strip().split()[-1].split('.')[-1].replace(';', '')
            imported_types.add(imported)
            existing_imports.append(line)
    
    print(f"[调试] 已导入的类型：{sorted(imported_types)}")

    # 需要 import 的类型
    need_import = set()
    
    # 处理每个类型
    for t in types:
        if t in imported_types:
            continue
            
        # 检查是否是内部类
        if t in inner_classes:
            outer_class = inner_classes[t]
            # 查找外部类所在的包
            found_outer = False
            for pkg, classes in package_info.items():
                # 跳过当前测试类所在的包
                if pkg == package_name:
                    continue
                if outer_class in classes:
                    found_outer = True
                    need_import.add(f"import {pkg}.{outer_class};\n")
                    print(f"[调试] 导入内部类的外部类：{outer_class} -> {pkg}.{outer_class}")
                    break
            if found_outer:
                continue  # 跳过内部类的单独导入
            
        # 检查是否是项目中的类
        found_in_project = False
        target_package = None
        
        # 首先检查被测试类的包中是否有这个类（排除当前测试类所在的包）
        if test_class_package and test_class_package in package_info and test_class_package != package_name:
            if t in package_info[test_class_package]:
                found_in_project = True
                target_package = test_class_package
                print(f"[调试] 在被测试类包中找到类：{t} -> {target_package}")
        
        # 如果没找到，检查其他包（排除当前测试类所在的包）
        if not found_in_project:
            for pkg, classes in package_info.items():
                # 跳过当前测试类所在的包
                if pkg == package_name:
                    continue
                if t in classes:
                    found_in_project = True
                    target_package = pkg
                    print(f"[调试] 在其他包中找到类：{t} -> {target_package}")
                    break
        
        if found_in_project and target_package:
            need_import.add(f"import {target_package}.{t};\n")
            print(f"[调试] 导入类：{t} -> {target_package}.{t}")
        # 如果不是项目中的类，检查是否是标准库/第三方库的类
        elif t in JAVA_IMPORT_MAP and JAVA_IMPORT_MAP[t]:
            need_import.add(f"import {JAVA_IMPORT_MAP[t]};\n")
            print(f"[调试] 导入标准库/第三方库类：{t} -> {JAVA_IMPORT_MAP[t]}")

    # 添加所有 import 语句（先添加新的，再添加原有的）
    if need_import:
        updated_lines.extend(sorted(need_import))
        updated_lines.append("\n")
        print(f"[完成] 自动添加 {len(need_import)} 个 import 语句。")
    
    # 添加原有的 import 语句
    if existing_imports:
        updated_lines.extend(existing_imports)
        updated_lines.append("\n")
        print(f"[完成] 保留 {len(existing_imports)} 个原有 import 语句。")

    # 添加其他内容（跳过 package 和 import 语句）
    for line in lines:
        if not (line.strip().startswith("package ") or line.strip().startswith("import ")):
            updated_lines.append(line)

    # 添加许可证
    updated_lines = add_license(updated_lines)

    # 写回文件
    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

def add_license(updated_lines):
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

    # Join the list of lines into a single string, then prepend the license
    return [apache_license + "\n"] + updated_lines

# 示例用法
if __name__ == "__main__":
    # 使用正斜杠的路径，并确保文件存在
    # test_file_path = "E:/YAU_BIT/Research/Project Implementation/Project1/Sub-project 2/Sub-project 2.1/Sub-project 2.1.1/Now/Experiment/0429_commons-cli-master_all/src/test/java/org/apache/commons/cli/CommandLineTest.java"
    test_file_path = (r"E:/YAU_BIT/Research/Project Implementation/Project1/Sub-project 2/Sub-project 2.1/"
                     r"Sub-project 2.1.1/Now/Experiment/0516_commons-cli-master_all/src/test/java/org/apache/"
                     r"commons/cli/CommandLineTest.java")
    path = (
        r"E:\YAU_BIT\Research\Project Implementation\Project1"
        r"\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1"
        r"\Now\Experiment\0516_commons-cli-master_all"
    )
    if not os.path.exists(test_file_path):
        print(f"[错误] 文件不存在：{test_file_path}")
        exit(1)
        
    # test_class_name = "TextHelpAppendableTest"  # Updated to match the test file path
    test_class_name = "CommandLineTest"
    package_info = {
        'org.apache.commons.cli': [
            'CommandLine', 'Option', 'Options', 'Parser', 'ParseException',
            'HelpFormatter', 'OptionGroup', 'OptionBuilder', 'TypeHandler',
            'Util', 'DefaultParser', 'BasicParser', 'GnuParser', 'PosixParser',
            'PatternOptionBuilder', 'OptionValidator', 'OptionComparator',
            'MissingArgumentException', 'MissingOptionException',
            'UnrecognizedOptionException', 'AmbiguousOptionException',
            'AlreadySelectedException', 'DeprecatedAttributes'
        ],
        'org.apache.commons.cli.help': [
            'AbstractHelpFormatter', 'TextHelpAppendable', 'FilterHelpAppendable',
            'HelpFormatter', 'OptionFormatter', 'TextStyle', 'Util',
            'Builder', 'ConcreteHelpAppendable', 'HelpAppendableImpl'
        ]
    }
    
    # 获取项目包信息
    project_path = (
        r"E:\YAU_BIT\Research\Project Implementation\Project1"
        r"\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1"
        r"\Now\Experiment\0516_commons-cli-master_all"
    )

    # package_info = get_project_classes(project_path)
    
    print("[开始] 执行自动添加 import 语句...")
    add_package_and_import(test_file_path, test_class_name, package_info)
    add_package_and_import_auto(test_file_path, test_class_name, package_info, path)