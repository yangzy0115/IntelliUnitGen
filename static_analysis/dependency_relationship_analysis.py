# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 16:41:31 2025

@author: An Wen
"""

import os
import javalang

def is_custom_project_class(name, project_path):
    """
    判断是否是项目自定义类
    - 不能是Java标准库类（以java.或javax.开头）
    - 不能是常见的三方库类（如org.apache.等）
    - 必须是项目中的自定义类
    """
    if not name:
        return False
        
    # 排除Java标准库类
    standard_library_classes = {
        # java.lang 包
        'String', 'Integer', 'Long', 'Double', 'Float', 'Boolean', 'Character', 'Byte', 'Short',
        'Object', 'Class', 'System', 'Thread', 'Runnable', 'Exception', 'Error', 'RuntimeException',
        'IllegalArgumentException', 'IllegalStateException', 'NullPointerException', 'IndexOutOfBoundsException',
        'ArrayIndexOutOfBoundsException', 'ClassCastException', 'NumberFormatException', 'UnsupportedOperationException',
        
        # java.util 包
        'List', 'ArrayList', 'LinkedList', 'Vector', 'Stack', 'Queue', 'Deque', 'PriorityQueue',
        'Map', 'HashMap', 'TreeMap', 'LinkedHashMap', 'WeakHashMap', 'Set', 'HashSet', 'TreeSet',
        'LinkedHashSet', 'Properties', 'Objects', 'Arrays', 'Collections', 'Date', 'Calendar',
        'TimeZone', 'Locale', 'Random', 'UUID', 'Optional',
        
        # java.util.stream 包
        'Stream', 'Collectors', 'IntStream', 'LongStream', 'DoubleStream',
        
        # java.io 包
        'File', 'InputStream', 'OutputStream', 'Reader', 'Writer', 'BufferedReader', 'BufferedWriter',
        'FileInputStream', 'FileOutputStream', 'FileReader', 'FileWriter',
        
        # java.nio 包
        'Path', 'Paths', 'Files', 'DirectoryStream', 'WatchService',
        
        # java.net 包
        'URL', 'URLConnection', 'HttpURLConnection', 'Socket', 'ServerSocket', 'DatagramSocket',
        'InetAddress', 'InetSocketAddress'
    }
    
    if name in standard_library_classes:
        return False
        
    # 排除Java标准库包
    if name.startswith('java.') or name.startswith('javax.'):
        return False
        
    # 排除常见的三方库类
    common_third_party_prefixes = [
        'org.apache.', 'org.springframework.', 'org.junit.',
        'com.google.', 'com.fasterxml.', 'com.sun.',
        'net.sf.', 'io.netty.', 'ch.qos.'
    ]
    for prefix in common_third_party_prefixes:
        if name.startswith(prefix):
            return False

    # 获取项目中的所有Java文件路径
    java_files = []
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                java_files.append(os.path.join(root, file))

    # 将类名转换为可能的文件名
    possible_filenames = [
        name + '.java',  # 简单类名
        name.replace('.', os.sep) + '.java'  # 完整包路径
    ]

    # 检查是否存在对应的Java文件
    for java_file in java_files:
        file_name = os.path.basename(java_file)
        if file_name in possible_filenames:
            print(f"找到匹配的类文件: {java_file} 对应类名: {name}")
            return True

    # 如果找不到对应的文件，但类名符合Java命名规范（首字母大写），也认为是项目类
    if name[0].isupper() and not any(c.isupper() for c in name[1:]):
        print(f"类名 {name} 符合Java命名规范，认为是项目类")
        return True

    return False

def extract_class_info_from_java_code(java_code, project_path):
    dependencies_dict = {}
    method_signatures = {}

    try:
        print("\n尝试解析Java代码...")
        print("代码前200字符:", java_code[:200])
        tree = javalang.parse.parse(java_code)
        print("✅ javalang解析成功")
        print("解析树类型:", type(tree))
        
        # 遍历所有顶级声明
        found_types = False
        for type_decl in tree.types:
            if isinstance(type_decl, (javalang.tree.ClassDeclaration, 
                                    javalang.tree.InterfaceDeclaration, 
                                    javalang.tree.EnumDeclaration)):
                found_types = True
                class_name = type_decl.name
                print(f"\n发现声明: {class_name} ({type(type_decl).__name__})")
                dependencies = set()
                methods = []

                # 提取构造函数
                for constructor in type_decl.constructors:
                    parameters = []
                    for param in constructor.parameters:
                        param_type = param.type.name
                        param_name = param.name
                        parameters.append(f"{param_type} {param_name}")
                    param_str = ', '.join(parameters)
                    if constructor.modifiers:
                        access_mod = next((m for m in ['public', 'private', 'protected'] if m in constructor.modifiers), 'default')
                    else:
                        access_mod = 'default'
                    signature = f"{access_mod} {class_name}({param_str})"
                    print(f"  发现构造函数: {signature}")
                    methods.append(signature)

                # 提取成员变量依赖
                for field in type_decl.fields:
                    if hasattr(field.type, 'name'):
                        dep_name = field.type.name
                        if is_custom_project_class(dep_name, project_path):
                            print(f"  发现字段依赖: {dep_name}")
                            dependencies.add(dep_name)

                # 提取构造函数new出来的对象
                for _, creator in type_decl.filter(javalang.tree.ClassCreator):
                    if hasattr(creator.type, 'name'):
                        typename = creator.type.name
                        if is_valid_dependency(typename) and is_custom_project_class(typename, project_path):
                            print(f"  发现构造函数依赖: {typename}")
                            dependencies.add(typename)

                # 提取方法调用中对象类型
                for _, method_inv in type_decl.filter(javalang.tree.MethodInvocation):
                    if method_inv.qualifier:
                        qualifier = method_inv.qualifier.strip()
                        if is_valid_dependency(qualifier) and is_custom_project_class(qualifier, project_path):
                            print(f"  发现方法调用依赖: {qualifier}")
                            dependencies.add(qualifier)

                # 提取本类/接口/枚举中的方法签名
                for method in type_decl.methods:
                    method_name = method.name
                    parameters = []
                    for param in method.parameters:
                        param_type = param.type.name
                        param_name = param.name
                        parameters.append(f"{param_type} {param_name}")
                    param_str = ', '.join(parameters)
                    if method.modifiers:
                        access_mod = next((m for m in ['public', 'private', 'protected'] if m in method.modifiers), 'default')
                    else:
                        access_mod = 'default'
                    signature = f"{access_mod} {method.return_type.name if method.return_type else 'void'} {method_name}({param_str})"
                    print(f"  发现方法: {signature}")
                    methods.append(signature)

                method_signatures[class_name] = methods
                dependencies_dict[class_name] = list(dependencies)
                print(f"  为 {class_name} 收集到 {len(dependencies)} 个依赖和 {len(methods)} 个方法")

        if not found_types:
            print("⚠️ 警告：未在代码中发现任何类、接口或枚举声明")
            print("尝试打印所有顶级声明:")
            for type_decl in tree.types:
                print(f"发现节点: {type(type_decl)}")

    except Exception as e:
        print(f"⚠️ 解析失败，跳过。错误信息：{e}")
        print("源码片段：", java_code[:200])

    return dependencies_dict, method_signatures

def is_valid_dependency(name):
    """
    判断是否是合理的依赖类名
    - 必须首字母大写
    - 不能是单个小写字母（比如 o、p、e）
    """
    if not name:
        return False
    if len(name) == 1 and name.islower():
        return False
    if not name[0].isupper():
        return False
    return True

def read_file_with_encoding(file_path):
    """尝试使用不同的编码读取文件"""
    encodings = ['utf-8', 'gbk', 'gb2312', 'latin1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                print(f"✅ 成功使用 {encoding} 编码读取文件")
                return content
        except UnicodeDecodeError:
            print(f"❌ {encoding} 编码读取失败")
            continue
    
    # 如果所有编码都失败，使用二进制模式读取
    print("⚠️ 所有编码尝试失败，使用二进制模式读取")
    with open(file_path, 'rb') as f:
        return f.read().decode('utf-8', errors='ignore')

def analyze_project_java_files(project_path):
    """分析项目中的所有Java文件，提取依赖关系和函数签名"""
    all_dependency_result = {}  # 字典，key是类名，value是依赖列表
    all_fun_signature = {}  # 改为字典，key是类名，value是方法签名列表
    
    print("\n开始分析项目依赖...")
    print(f"项目路径: {project_path}")
    
    java_files_found = 0
    java_files_processed = 0
    
    # 遍历项目目录
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                java_files_found += 1
                file_path = os.path.join(root, file)
                print(f"\n正在处理文件 ({java_files_found}): {file_path}")
                try:
                    # 使用新的文件读取函数
                    java_code = read_file_with_encoding(file_path)
                    
                    # 提取依赖关系
                    dependencies, method_signatures = extract_class_info_from_java_code(java_code, project_path)
                    
                    if dependencies:
                        print(f"发现依赖关系: {dependencies}")
                    if method_signatures:
                        print(f"发现方法签名: {method_signatures}")
                    
                    # 合并依赖关系
                    for class_name, deps in dependencies.items():
                        if class_name in all_dependency_result:
                            all_dependency_result[class_name].extend(deps)
                        else:
                            all_dependency_result[class_name] = deps
                    
                    # 合并方法签名
                    for class_name, methods in method_signatures.items():
                        if class_name in all_fun_signature:
                            all_fun_signature[class_name].extend(methods)
                        else:
                            all_fun_signature[class_name] = methods
                    
                    java_files_processed += 1
                            
                except Exception as e:
                    print(f"处理文件 {file_path} 时出错: {str(e)}")
                    continue
    
    print("\n分析完成!")
    print(f"找到 {java_files_found} 个Java文件")
    print(f"成功处理 {java_files_processed} 个Java文件")
    print(f"总共发现 {len(all_dependency_result)} 个类的依赖关系")
    print(f"总共发现 {len(all_fun_signature)} 个类的方法签名")
    
    return all_dependency_result, all_fun_signature

# def main():
#     project_dir = input("请输入项目目录路径：").strip()
#     dependencies, methods = analyze_project_java_files(project_dir)

#     print("\n📋 分析结果：")

#     for class_name, deps in dependencies.items():
#         print(f"\n【类】{class_name} 的依赖：")
#         for dep in deps:
#             print(f"  - {dep}")

#         print(f"【{class_name}】自身的方法：")
#         if class_name in methods:
#             for sig in methods[class_name]:
#                 print(f"    - {sig}")
#         else:
#             print("    - 无方法定义")

#     print("\n📋 被依赖类的方法提取结果：")
#     for class_name, sigs in methods.items():
#         if class_name not in dependencies:
#             continue
#         print(f"\n依赖类【{class_name}】的方法签名：")
#         for sig in sigs:
#             print(f"  - {sig}")

# if __name__ == "__main__":
#     main()
