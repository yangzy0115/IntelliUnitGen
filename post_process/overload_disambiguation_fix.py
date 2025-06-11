import re

def extract_param_type(param: str):
    """
    提取参数的类型（忽略变量名）：
    如 'char optionChar' => 'char'
    如 'Supplier<String[]> defaultValue' => 'Supplier'
    """
    return param.strip().split()[0].split('<')[0]

def disambiguate_null_overloads_in_place(test_file_path, test_class_name, method_signature):
    with open(test_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 构建 method -> list of param_types
    method_map = {}
    for class_name, signatures in method_signature.items():
        for sig in signatures:
            match = re.match(r'(public|protected|private)\s+[\w<>\[\]]+\s+(\w+)\((.*?)\)', sig)
            if match:
                _, method_name, params = match.groups()
                param_list = [extract_param_type(p) for p in params.split(',')] if params.strip() else []
                method_map.setdefault(method_name, []).append(param_list)

    updated_lines = []
    for line in lines:
        original_line = line

        # 匹配两参数形式 null, xxx
        match_2 = re.search(r'(\w+)\.(\w+)\(\s*null\s*,\s*([^)]+)\)', line)
        if match_2:
            obj, method_name, second_arg = match_2.groups()
            for param_types in method_map.get(method_name, []):
                if len(param_types) == 2 and 'Supplier' in param_types[1] and 'null' not in param_types[0].lower():
                    cast_type = param_types[0]
                    fixed = f'{obj}.{method_name}(({cast_type})null, {second_arg})'
                    pattern = rf'{obj}\.{method_name}\(\s*null\s*,\s*{re.escape(second_arg)}\)'
                    line = re.sub(pattern, fixed, line)
                    print(f'[修复-2参] {original_line.strip()} => {line.strip()}')
                    break

        # 匹配一参数形式 null
        match_1 = re.search(r'(\w+)\.(\w+)\(\s*null\s*\)', line)
        if match_1:
            obj, method_name = match_1.groups()
            for param_types in method_map.get(method_name, []):
                if len(param_types) == 1 and 'null' not in param_types[0].lower():
                    cast_type = param_types[0]
                    fixed = f'{obj}.{method_name}(({cast_type})null)'
                    pattern = rf'{obj}\.{method_name}\(\s*null\s*\)'
                    line = re.sub(pattern, fixed, line)
                    print(f'[修复-1参] {original_line.strip()} => {line.strip()}')
                    break

        updated_lines.append(line)

    with open(test_file_path, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)

    print(f"[完成] 文件已更新：{test_file_path}")

# 示例用法
if __name__ == "__main__":

        # 你可以在这里测试
    test_file_path = r"E:\YAU_BIT\Research\Project Implementation\Project1\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1\Now\Experiment\0429_commons-cli-master_all\src\test\java\org\apache\commons\cli\CommandLineTest.java"
    test_class_name = "CommandLineTest"
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

    disambiguate_null_overloads_in_place(test_file_path, test_class_name, method_signature)
