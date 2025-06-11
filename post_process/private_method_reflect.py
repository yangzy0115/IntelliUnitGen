import re

JAVA_TYPE_MAP = {
    "int": "int.class",
    "boolean": "boolean.class",
    "char": "char.class",
    "byte": "byte.class",
    "short": "short.class",
    "long": "long.class",
    "float": "float.class",
    "double": "double.class",
    "String": "String.class"
}

def add_invocation_target_exception_import(test_file_path):
    """
    在 Java 测试类文件中添加 import java.lang.reflect.InvocationTargetException; 语句
    如果已经存在则不重复添加。
    """
    import_line = "import java.lang.reflect.InvocationTargetException;\n"

    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 如果已包含该 import，直接返回
    if any("import java.lang.reflect.InvocationTargetException;" in line for line in lines):
        print("✅ 已存在 import InvocationTargetException，跳过添加。")
        return

    # 找到第一个非 package 且是 import 的位置后插入
    insert_index = 0
    for i, line in enumerate(lines):
        if line.strip().startswith("import "):
            insert_index = i + 1
        elif line.strip().startswith("public class") or line.strip().startswith("@"):
            break

    lines.insert(insert_index, import_line)

    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    print("✅ 已添加 import java.lang.reflect.InvocationTargetException;")

def add_throws_to_reflection_tests(test_file_path):
    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    updated_lines = []
    reflection_exceptions = [
        "NoSuchMethodException",
        "IllegalAccessException",
        "InvocationTargetException"
    ]

    inside_method = False
    for i, line in enumerate(lines):
        stripped = line.strip()

        # 记录 @Test 标签，准备进入方法
        if stripped.startswith("@Test"):
            inside_method = True
            updated_lines.append(line)
            continue

        # 找到测试方法定义
        if inside_method and re.match(r'\s*public\s+void\s+\w+\s*\(', stripped):
            inside_method = False

            # 检查是否已有 throws
            if "throws" in line:
                match = re.search(r'throws\s+([^ {]+)', line)
                if match:
                    existing = [e.strip() for e in match.group(1).split(',')]
                    all_throws = sorted(set(existing + reflection_exceptions))
                    line = re.sub(r'throws\s+[^ {]+', f"throws {', '.join(all_throws)}", line)
            else:
                # 没有 throws 子句，直接插入
                line = line.rstrip().rstrip("{") + f" throws {', '.join(reflection_exceptions)} {{\n"

        updated_lines.append(line)

    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("✅ 已在方法签名中添加反射异常的 throws 子句。")

def extract_param_types(signature):
    param_list = re.search(r'\((.*?)\)', signature)
    if not param_list:
        return []
    params = param_list.group(1).strip()
    if not params:
        return []
    param_types = []
    for param in params.split(','):
        param = param.strip()
        if ' ' in param:
            type_part = param.split()[0]
        else:
            type_part = param
        java_class_type = JAVA_TYPE_MAP.get(type_part, f"{type_part}.class")
        param_types.append(java_class_type)
    return param_types

def extract_object_and_assignment(line, method_name):
    # 检查是否是静态方法调用
    static_match = re.search(r'(\w+)\s*\.\s*' + re.escape(method_name) + r'\s*\(', line)
    if static_match:
        obj = static_match.group(1)
        # 如果是静态方法调用，返回类名作为对象
        return obj, None, None, None
    
    # 处理实例方法调用
    obj_match = re.search(r'(\w+)\s*\.\s*' + re.escape(method_name) + r'\s*\(', line)
    lhs_match = re.match(r'\s*(\w[\w\s<>]*?)\s+(\w+)\s*=\s*', line)
    obj = obj_match.group(1) if obj_match else "null"
    lhs = lhs_match.group(0).strip() if lhs_match else None
    lhs_type = lhs_match.group(1).strip() if lhs_match else None
    lhs_var = lhs_match.group(2).strip() if lhs_match else None
    return obj, lhs, lhs_type, lhs_var

def extract_method_info(signature):
    """
    从方法签名中提取方法名、参数类型和访问修饰符
    返回: (method_name, param_types, access_modifier, raw_signature)
    """
    # 匹配访问修饰符、返回类型、方法名和参数列表
    match = re.match(r'(private|public|protected|default)\s+([^\s]+)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)', signature)
    if not match:
        return None
    
    access_modifier, return_type, method_name, params = match.groups()
    param_types = []
    
    # 处理参数类型
    if params.strip():
        for param in params.split(','):
            param = param.strip()
            if ' ' in param:
                type_part = param.split()[0]
            else:
                type_part = param
            param_types.append(type_part)
    
    return method_name, param_types, access_modifier, signature

def rewrite_private_method_calls(test_file_path, test_class_name, method_signature):
    private_methods = {}  # method_name -> [(class_name, param_types, raw_signature), ...]
    
    # 收集所有私有方法，按方法名分组
    for class_name, methods in method_signature.items():
        for method in methods:
            method_info = extract_method_info(method)
            if method_info and method_info[2] == 'private':  # 只处理private方法
                method_name, param_types, _, signature = method_info
                if method_name not in private_methods:
                    private_methods[method_name] = []
                private_methods[method_name].append((class_name, param_types, signature))

    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified_lines = []
    method_counter = 1
    already_imported_method = any("import java.lang.reflect.Method;" in line for line in lines)
    inserted_import = False
    inside_test_method = False
    current_method_counter = 0

    for i, line in enumerate(lines):
        if not already_imported_method and re.match(r'\s*import ', line) and not inserted_import:
            modified_lines.append("import java.lang.reflect.Method;\n")
            inserted_import = True

        # 检测是否进入新的测试方法
        if line.strip().startswith("@Test"):
            inside_test_method = True
            current_method_counter = 0
            modified_lines.append(line)
            continue

        # 检测是否离开测试方法
        if inside_test_method and re.match(r'\s*public\s+void\s+\w+\s*\(', line):
            inside_test_method = False

        matched = False
        # 匹配方法调用
        method_call_match = re.search(r'(\w+)\s*\.\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)', line)
        if method_call_match:
            obj_var, method_name, args_str = method_call_match.groups()
            
            # 如果这个方法名在私有方法列表中
            if method_name in private_methods:
                # 提取实际参数类型
                args = [arg.strip() for arg in args_str.split(',')] if args_str.strip() else []
                
                # 尝试匹配最合适的方法签名
                best_match = None
                for class_name, param_types, signature in private_methods[method_name]:
                    # 检查参数数量是否匹配
                    if len(args) == len(param_types):
                        # 这里可以添加更复杂的参数类型匹配逻辑
                        # 目前简单实现：如果参数数量匹配，就认为找到了匹配的方法
                        best_match = (class_name, param_types, signature)
                        break
                
                if best_match:
                    matched = True
                    class_name, param_types, signature = best_match
                    indent = re.match(r'\s*', line).group(0)
                    param_class_list = ", ".join(JAVA_TYPE_MAP.get(pt, f"{pt}.class") for pt in param_types)
                    obj_var, lhs, lhs_type, lhs_var = extract_object_and_assignment(line, method_name)

                    # 注释原始行
                    modified_lines.append(f"{indent}// {line.lstrip()}")

                    # 为每个测试方法创建新的 method 变量
                    current_method_counter += 1
                    method_var = f"method{current_method_counter}"
                    modified_lines.append(f"{indent}Method {method_var} = {class_name}.class.getDeclaredMethod(\"{method_name}\"{', ' if param_class_list else ''}{param_class_list});\n")
                    modified_lines.append(f"{indent}{method_var}.setAccessible(true); // 绕过私有限制\n")

                    # 获取返回类型（用于强转）
                    return_type_match = re.match(r'\s*private\s+([^\s<]+)', signature.strip())
                    return_type = return_type_match.group(1) if return_type_match else "Object"

                    # 提取调用表达式完整片段与参数部分
                    call_match = re.search(r'(' + re.escape(obj_var) + r'\s*\.\s*' + re.escape(method_name) + r'\s*\((.*?)\))', line)
                    if call_match:
                        full_call_str = call_match.group(1)
                        arg_expr_str = call_match.group(2).strip()
                        arg_list = [e.strip() for e in arg_expr_str.split(',')] if arg_expr_str else []
                        
                        # 对于静态方法，第一个参数是 null
                        if obj_var == class_name:  # 静态方法调用
                            final_args = ", ".join(["null"] + arg_list)
                        else:  # 实例方法调用
                            final_args = ", ".join([obj_var] + arg_list)
                            
                        reflect_call = f"({return_type}) {method_var}.invoke({final_args})"
                        new_line = line.replace(full_call_str, reflect_call)
                        modified_lines.append(new_line)
                    else:
                        # fallback：未匹配完整表达式
                        modified_lines.append(f"{indent}// 替换失败，请手动处理\n")
                        modified_lines.append(line)

        if not matched:
            modified_lines.append(line)

    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(modified_lines)

    print("✅ 处理完成：每个测试方法使用独立的反射变量，已保存结果。")

def reflect_private_method_calls(test_file_path, test_class_name, method_signature):
    add_throws_to_reflection_tests(test_file_path)
    add_invocation_target_exception_import(test_file_path)
    rewrite_private_method_calls(test_file_path, test_class_name, method_signature)

# 示例用法
if __name__ == "__main__":
    # 你可以在这里测试
    test_file_path = r"E:\YAU_BIT\Research\Project Implementation\Project1\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1\Now\Experiment\0429_commons-cli-master_all\src\test\java\org\apache\commons\cli\CommandLineTest.java"
    # test_class_name = "CommandLineTest"
    test_class_name = "MissingOptionExceptionTest"
    '''
    method_signature = {
        'ParseException': ['public ParseException wrap(Throwable e)'],
        'CommandLine': [
            'public Builder addArg(String arg)',
            'public Builder addOption(Option option)',
            'public CommandLine build()',
            'public CommandLine get()',
            'public Builder setDeprecatedHandler(Consumer deprecatedHandler)',
            'public Builder builder()',
            'protected void addArg(String arg)',
            'protected void addOption(Option option)',
            'private T get(Supplier supplier)',
            'public List getArgList()',
            'public String getArgs()',
            'public Object getOptionObject(char optionChar)',
            'public Object getOptionObject(String optionName)',
            'public Properties getOptionProperties(Option option)',
            'public Properties getOptionProperties(String optionName)',
            'public Option getOptions()',
            'public String getOptionValue(char optionChar)',
            'public String getOptionValue(char optionChar, String defaultValue)',
            'public String getOptionValue(char optionChar, Supplier defaultValue)',
            'public String getOptionValue(Option option)',
            'public String getOptionValue(Option option, String defaultValue)',
            'public String getOptionValue(Option option, Supplier defaultValue)',
            'public String getOptionValue(OptionGroup optionGroup)',
            'public String getOptionValue(OptionGroup optionGroup, String defaultValue)',
            'public String getOptionValue(OptionGroup optionGroup, Supplier defaultValue)',
            'public String getOptionValue(String optionName)',
            'public String getOptionValue(String optionName, String defaultValue)',
            'public String getOptionValue(String optionName, Supplier defaultValue)',
            'public String getOptionValues(char optionChar)',
            'public String getOptionValues(Option option)',
            'public String getOptionValues(OptionGroup optionGroup)',
            'public String getOptionValues(String optionName)',
            'public T getParsedOptionValue(char optionChar)',
            'public T getParsedOptionValue(char optionChar, Supplier defaultValue)',
            'public T getParsedOptionValue(char optionChar, T defaultValue)',
            'public T getParsedOptionValue(Option option)',
            'public T getParsedOptionValue(Option option, Supplier defaultValue)',
            'public T getParsedOptionValue(Option option, T defaultValue)',
            'public T getParsedOptionValue(OptionGroup optionGroup)',
            'public T getParsedOptionValue(OptionGroup optionGroup, Supplier defaultValue)',
            'public T getParsedOptionValue(OptionGroup optionGroup, T defaultValue)',
            'public T getParsedOptionValue(String optionName)',
            'public T getParsedOptionValue(String optionName, Supplier defaultValue)',
            'public T getParsedOptionValue(String optionName, T defaultValue)',
            'public T getParsedOptionValues(char optionChar)',
            'public T getParsedOptionValues(char optionChar, Supplier defaultValue)',
            'public T getParsedOptionValues(char optionChar, T defaultValue)',
            'public T getParsedOptionValues(Option option)',
            'public T getParsedOptionValues(Option option, Supplier defaultValue)',
            'public T getParsedOptionValues(Option option, T defaultValue)',
            'public T getParsedOptionValues(OptionGroup optionGroup)',
            'public T getParsedOptionValues(OptionGroup optionGroup, Supplier defaultValue)',
            'public T getParsedOptionValues(OptionGroup optionGroup, T defaultValue)',
            'public T getParsedOptionValues(String optionName)',
            'public T getParsedOptionValues(String optionName, Supplier defaultValue)',
            'public T getParsedOptionValues(String optionName, T defaultValue)',
            'private void handleDeprecated(Option option)',
            'public boolean hasOption(char optionChar)',
            'public boolean hasOption(Option option)',
            'public boolean hasOption(OptionGroup optionGroup)',
            'public boolean hasOption(String optionName)',
            'public Iterator iterator()',
            'private void processPropertiesFromValues(Properties props, List values)',
            'private Option resolveOption(String optionName)'
        ],
        'Util': [
            'default T defaultValue(T str, T defaultValue)',
            'default int indexOfNonWhitespace(CharSequence text, int startPos)',
            'default boolean isEmpty(CharSequence str)',
            'default boolean isWhitespace(char c)',
            'default String ltrim(String s)',
            'default String repeat(int len, char fillChar)',
            'default String repeatSpace(int len)',
            'default String rtrim(String s)'
        ]
    }
    '''

    reflect_private_method_calls(test_file_path, test_class_name, method_signature)