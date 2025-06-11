import re
import lizard
from language_switch.language_switcher import get_text

# ----------------- 工具函数区 -----------------

def is_escaped(code, index):
    backslash_count = 0
    i = index - 1
    while i >= 0 and code[i] == '\\':
        backslash_count += 1
        i -= 1
    return backslash_count % 2 == 1

def remove_java_comments(java_code):
    result = []
    i = 0
    in_single_quote = False
    in_double_quote = False
    in_single_line_comment = False
    in_multi_line_comment = False

    while i < len(java_code):
        ch = java_code[i]
        next_ch = java_code[i + 1] if i + 1 < len(java_code) else ''

        if not in_single_quote and not in_double_quote:
            if not in_multi_line_comment and not in_single_line_comment:
                if ch == '/' and next_ch == '/':
                    in_single_line_comment = True
                    i += 2
                    continue
                elif ch == '/' and next_ch == '*':
                    in_multi_line_comment = True
                    i += 2
                    continue

        if in_single_line_comment:
            if ch == '\n':
                in_single_line_comment = False
                result.append(ch)
            i += 1
            continue

        if in_multi_line_comment:
            if ch == '*' and next_ch == '/':
                in_multi_line_comment = False
                i += 2
            else:
                i += 1
            continue

        if ch == '"' and not in_single_quote:
            result.append(ch)
            if not is_escaped(java_code, i):
                in_double_quote = not in_double_quote
        elif ch == "'" and not in_double_quote:
            result.append(ch)
            if not is_escaped(java_code, i):
                in_single_quote = not in_single_quote
        else:
            result.append(ch)

        i += 1

    return ''.join(result)

def remove_all_empty_lines_outside_quotes(java_code):
    result = []
    in_single_quote = False
    in_double_quote = False

    lines = java_code.splitlines(keepends=True)

    for line in lines:
        stripped_line = line.strip()

        for i, ch in enumerate(line):
            if ch == '"' and not in_single_quote:
                if not is_escaped(line, i):
                    in_double_quote = not in_double_quote
            elif ch == "'" and not in_double_quote:
                if not is_escaped(line, i):
                    in_single_quote = not in_single_quote

        if stripped_line == '' and not in_single_quote and not in_double_quote:
            continue

        result.append(line)

    return ''.join(result)

def remove_spaces_around_symbols_outside_quotes(java_code):
    result_lines = []

    for line in java_code.splitlines():
        new_line = ''
        i = 0
        in_single_quote = False
        in_double_quote = False
        buffer = ''

        while i < len(line):
            ch = line[i]

            if ch == '"' and not in_single_quote:
                buffer += ch
                if not is_escaped(line, i):
                    in_double_quote = not in_double_quote
                i += 1
                continue
            elif ch == "'" and not in_double_quote:
                buffer += ch
                if not is_escaped(line, i):
                    in_single_quote = not in_single_quote
                i += 1
                continue

            if in_single_quote or in_double_quote:
                buffer += ch
                i += 1
                continue

            buffer += ch
            i += 1

        cleaned_line = clean_outside_quotes(buffer)
        result_lines.append(cleaned_line)

    return '\n'.join(result_lines)

def clean_outside_quotes(line):
    string_spans = []
    pattern = r'"(\\.|[^"\\])*"|\'(\\.|[^\'\\])*\''
    for m in re.finditer(pattern, line):
        string_spans.append((m.start(), m.end()))

    def in_string(index):
        return any(start <= index < end for start, end in string_spans)

    patterns = [
        (r'\s*([=+\-*/%<>&|^!]=?|==|!=|<=|>=)\s*', r'\1'),
        (r'\s*\(\s*', r'('),
        (r'\s*\)\s*', r')'),
        (r'\s*;\s*', r';'),
    ]

    i = 0
    output = ''
    while i < len(line):
        if in_string(i):
            for span in string_spans:
                if span[0] == i:
                    output += line[span[0]:span[1]]
                    i = span[1]
                    break
        else:
            matched = False
            for pattern, repl in patterns:
                m = re.match(pattern, line[i:])
                if m:
                    output += re.sub(pattern, repl, m.group(0))
                    i += len(m.group(0))
                    matched = True
                    break
            if not matched:
                output += line[i]
                i += 1

    return output

def normalize_indentation(java_code):
    return java_code

def format_statements(java_code):
    return java_code

# ----------------- 圈复杂度检测并删除简单方法 -----------------

def get_complex_methods(java_code, min_complexity=4):

    # 检测圈复杂度并删除圈复杂度小于 min_complexity 的方法 
    analysis = lizard.analyze_file.analyze_source_code("temp.java", java_code)

    print(f"\n{get_text('recognized_methods')}: {len(analysis.function_list)}\n")
    if not analysis.function_list:
        print("⚡⚡⚡ " + get_text('no_method'))
        return False, []

    complex_methods = []
    return True, complex_methods

    '''
    for func in analysis.function_list:
        print(f"方法 {func.name}，圈复杂度={func.cyclomatic_complexity}，参数={func.parameters}")
        if func.cyclomatic_complexity >= min_complexity:
            complex_methods.append((f"{func.name}({func.parameters})", func.start_line, func.end_line))

    # 重点！！！如果没有需要保留的方法，直接返回空
    if not complex_methods:
        print("⚡⚡⚡ 所有方法圈复杂度过低，无需处理！")
        return False, []
    else:
        print("\n✅ 复杂方法有：")
        for name, start, end in complex_methods:
            print(f"  - {name} (行 {start} 到 {end})")
        print(f"共有 {len(complex_methods)} 个复杂方法。\n")
        return True, complex_methods
    '''

# ----------------- 清理和规范化 -----------------

def code_cleaning(pre_process_java_code):
    pre_process_java_code = remove_java_comments(pre_process_java_code)
    pre_process_java_code = remove_all_empty_lines_outside_quotes(pre_process_java_code)
    pre_process_java_code = remove_spaces_around_symbols_outside_quotes(pre_process_java_code)
    return pre_process_java_code.strip()

def code_normalization(pre_process_java_code):
    pre_process_java_code = normalize_indentation(pre_process_java_code)
    pre_process_java_code = format_statements(pre_process_java_code)
    return pre_process_java_code.strip()

