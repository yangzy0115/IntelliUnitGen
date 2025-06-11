import re
import os

def rewrite_private_constructors_with_builder(test_file_path, test_class_name, method_signature):
    with open(test_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 找出 CommandLine 类的私有构造函数参数列表
    constructor_map = {}
    for class_name, signatures in method_signature.items():
        for sig in signatures:
            if (sig.startswith("private") or sig.startswith("protected")) and class_name in sig:
                match = re.match(r'(?:private|protected)\s+(\w+)\s*\((.*?)\)', sig)
                if match:
                    constructor_name, params = match.groups()
                    if constructor_name == class_name:
                        param_types = [p.strip().split()[-1] for p in params.split(',')] if params else []
                        constructor_map[class_name] = param_types

    updated_lines = []
    for i, line in enumerate(lines):
        matched = False
        for class_name, param_types in constructor_map.items():
            # 支持多层嵌套构造参数，改为非贪婪匹配 + 容忍空格 + 结束于括号后分号
            pattern = rf'(\w+)\s*=\s*new\s+{re.escape(class_name)}\s*\((.*?)\);'
            match = re.search(pattern, line)
            if match:
                var_name, args_str = match.groups()
                args_str = args_str.strip()

                # 处理泛型和括号嵌套安全分割参数
                depth, arg, args_list = 0, '', []
                for ch in args_str:
                    if ch == ',' and depth == 0:
                        args_list.append(arg.strip())
                        arg = ''
                    else:
                        if ch in '(<[':
                            depth += 1
                        elif ch in ')>]':
                            depth -= 1
                        arg += ch
                if arg:
                    args_list.append(arg.strip())

                indent = re.match(r'\s*', line).group(0)
                builder_code = [f"{indent}// {line.strip()}\n",
                                 f"{indent}{class_name}.Builder builder = new {class_name}.Builder();\n"]

                for arg in args_list:
                    if "LinkedList" in arg or "args" in arg:
                        builder_code.append(f"{indent}builder.addArg({arg});\n")
                    elif "List.of" in arg or "testOption" in arg or "options" in arg:
                        builder_code.append(f"{indent}builder.addOption({arg});\n")
                    elif "DEPRECATED_HANDLER" in arg or "handler" in arg:
                        builder_code.append(f"{indent}builder.setDeprecatedHandler({arg});\n")

                builder_code.append(f"{indent}{var_name} = builder.build();\n")
                updated_lines.extend(builder_code)
                matched = True
                break

        if not matched:
            updated_lines.append(line)

    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print("✅ 私有构造函数调用已替换为 builder 形式。")
# 示例用法
if __name__ == "__main__":
    # 你可以在这里测试
    test_file_path = r"E:\YAU_BIT\Research\Project Implementation\Project1\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1\Now\Experiment\0429_commons-cli-master_all\src\test\java\org\apache\commons\cli\CommandLineTest.java"
    test_class_name = "CommandLineTest"
    method_signature = {'ParseException': ['public ParseException wrap(Throwable e)', 'public ParseException ParseException(String message)', 'public ParseException ParseException(Throwable e)'], 'Util': ['default T defaultValue(T str, T defaultValue)', 'default int indexOfNonWhitespace(CharSequence text, int startPos)', 'default boolean isEmpty(CharSequence str)', 'default boolean isWhitespace(char c)', 'default String ltrim(String s)', 'default String repeat(int len, char fillChar)', 'default String repeatSpace(int len)', 'default String rtrim(String s)', 'private Util Util()'], 'CommandLine': ['public Builder addArg(String arg)', 'public Builder addOption(Option option)', 'public CommandLine build()', 'public CommandLine get()', 'public Builder setDeprecatedHandler(Consumer deprecatedHandler)', 'public Builder builder()', 'protected void addArg(String arg)', 'protected void addOption(Option option)', 'private T get(Supplier supplier)', 'public List getArgList()', 'public String getArgs()', 'public Object getOptionObject(char optionChar)', 'public Object getOptionObject(String optionName)', 'public Properties getOptionProperties(Option option)', 'public Properties getOptionProperties(String optionName)', 'public Option getOptions()', 'public String getOptionValue(char optionChar)', 'public String getOptionValue(char optionChar, String defaultValue)', 'public String getOptionValue(char optionChar, Supplier defaultValue)', 'public String getOptionValue(Option option)', 'public String getOptionValue(Option option, String defaultValue)', 'public String getOptionValue(Option option, Supplier defaultValue)', 'public String getOptionValue(OptionGroup optionGroup)', 'public String getOptionValue(OptionGroup optionGroup, String defaultValue)', 'public String getOptionValue(OptionGroup optionGroup, Supplier defaultValue)', 'public String getOptionValue(String optionName)', 'public String getOptionValue(String optionName, String defaultValue)', 'public String getOptionValue(String optionName, Supplier defaultValue)', 'public String getOptionValues(char optionChar)', 'public String getOptionValues(Option option)', 'public String getOptionValues(OptionGroup optionGroup)', 'public String getOptionValues(String optionName)', 'public T getParsedOptionValue(char optionChar)', 'public T getParsedOptionValue(char optionChar, Supplier defaultValue)', 'public T getParsedOptionValue(char optionChar, T defaultValue)', 'public T getParsedOptionValue(Option option)', 'public T getParsedOptionValue(Option option, Supplier defaultValue)', 'public T getParsedOptionValue(Option option, T defaultValue)', 'public T getParsedOptionValue(OptionGroup optionGroup)', 'public T getParsedOptionValue(OptionGroup optionGroup, Supplier defaultValue)', 'public T getParsedOptionValue(OptionGroup optionGroup, T defaultValue)', 'public T getParsedOptionValue(String optionName)', 'public T getParsedOptionValue(String optionName, Supplier defaultValue)', 'public T getParsedOptionValue(String optionName, T defaultValue)', 'public T getParsedOptionValues(char optionChar)', 'public T getParsedOptionValues(char optionChar, Supplier defaultValue)', 'public T getParsedOptionValues(char optionChar, T defaultValue)', 'public T getParsedOptionValues(Option option)', 'public T getParsedOptionValues(Option option, Supplier defaultValue)', 'public T getParsedOptionValues(Option option, T defaultValue)', 'public T getParsedOptionValues(OptionGroup optionGroup)', 'public T getParsedOptionValues(OptionGroup optionGroup, Supplier defaultValue)', 'public T getParsedOptionValues(OptionGroup optionGroup, T defaultValue)', 'public T getParsedOptionValues(String optionName)', 'public T getParsedOptionValues(String optionName, Supplier defaultValue)', 'public T getParsedOptionValues(String optionName, T defaultValue)', 'private void handleDeprecated(Option option)', 'public boolean hasOption(char optionChar)', 'public boolean hasOption(Option option)', 'public boolean hasOption(OptionGroup optionGroup)', 'public boolean hasOption(String optionName)', 'public Iterator iterator()', 'private void processPropertiesFromValues(Properties props, List values)', 'private Option resolveOption(String optionName)', 'public CommandLine Builder()', 'protected CommandLine CommandLine()', 'private CommandLine CommandLine(List args, List options, Consumer deprecatedHandler)']}
    rewrite_private_constructors_with_builder(test_file_path, test_class_name, method_signature)