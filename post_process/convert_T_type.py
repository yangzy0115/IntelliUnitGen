import re
from typing import List, Dict

def infer_cast_type_from_signature(signature: str) -> str:
    match = re.match(r"(public|protected|private|default)?\s+([a-zA-Z0-9_<>]+)\s+[a-zA-Z0-9_]+\(", signature)
    if match:
        return_type = match.group(2)
        if return_type in ['int', 'double', 'float', 'boolean', 'char', 'byte', 'short', 'long']:
            return return_type
        return return_type.split("<")[0]
    return "Object"

def covert(test_file_content: str, method_signatures: List[str]) -> str:
    method_return_types = {}
    for sig in method_signatures:
        match = re.match(r".*\s+([a-zA-Z0-9_]+)\(.*\)", sig)
        if match:
            method_name = match.group(1)
            method_return_types[method_name] = infer_cast_type_from_signature(sig)

    def replacer(match):
        method_call = match.group(1)
        method_name_match = re.search(r'\.invoke\([^,]+,\s*"?([a-zA-Z0-9_]+)"?', method_call)
        if method_name_match:
            method_name = method_name_match.group(1)
            cast_type = method_return_types.get(method_name, "Object")
        else:
            cast_type = "Object"
        return f"({cast_type}) {method_call}"

    fixed_content = re.sub(r"\(T\)\s*((?:method\d*)\.invoke\([^)]+\))", replacer, test_file_content)
    return fixed_content

def covert_T_type(test_file_path: str, test_class_name: str, method_signature: Dict[str, List[str]]) -> None:
    method_signature_list = [item for sublist in method_signature.values() for item in sublist]
    with open(test_file_path, "r", encoding="utf-8") as f:
        test_file_content = f.read()
    fixed_content = covert(test_file_content, method_signature_list)
    with open(test_file_path, "w", encoding="utf-8") as f:
        f.write(fixed_content)
    print("✅ 修复完成：文件已更新。")

# test_file_path = r"E:\YAU_BIT\Research\Project Implementation\Project1\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1\Now\Experiment\0516_commons-cli-master_all\src\test\java\org\apache\commons\cli\CommandLineTest.java"
# test_class_name = "CommandLineTest"
# method_signature = {'ParseException': ['public ParseException wrap(Throwable e)', 'public ParseException ParseException(String message)', 'public ParseException ParseException(Throwable e)'], 'Util': ['default T defaultValue(T str, T defaultValue)', 'default int indexOfNonWhitespace(CharSequence text, int startPos)', 'default boolean isEmpty(CharSequence str)', 'default boolean isWhitespace(char c)', 'default String ltrim(String s)', 'default String repeat(int len, char fillChar)', 'default String repeatSpace(int len)', 'default String rtrim(String s)', 'private Util Util()'], 'CommandLine': ['public Builder addArg(String arg)', 'public Builder addOption(Option option)', 'public CommandLine build()', 'public CommandLine get()', 'public Builder setDeprecatedHandler(Consumer deprecatedHandler)', 'public Builder builder()', 'protected void addArg(String arg)', 'protected void addOption(Option option)', 'private T get(Supplier supplier)', 'public List getArgList()', 'public String getArgs()', 'public Object getOptionObject(char optionChar)', 'public Object getOptionObject(String optionName)', 'public Properties getOptionProperties(Option option)', 'public Properties getOptionProperties(String optionName)', 'public Option getOptions()', 'public String getOptionValue(char optionChar)', 'public String getOptionValue(char optionChar, String defaultValue)', 'public String getOptionValue(char optionChar, Supplier defaultValue)', 'public String getOptionValue(Option option)', 'public String getOptionValue(Option option, String defaultValue)', 'public String getOptionValue(Option option, Supplier defaultValue)', 'public String getOptionValue(OptionGroup optionGroup)', 'public String getOptionValue(OptionGroup optionGroup, String defaultValue)', 'public String getOptionValue(OptionGroup optionGroup, Supplier defaultValue)', 'public String getOptionValue(String optionName)', 'public String getOptionValue(String optionName, String defaultValue)', 'public String getOptionValue(String optionName, Supplier defaultValue)', 'public String getOptionValues(char optionChar)', 'public String getOptionValues(Option option)', 'public String getOptionValues(OptionGroup optionGroup)', 'public String getOptionValues(String optionName)', 'public T getParsedOptionValue(char optionChar)', 'public T getParsedOptionValue(char optionChar, Supplier defaultValue)', 'public T getParsedOptionValue(char optionChar, T defaultValue)', 'public T getParsedOptionValue(Option option)', 'public T getParsedOptionValue(Option option, Supplier defaultValue)', 'public T getParsedOptionValue(Option option, T defaultValue)', 'public T getParsedOptionValue(OptionGroup optionGroup)', 'public T getParsedOptionValue(OptionGroup optionGroup, Supplier defaultValue)', 'public T getParsedOptionValue(OptionGroup optionGroup, T defaultValue)', 'public T getParsedOptionValue(String optionName)', 'public T getParsedOptionValue(String optionName, Supplier defaultValue)', 'public T getParsedOptionValue(String optionName, T defaultValue)', 'public T getParsedOptionValues(char optionChar)', 'public T getParsedOptionValues(char optionChar, Supplier defaultValue)', 'public T getParsedOptionValues(char optionChar, T defaultValue)', 'public T getParsedOptionValues(Option option)', 'public T getParsedOptionValues(Option option, Supplier defaultValue)', 'public T getParsedOptionValues(Option option, T defaultValue)', 'public T getParsedOptionValues(OptionGroup optionGroup)', 'public T getParsedOptionValues(OptionGroup optionGroup, Supplier defaultValue)', 'public T getParsedOptionValues(OptionGroup optionGroup, T defaultValue)', 'public T getParsedOptionValues(String optionName)', 'public T getParsedOptionValues(String optionName, Supplier defaultValue)', 'public T getParsedOptionValues(String optionName, T defaultValue)', 'private void handleDeprecated(Option option)', 'public boolean hasOption(char optionChar)', 'public boolean hasOption(Option option)', 'public boolean hasOption(OptionGroup optionGroup)', 'public boolean hasOption(String optionName)', 'public Iterator iterator()', 'private void processPropertiesFromValues(Properties props, List values)', 'private Option resolveOption(String optionName)', 'public CommandLine Builder()', 'protected CommandLine CommandLine()', 'private CommandLine CommandLine(List args, List options, Consumer deprecatedHandler)']}

# covert_T_type(test_file_path, test_class_name, method_signature)