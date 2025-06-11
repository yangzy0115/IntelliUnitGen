import os
from import_export.import_java_code import show_initial_choice
from import_export.import_java_code import show_warning
from pre_process.data_standardization import get_complex_methods
from pre_process.data_standardization import code_cleaning
from pre_process.data_standardization import code_normalization
from static_analysis.common import static_code_analysis_common
from static_analysis.extra import static_code_analysis_extra
from static_analysis.dependency_relationship_analysis import analyze_project_java_files
from static_analysis.package_info import get_project_classes
from generate_test_cases.test_cases_generation import generate_test_case
from prompt_synthesis.prompt_synthesis import prompt_synthesis
from import_export.save_code import save_the_test_cases
from import_export.save_code import set_global_paths
from import_export.save_code import save_the_test_cases
from bug_repaired.bug_fix import compile_and_run_java
from bug_repaired.bug_fix import fix_bug
from bug_repaired.bug_fix import re_generate_last_prompt
from bug_repaired.bug_fix import re_generate_all_prompt
from post_process.private_method_reflect import reflect_private_method_calls
from post_process.package_import_add import add_package_and_import, add_package_and_import_auto
from post_process.convert_T_type import covert_T_type
import shutil
import javalang
from language_switch.language_switcher import get_text


def user_select():
    print("\n")
    print("###################################")
    print("######" + get_text('please_select_coverage_type') + "#######")
    print("###################################")
    print("(1)" + get_text('statement_coverage'))
    print("(2)" + get_text('condition_coverage'))
    print("(3)" + get_text('branch_coverage'))
    print("(4)" + get_text('decision_coverage'))
    print("(5)" + get_text('path_coverage'))
    select = int(input().strip())
    return select

def process_java_code(java_code, select, project_path, all_dependency_result, all_method_signature, class_file_name, path):
    
    '''
    is_generate_success = False
    re_generate_times = 0
    compile_times = 0
    test_file_path = os.path.join(project_path, r"src/test/java/org/apache/commons/cli/CommandLineTest.java")

    print("⚠️⚠️⚠️ 测试用例已生成，但编译或运行出错，请手动修复")
    # 将失败的测试类复制到before_fix文件夹，保持包结构
    before_fix_dir = os.path.join(project_path, "before_fix")
    # 从test_file_path中提取包路径
    package_path = os.path.dirname(test_file_path)
    # 在before_fix下创建对应的包目录结构 
    target_dir = os.path.join(before_fix_dir, os.path.relpath(package_path, project_path))
    os.makedirs(target_dir, exist_ok=True)
    # 复制文件到对应包目录下
    failed_test_path = os.path.join(target_dir, os.path.basename(test_file_path))
    shutil.copy2(test_file_path, failed_test_path)
    print(f"⚠️⚠️⚠️ 已将编译或运行出错的原始测试类备份到: {failed_test_path}，您可在测试类中进行修改")
    return
    '''
    
    # 阶段一 预处理
    print("\n\n")
    print("########### " + get_text('phase_1') + " ############\n")
    is_need_process, complex_methods = get_complex_methods(java_code, min_complexity=4)

    if not is_need_process:
        return
    
    # pre_process_java_code = code_cleaning(pre_process_java_code)
    pre_process_java_code = code_cleaning(java_code)
    pre_process_java_code = code_normalization(pre_process_java_code)
    print(pre_process_java_code)
    # print(f"✅✅✅ 复杂方法：{complex_methods}")
    # print(f"✅✅✅ 复杂方法个数：{len(complex_methods)}")
    # return
    # 阶段二 静态分析
    print("\n\n")

    print("########## " + get_text('phase_2') + " ############")

    print("\n@@@@@ " + get_text('dependency_info') + " @@@@@\n")
    # print(class_file_name)
    # return
    print("all_dependency_result: ", all_dependency_result)
    print("class_file_name: ", class_file_name)
    # print("依赖分析keys: ", all_dependency_result.keys())

    dependency_classes = all_dependency_result[class_file_name]
    print(dependency_classes)
    # return
    print("\n@@@@@ " + get_text('extracted_method_signature') + " @@@@@\n")
    method_signature = {}
    for dep_class in dependency_classes:
        if dep_class in all_method_signature:
            method_signature[dep_class] = all_method_signature[dep_class]
        else:
            print(f"⚠️ 警告：未在方法签名字典中找到类 {dep_class} 的方法定义。")

    print(method_signature)
    # return
    # 输出结构良好的方法签名信息
    for class_name, methods in method_signature.items():
        print(f"\n{get_text('class_methods', class_name)}")
        for m in methods:
            print(f"  - {m}")
            
    # method_signature = all_method_signature[dependency_classes]
    # return
    print("\n@@@@@ " + get_text('specific_info') + " @@@@@\n")
    java_analysis_result = static_code_analysis_extra(pre_process_java_code, select)
    print("\n@@@@@ " + get_text('common_info') + " @@@@@\n")
    static_common = static_code_analysis_common(pre_process_java_code)
    # print("\n@@@@@" + get_text('specific_info_1') + "@@@@@\n")
    # java_analysis_result = static_code_analysis_extra(pre_process_java_code, select)
    # print("\n@@@@@" + get_text('package_info') + "@@@@@\n")
    package_info = get_project_classes(project_path)
    # return

    # 阶段三+四 Prompt合成 + 上下文学习
    print("\n\n")
    print("###################################")
    print("############ " + get_text('prompt_synthesis') + " #############")
    print("############ " + get_text('context_learning_phase') + "#############")
    print("###################################\n")
    java_prompt_synthesis_result, test_class_name = prompt_synthesis(
        pre_process_java_code, static_common, java_analysis_result, dependency_classes, method_signature, select)
    print(java_prompt_synthesis_result)
    # return


    # 阶段五 测试用例生成
    print("\n\n")
    print("###################################")
    print("############阶段五：测试用例生成#############")
    print("###################################\n")
    # while is_generate:
    # print(f"$$$$$$$$$$$$$$$$$$第{generate_times}次生成测试用例$$$$$$$$$$$$$$$$$$")
    java_generate_test_cases_result, messages, messages_with_response = generate_test_case(
        pre_process_java_code, java_prompt_synthesis_result, select, test_class_name)
    statement_tests_result = java_generate_test_cases_result[-1]
    # generate_times += 1
    # if generate_times > 10:
    #     is_generate = False
    #     print("生成测试用例次数超过10次，停止生成")
    #     return
    # return

    test_file_path, test_file_path_run = save_the_test_cases(statement_tests_result, test_class_name)

    # Add by Wanglei (2025-5-6)
    # 阶段六 后处理
    print("\n\n")
    print("###################################")
    print("###########阶段六：后处理###########")
    print("###################################\n")
    # 打桩数据
    # test_file_path = "E:\YAU_BIT\Research\Project Implementation\Project1\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1\Now\Experiment\0429_commons-cli-master_all\src\test\java\org\apache\commons\cli"
    # test_class_name = "CommandLineTest"
    # post_process(test_file_path, test_class_name, dependency_classes, method_signature)
    # 反射私有方法
    print("%%%%%%%%%%%%反射私有方法%%%%%%%%%%%%")
    reflect_private_method_calls(test_file_path, test_class_name, method_signature)
    # covert_T_type(test_file_path, test_class_name, method_signature)
    # add_package_and_import(test_file_path, test_class_name, dependency_classes)
    print("%%%%%%%%%%%%添加包和导入%%%%%%%%%%%%")
    print("[package_info]:", package_info)
    add_package_and_import_auto(test_file_path, test_class_name, package_info, path)
    # return


    # Modified by Wanglei (2025-5-6)
    # 阶段七 编译与运行
    print("\n\n")
    print("###################################")
    # print("##########阶段七：编译与修复###########")
    print("###### ##阶段七：编译与重新生成#### #####")
    print("###################################\n")
    is_generate_success = False
    re_generate_times = 0
    compile_times = 0
    try:
        compile_result_code, test_result_code, compile_log, test_log = compile_and_run_java(test_file_path, test_file_path_run, test_class_name)
        
        if compile_result_code == 0 and test_result_code == 0:
            print("编译与运行成功")
            is_generate_success = True
        else:
            print("编译与运行失败")
            # print(f"$$$$$$$$$$$$$$$$$$正在修复......$$$$$$$$$$$$$$$$$$\n\n")
            print(f"$$$$$$$$$$$$$$$$$$正在重新生成......$$$$$$$$$$$$$$$$$$\n\n")
            # is_generate_success, compile_times = fix_bug(messages_with_response, test_file_path, test_class_name, compile_log, test_log, method_signature, dependency_classes)
            is_generate_success, re_generate_times = re_generate_last_prompt(
                messages,
                pre_process_java_code,
                select,
                test_class_name,
                method_signature,
                dependency_classes,
                path,
                package_info
            )
            # is_generate_success, re_generate_times = re_generate_all_prompt(
            #     pre_process_java_code,
            #     java_prompt_synthesis_result,
            #     select,
            #     test_class_name,
            #     method_signature,
            #     dependency_classes,
            #     path,
            #     package_info
            # )
        
        if is_generate_success:
            print("✅✅✅  " + get_text('test_case_generate_success'))
            print(f"✅✅✅  {get_text('re_generate_times')}: {re_generate_times}")
            # print(f"✅✅✅ 测试用例修复次数：{compile_times}")
            # print(f"测试用例修复次数：{compile_times}")
            # print(f"✅✅✅ 复杂方法：{complex_methods}")
            # print(f"✅✅✅ 复杂方法个数：{len(complex_methods)}")
        else:
            print("⚠️⚠️⚠️  " + get_text('test_case_generate_failed'))
            # 将失败的测试类复制到before_fix文件夹，保持包结构
            before_fix_dir = os.path.join(project_path, "before_fix")
            # 从test_file_path中提取包路径
            package_path = os.path.dirname(test_file_path)
            # 在before_fix下创建对应的包目录结构 
            target_dir = os.path.join(before_fix_dir, os.path.relpath(package_path, project_path))
            os.makedirs(target_dir, exist_ok=True)
            # 复制文件到对应包目录下
            failed_test_path = os.path.join(target_dir, os.path.basename(test_file_path))
            shutil.copy2(test_file_path, failed_test_path)
            print(f"⚠️⚠️⚠️  {get_text('backup_failed_test_case')}: {failed_test_path}，{get_text('backup_failed_test_case_prompt')}")

    #     print("dependencies:", dependency_classes)
    #     print("method_signatures:", method_signature)
    #     print("all_dependency_result（每次更新后）:", all_dependency_result)

    #     if class_file_name not in all_dependency_result:
    #         print(f"未在依赖分析结果中找到 {class_file_name}，可用有: {list(all_dependency_result.keys())}")
    #         return

    #     tree = javalang.parse.parse(java_code)
    #     print("javalang 解析成功")
    #     for path, node in tree.filter((javalang.tree.ClassDeclaration, javalang.tree.InterfaceDeclaration, javalang.tree.EnumDeclaration)):
    #         print("发现声明:", node.name, type(node))
    #         ...

    except Exception as e:
        print(f"⚠️ {get_text('parse_failed_skip')}: {e}")
        print(f"{get_text('source_code_fragment')}: {java_code[:200]}")

def main():
        
    print("\n\n")
    print("###################################")
    print("############" + get_text('code_import') + "############")
    print("###################################")
    
    # 初始选择
    mode, file_list, path = show_initial_choice()
    while mode is None or not file_list:
        mode, file_list, path = show_warning()
    
        
    # 设置全局保存和运行路径
    # set_global_paths()
    project_path = set_global_paths()
    print(project_path)

    # 用户选择覆盖方式
    select = user_select()
    
    # print("\n@@@@@依赖关系分析@@@@@\n")
    all_dependency_result, all_fun_signature = analyze_project_java_files(project_path)
    # print("\n@@@@@所有类的依赖关系@@@@@\n")
    # print(type(all_dependency_result))
    # print(all_dependency_result)
    # print("\n@@@@@所有类的方法签名@@@@@\n")
    # print(type(all_fun_signature))
    # print(all_fun_signature)
    # return

    # 开始处理逻辑3
    if mode == "file":
        with open(file_list[0], "r", encoding="utf-8") as f:
            java_code = f.read()
        class_file_name = os.path.splitext(os.path.basename(file_list[0]))[0]
        process_java_code(java_code, select, project_path, all_dependency_result, all_fun_signature, class_file_name, path)

    elif mode == "dir":
        for java_path in file_list:
            print(f"\n>>> {get_text('processing_file')}: {java_path}")
            with open(java_path, "r", encoding="utf-8") as f:
                java_code = f.read()
            class_file_name = os.path.splitext(os.path.basename(java_path))[0]
            process_java_code(java_code, select, project_path, all_dependency_result, all_fun_signature, class_file_name, path)


if __name__ == "__main__":
    main()
