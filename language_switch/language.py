# language.py

language = {
    'phase_1': {
        'en': 'Phase 1: Preprocessing',
        'zh': '阶段一：预处理'
    },
    'phase_2': {
        'en': 'Phase 2: Static Analysis',
        'zh': '阶段二：静态分析'
    },
    'common_info': {
        'en': 'Common Information of Code',
        'zh': '代码公共信息'
    },
    'extracted_decision_nodes': {
        'en': 'Extracted Decision Nodes:',
        'zh': '提取的判定节点'
    },
    'extracted_exception_handling': {
        'en': 'Extracted Exception Handling:',
        'zh': '提取的异常处理'
    },
    'extracted_class_name': {
        'en': 'Extracted Class Name:',
        'zh': '提取的类名'
    },
    'extracted_method_name': {
        'en': 'Extracted Method Name:',
        'zh': '提取的方法名'
    },
    'extracted_method_info': {
        'en': 'Extracted Method Info:',
        'zh': '提取的方法详细信息'
    },
    'extracted_executable_statements_count': {
        'en': 'Number of Executable Statements',
        'zh': '提取的可执行语句的个数'
    },
    'extracted_executable_statements': {
        'en': 'Extracted Executable Statements',
        'zh': '提取的可执行语句'
    },
    'extracted_function_info': {
        'en': 'Extracted Function Information',
        'zh': '提取的函数信息'
    },
    'extracted_method_signature': {
        'en': 'Extracted Method Signature',
        'zh': '方法签名信息'
    },
    'specific_info': {
        'en': 'Specific Information of Code',
        'zh': '代码特定信息'
    },
    'recognized_methods': {
        'en': 'Recognized {len(analysis.function_list)} methods',
        'zh': '识别到 {len(analysis.function_list)} 个方法'
    },
    'class_methods': {
        'en': 'Class {class_name} methods',
        'zh': '类 {class_name} 的方法：'
    },
    'prompt_synthesis': {
        'en': 'Prompt Synthesis',
        'zh': '阶段三：Prompt合成'
    },
    'context_learning': {
        'en': 'Context Learning',
        'zh': '上下文学习'
    },
    'dependency_info': {
        'en': 'Dependency Information',
        'zh': '依赖关系信息'
    },
    'dependency_analysis_prompt_title': {
        'en': 'Dependency Analysis Prompt',
        'zh': '依赖关系 Prompt'
    },
    'context_learning_phase': {
        'en': 'Phase 4：Context Learning',
        'zh': '阶段四：上下文学习'
    },
    'static_analysis_prompt_title': {
        'en': 'Static Analysis Prompt',
        'zh': '结构信息 Prompt'
    },
    'select_java_file_or_dir': {
        'en': 'Select Java File or Directory',
        'zh': '选择 Java 文件或目录'
    },
    'please_select_import_method': {
        'en': 'Please Select Import Method',
        'zh': '请选择导入方式：'
    },
    'select_java_file': {
        'en': 'Select Java File',
        'zh': '选择 Java 文件'
    },
    'select_dir': {
        'en': 'Select Directory',
        'zh': '选择目录'
    },
    'user_closed_main_window': {
        'en': 'User Closed Main Window',
        'zh': '用户关闭了主选择窗口'
    },
    'prompt': {
        'en': 'Prompt',
        'zh': '提示'
    },
    'user_closed_main_window_prompt': {
        'en': 'You did not select the correct file, do you want to continue selecting?',
        'zh': '您未正确选择文件，是否继续选择？'
    },
    'user_continue_selecting': {
        'en': 'User Continue Selecting',
        'zh': '用户选择继续选择文件'
    },
    'user_exit_program': {
        'en': 'User Exit Program',
        'zh': '用户选择退出程序'
    },
    'select_test_code_save_path': {
        'en': 'Select Test Code Save Path',
        'zh': '请选择 Java 测试代码保存路径'
    },
    'no_save_path': {
        'en': 'No Save Path, Program Terminated',
        'zh': '未选择保存路径，程序终止'
    },
    'select_project_run_path': {
        'en': 'Select Project Run Path (For Compilation)',
        'zh': '请选择项目运行路径（用于编译）'
    },
    'no_run_path': {
        'en': 'No Run Path, Program Terminated',
        'zh': '未选择运行路径，程序终止'
    },
    'save_path': {
        'en': 'Save Path',
        'zh': '保存路径'
    },
    'compile_path': {
        'en': 'Compile Path',
        'zh': '编译路径'
    },
    'save_java_test_code': {
        'en': 'Save Java Test Code',
        'zh': '保存 Java 测试代码'
    },
    'save_java_test_code_success': {
        'en': 'JUnit Test Code Successfully Saved to',
        'zh': 'JUnit 测试代码已成功保存到'
    },
    'save_java_test_code_failed': {
        'en': 'Save Test Code Failed',
        'zh': '保存测试代码失败'
    },
    'test_case_generate_success': {
        'en': 'Test Case Generate Success, and Compile or Run Success',
        'zh': '测试用例生成成功，且编译或运行成功'
    },
    're_generate_times': {
        'en': 'Re-generate Times',
        'zh': '测试用例重新生成次数'
    },
    'test_case_generate_failed': {
        'en': 'Test Case Generate Failed, Please Manually Fix',
        'zh': '测试用例已生成，但编译或运行出错，请手动修复'
    },
    'backup_failed_test_case': {
        'en': 'Backup Failed Test Case to',
        'zh': '已将编译或运行出错的原始测试类备份到'
    },
    'backup_failed_test_case_prompt': {
        'en': 'You Can Modify the Test Class',
        'zh': '您可在测试类中进行修改'
    },
    'parse_failed_skip': {
        'en': 'Parse Failed, Skip. Error Information',
        'zh': '解析失败，跳过。错误信息'
    },
    'source_code_fragment': {
        'en': 'Source Code Fragment',
        'zh': '源码片段'
    },
    'processing_file': {
        'en': 'Processing File',
        'zh': '正在处理文件'
    },
    'please_select_java_file_or_dir': {
        'en': 'Please Select Java File or Directory',
        'zh': '请选择 Java 文件或目录'
    },
    'code_preview': {
        'en': 'Code Preview (First 500 Characters)',
        'zh': '代码内容预览 (前500字符)'
    },
    'read_file_error': {
        'en': 'Read File Error',
        'zh': '读取文件出错'
    },
    'no_java_file': {
        'en': 'No Java File Selected',
        'zh': '未选择 Java 文件'
    },
    'select_java_file_dir': {
        'en': 'Select Java File Directory',
        'zh': '选择包含 Java 文件的文件夹'
    },
    'Found': {
        'en': 'Found',
        'zh': '共找到'
    },
    'java_file_count': {
        'en': 'Java File Count',
        'zh': '个Java文件'
    },
    'code_preview_lines': {
        'en': 'Code Preview (First 5 Lines)',
        'zh': '代码内容预览 (前5行)'
    },
    'read_file_error': {
        'en': 'Read File Error',
        'zh': '读取文件出错'
    },
    'no_dir_selected': {
        'en': 'No Directory Selected',
        'zh': '未选择目录'
    },
    'please_select_coverage_type': {
        'en': 'Please Select Coverage Type',
        'zh': '请选择您需要达到何种覆盖'
    },
    'statement_coverage': {
        'en': 'Statement Coverage',
        'zh': '语句覆盖'
    },
    'condition_coverage': {
        'en': 'Condition Coverage',
        'zh': '条件覆盖'
    },
    'branch_coverage': {
        'en': 'Branch Coverage',
        'zh': '分支覆盖'
    },
    'decision_coverage': {
        'en': 'Decision Coverage',
        'zh': '决策覆盖'
    },
    'path_coverage': {
        'en': 'Path Coverage',
        'zh': '路径覆盖'
    },
    'code_import': {
        'en': 'Code Import',
        'zh': '代码导入'
    },
    'no_method': {
        'en': 'No Method',
        'zh': '没有方法，无需处理！'
    }
    
}