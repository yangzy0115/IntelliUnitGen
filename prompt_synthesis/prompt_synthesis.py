# -*- coding: utf-8 -*-
"""
Created on Thu Apr 10 16:18:09 2025

@author: An Wen
"""

import re

# **示例 Java 代码及其 JUnit 5 测试用例**
sample_java_code = """
public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
}
"""

sample_test_case = """
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.Test;

public class CalculatorTest {
    @Test
    public void testAdd() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.add(2, 3));
    }
}
"""

java_prompt_synthesis_result = []



def get_step1_prompt(pre_process_java_code, static_common):

    # print("==============================================================",static_common)
    # 安全兜底：如果返回 None，使用空结构
    if static_common is None:
        print("⚠️ 警告：静态分析未返回任何结构信息（返回 None），请检查代码是否为空或格式错误。")
        static_common = {
            "classes": [],
            "functions": [],
            "function_details": [],
            "conditions": [],
            "exceptions": []
        }

    # 结构提取
    classes = static_common.get("classes", [])
    functions = static_common.get("functions", [])
    function_details = static_common.get("function_details", [])
    conditions = static_common.get("conditions", [])
    exceptions = static_common.get("exceptions", [])

    # 安全处理
    class_line = ', '.join(classes) if classes else '未提取到'
    function_names = [f[0] for f in functions] if functions else []
    function_line = f"{len(functions)}，方法名: {function_names or '无方法'}"


    # 组装 Prompt
    prompt_step1 = f"""以下是对 Java 代码结构的静态分析结果：
- 类名: {class_line}
- 方法数量: {function_line}
- 每个方法的输入参数和修饰符: {function_details}
- 判定节点: {conditions}
- 异常处理结构: {exceptions}

Java 代码如下：########
{pre_process_java_code}
########
"""
    print("【结构信息 Prompt】\n", prompt_step1) 
    java_prompt_synthesis_result.append({"role": "user", "content": prompt_step1})

    # return prompt_step1

def get_step2_prompt(pre_process_java_code, dependency_classes, method_signature):
    
    # 提取构造函数信息
    constructors = {}
    for class_name, methods in method_signature.items():
        # 检查方法签名是否包含类名作为方法名（构造函数的特征）
        class_constructors = [m for m in methods if f" {class_name}(" in m]
        if class_constructors:
            constructors[class_name] = class_constructors

    # 组装 Prompt
    prompt_step2 = f"""
以下是对Java代码依赖关系的分析结果：
依赖的类：{dependency_classes}
依赖的类的方法签名：{method_signature}
依赖的类的构造函数：{constructors}
"""
    print("【依赖关系 Prompt】\n", prompt_step2)
    java_prompt_synthesis_result.append({"role": "user", "content": prompt_step2})


def get_test_class_name(pre_process_java_code):
    """
    从 Java 源码中提取类名或接口名，并生成对应的测试类文件名。
    支持识别包含泛型参数的接口名称，如 Converter<T, E extends Exception>
    :param pre_process_java_code: 字符串形式的 Java 代码
    :return: 测试类的文件名（如 MyClassTest.java）
    """
    # 匹配 class 或 interface 名称，包括泛型参数
    pattern = r'(?:class|interface)\s+(\w+)(?:<[^>]+>)?'
    match = re.search(pattern, pre_process_java_code)
    class_name = match.group(1) if match else "UnknownClass"
    test_class_name = f"{class_name}Test.java"
    return test_class_name

# 语句覆盖
def statement_coverage_prompt_synthesis(pre_process_java_code,static_common, java_analysis_result, dependency_classes, method_signature, test_class_name):
    # 系统提示
    print("============================step 0.1:系统提示====================================")
    prompt_step0_1 = f"你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"
    print("【系统提示 Prompt】",prompt_step0_1)
    java_prompt_synthesis_result.append({"role": "system", "content": prompt_step0_1})
                                         
    print("============================step 0.2:系统提示====================================") 
    # prompt_step0_2 = f"你是一名经验丰富的Java开发工程师，擅长编写高质量的JUnit测试用例。"
    # prompt_step0_2 = f"你是计算机领域，尤其是软件工程方向的专家。请根据我下面给出的一系列的提示(Prompt)帮助我。"
    prompt_step0_2 = f"你是一位专注于软件测试和静态分析领域的系统分析师，请根据下面一系列的提示（prompt）帮助我。"
    print("【系统提示 Prompt】",prompt_step0_2)
    java_prompt_synthesis_result.append({"role": "system", "content": prompt_step0_2})
    
    # 了解代码结构
    print("============================step 1:了解代码结构====================================") 
    get_step1_prompt(pre_process_java_code, static_common)
    # 了解依赖关系
    print("============================step 2:了解依赖关系====================================") 
    get_step2_prompt(pre_process_java_code, dependency_classes, method_signature)
    # 分析可执行语句
    print("============================ Step 3: 分析可执行语句 ===============================")
    total_statements = java_analysis_result.get("total_executable", 0)
    # executable_statements = java_analysis_result.get("executable_statements", 0)
    prompt_step3 = f"请你根据上述的代码结构及可执行语句条数{total_statements}条，列出该方法中所有的可执行语句（不包括声明、注释、空行），并编号。"
    print("【分析可执行语句 Prompt】",prompt_step3)
    java_prompt_synthesis_result.append({"role": "user", "content": prompt_step3})

    # 分析执行条件
    print("========================== Step 4: 分析执行条件 ==============================")
    prompt_step4 = f"请根据你刚列出的可执行语句的执行条件，为每条语句设计至少一个输入参数组合，以确保该语句能被执行到。"
    print("【分析执行条件 Prompt】",prompt_step4)
    java_prompt_synthesis_result.append({"role": "user", "content": prompt_step4})
    
    # 生成测试用例
    print("========================== Step 5: 生成测试用例 ==============================")
    prompt_step5 = f"""请根据上述分析,参考以下示例及其测试用例，并根据其格式及结构：########
{sample_java_code}
m
{sample_test_case}
########

为以下 Java 代码生成 JUnit 5 测试用例，测试用例类的类名为{test_class_name},确保100%语句覆盖：
########
{pre_process_java_code}
########
要求：
(1) 在生成单元测试用例时，请避免调用重载方法时将 Null 作为参数传入，优先选择明确类型的参数，或使用替代值来避免编译错误。
(2) 在生成测试代码时，如果目标类的构造函数是 private 或 protected，请不要直接使用 new ClassName(...) 创建对象，而是应当使用该类提供的 Builder 模式进行实例化。例如，应使用 ClassName.Builder builder = new ClassName.Builder(); 并调用相关 addXxx(...) 或 setXxx(...) 方法设置属性，最后通过 builder.build() 获取对象。请根据参数推断适用的 builder 方法，确保代码合法且可编译。
(3) 在生成测试代码时，严格禁止引用任何非 public 的字段、方法或构造器。特别是像 `DEFAULT`、`EMPTY`、`INSTANCE` 等类中的默认静态字段，若它们不是 public，不得使用。请始终通过公开 API 或 Builder 模式显式构造对象，例如：`new ClassName.Builder().setXxx(...).build();`。所有测试对象都必须由用户可访问的构造流程生成，不得引用内部常量。
(4) 禁止在测试代码中使用 (T) 这样的泛型强制类型转换。所有类型转换必须使用明确的、已声明的具体类型。
(5) 请确保生成的测试用例符合目标方法的真实行为逻辑，若方法返回 null 表示"不支持"而非抛异常，请使用 assertNull，不要强行使用 assertThrows。
(6) 请确保生成的测试用例中为所有使用到的类添加正确的 import 语句，包括标准库类（如 List, ArrayList, Map, Properties 等）和项目类（如 CommandLine, ParseException 等）。不得遗漏任何 import，避免出现 类无法解析 或 未导入 的编译错误。
(7) 严禁在测试用例中调用 SimpleDateFormat.parse(...) 时传入与预设格式不匹配的字符串。如果需要测试格式错误的情况，必须通过 assertThrows(ParseException.class, ...) 显式断言异常抛出，避免测试失败。
(8) 不要使用 Mockito 或任何 mock 工具，避免对 final 类、系统类、第三方库进行 mock；测试对象必须使用真实数据或真实实例构造，避免任何模拟行为。
"""
    print("【生成测试用例 Prompt】",prompt_step5)
    java_prompt_synthesis_result.append({"role": "user", "content": prompt_step5})


# 条件覆盖
def condition_coverage_prompt_synthesis(pre_process_java_code,static_common, java_analysis_result, dependency_classes, method_signature, test_class_name):
    # 系统提示
    print("============================step 0:系统提示====================================") 
    prompt_step0 = f"你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"
    print("【系统提示 Prompt】",prompt_step0)
    java_prompt_synthesis_result.append(prompt_step0)
    # 了解代码结构
    print("============================step 1:了解代码结构====================================") 
    get_step1_prompt(pre_process_java_code, static_common)
    # 了解依赖关系
    print("============================step 2:了解依赖关系====================================") 
    get_step2_prompt(pre_process_java_code, dependency_classes, method_signature)
    
    # 提取独立条件
    print("======================== Step 3: 提取布尔表达式中的独立条件 =========================")
    conditions_count = java_analysis_result.get("conditions_count",0)
    conditions_condition = java_analysis_result.get("conditions_condition",0)
    prompt_step3 = f"请分析代码，并根据上述代码结构及解析出的{conditions_count}个布尔表达式\n{conditions_condition}\n提取出其中的独立条件。"
    print("【独立条件 Prompt】\n", prompt_step3)
    java_prompt_synthesis_result.append(prompt_step3)

    # 分析 
    print("=========================step 4:对独立条件进行分析====================================")
    prompt_step4 = f"请针对上述提取出的独立条件列出其为True和False时的方法行为差异，说明如何通过不同输入触发这些分支。"
    print("【分析独立条件 Prompt】\n", prompt_step4)
    java_prompt_synthesis_result.append(prompt_step4)
    
    # 生成测试用例
    print("========================== Step 5: 生成测试用例 ==============================")
    prompt_step5 = f"""请根据上述分析,参考以下示例及其测试用例，并根据其格式及结构：########
{sample_java_code}

{sample_test_case}
########

为以下 Java 代码生成 JUnit 5 测试用例，测试用例类的类名为{test_class_name},确保每个布尔条件在True和False状态下至少执行一次：
########
{pre_process_java_code}
########
要求：
(1) 在生成单元测试用例时，请避免调用重载方法时将 Null 作为参数传入，优先选择明确类型的参数，或使用替代值来避免编译错误。
(2) 在生成测试代码时，如果目标类的构造函数是 private 或 protected，请不要直接使用 new ClassName(...) 创建对象，而是应当使用该类提供的 Builder 模式进行实例化。例如，应使用 ClassName.Builder builder = new ClassName.Builder(); 并调用相关 addXxx(...) 或 setXxx(...) 方法设置属性，最后通过 builder.build() 获取对象。请根据参数推断适用的 builder 方法，确保代码合法且可编译。
"""
    print("【生成测试用例 Prompt】",prompt_step5)
    java_prompt_synthesis_result.append(prompt_step5)

# 分支覆盖
def branch_coverage_prompt_synthesis(pre_process_java_code,static_common, java_analysis_result, dependency_classes, method_signature, test_class_name):
    # 系统提示
    print("============================step 0:系统提示====================================") 
    prompt_step0 = f"你是一名经验丰富的Java开发工程师，擅长编写高质量的JUnit测试用例。"
    print("【系统提示 Prompt】",prompt_step0)
    java_prompt_synthesis_result.append(prompt_step0)
    # 了解代码结构
    print("============================step 1:了解代码结构====================================") 
    get_step1_prompt(pre_process_java_code, static_common)
    # 了解依赖关系
    print("============================step 2:了解依赖关系====================================") 
    get_step2_prompt(pre_process_java_code, dependency_classes, method_signature)
    
    # 分析触发条件
    print("============================step 3:分析触发条件====================================")    
    branch_count = java_analysis_result.get("branch_count",0)
    branch_structures = java_analysis_result.get("branch_structures",0)
    prompt_step3 = f"请根据源代码及{branch_count}个控制流分支\n这些控制流分支结构为\n{branch_structures}\，请分析每个分支的触发条件。"
    print("【分析触发条件 Prompt】\n", prompt_step3)
    java_prompt_synthesis_result.append(prompt_step3)
    
    # 生成测试用例
    print("========================== Step 4: 生成测试用例 ==============================")
    prompt_step4 = f"""请根据上述分析,参考以下示例及其测试用例，并根据其格式及结构：########
{sample_java_code}

{sample_test_case}
########

为以下 Java 代码生成 JUnit 5 测试用例，测试用例类的类名为{test_class_name},确保每个布尔条件在True和False状态下至少执行一次：
########
{pre_process_java_code}
########
"""
    print("【生成测试用例 Prompt】",prompt_step4)
    java_prompt_synthesis_result.append(prompt_step4)


# 决策覆盖
def decision_coverage_prompt_synthesis(pre_process_java_code,static_common, java_analysis_result, dependency_classes, method_signature, test_class_name):
    # 系统提示
    print("============================step 0:系统提示====================================") 
    prompt_step0 = f"你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"
    print("【系统提示 Prompt】",prompt_step0)
    java_prompt_synthesis_result.append(prompt_step0)
    # 了解代码结构
    print("============================step 1:了解代码结构====================================") 
    get_step1_prompt(pre_process_java_code, static_common)
    # 了解依赖关系
    print("============================step 2:了解依赖关系====================================") 
    get_step2_prompt(pre_process_java_code, dependency_classes, method_signature)
    
    # 提供输入
    print("============================step 3:分析不同情况的输入====================================")    
    decision_points_count = java_analysis_result.get("decision_points_count",0)
    conditions_decision = java_analysis_result("branch_structures",0)
    prompt_step3 = f"请为分析出的{decision_points_count}个决策语句\n{conditions_decision}提供至少一组使其为True的输入，以及一组使其为False的输入。"
    print("【提供输入 Prompt】\n", prompt_step3)
    java_prompt_synthesis_result.append(prompt_step3)

    # 生成测试用例
    print("========================== Step 4: 生成测试用例 ==============================")
    prompt_step4 = f"""请根据上述分析,参考以下示例及其测试用例，并根据其格式及结构：########
{sample_java_code}

{sample_test_case}
########

为以下 Java 代码生成 JUnit 5 测试用例，测试用例类的类名为{test_class_name},包含必要的断言逻辑和输入构造语句：
########
{pre_process_java_code}
########
"""
    print("【生成测试用例 Prompt】",prompt_step4)
    java_prompt_synthesis_result.append(prompt_step4)
    
# 路径覆盖
def path_coverage_prompt_synthesis(pre_process_java_code, static_common, dependency_classes, method_signature, test_class_name):
    # 系统提示
    print("============================step 0:系统提示====================================") 
    prompt_step0 = f"你是一个善于详细解释并保持条理清晰的助手，风格亲切，回答内容应包含细致推理步骤和完整解答。"
    print("【系统提示 Prompt】",prompt_step0)
    java_prompt_synthesis_result.append(prompt_step0)
    # 了解代码结构
    print("============================step 1:了解代码结构====================================")    
    get_step1_prompt(pre_process_java_code, static_common)
    # 了解依赖关系
    print("============================step 2:了解依赖关系====================================") 
    get_step2_prompt(pre_process_java_code, dependency_classes, method_signature)
    
    # 计算环路复杂度
    print("============================step 3:计算环路复杂度====================================")   
    conditions = static_common.get('conditions',0)
    prompt_step3 = f"请你根据上述分析出的判定节点个数{conditions}及公式：环路复杂度=判定节点+1  计算出环路复杂度"
    print("【环路复杂度 Prompt】\n", prompt_step3)
    java_prompt_synthesis_result.append(prompt_step3)
    
    # 设计触发条件
    print("============================step 4:设计触发条件====================================") 
    prompt_step4 = f"请根据上述计算出的环路复杂度为每条路径设计触发条件"
    print("【设计触发条件 Prompt】\n", prompt_step4)
    java_prompt_synthesis_result.append(prompt_step4)
    
    # 生成测试用例
    print("========================== Step 5: 生成测试用例 ==============================")
    prompt_step5 = f"""请根据上述分析,参考以下示例及其测试用例，并根据其格式及结构：########
{sample_java_code}

{sample_test_case}
########

根据公式 ：环路复杂度=路径的数量，其中环路复杂度为，为以下 Java 代码生成 JUnit 5 测试用例，测试用例类的类名为{test_class_name},确保所有列出的路径都能被至少执行一次，并包括异常路径与极端情况：
########
{pre_process_java_code}
########
"""
    print("【生成测试用例 Prompt】",prompt_step5)
    java_prompt_synthesis_result.append(prompt_step5)
       
def prompt_synthesis(pre_process_java_code, static_common, java_analysis_result, dependency_classes, method_signature, select):
    test_class_name = get_test_class_name(pre_process_java_code)
    if select == 1:
        statement_coverage_prompt_synthesis(pre_process_java_code, static_common, java_analysis_result, dependency_classes, method_signature, test_class_name)
    if select == 2:
        condition_coverage_prompt_synthesis(pre_process_java_code, static_common, java_analysis_result, dependency_classes, method_signature, test_class_name)
    if select == 3:
        branch_coverage_prompt_synthesis(pre_process_java_code, static_common, java_analysis_result, dependency_classes, method_signature, test_class_name)
    if select == 4:
        decision_coverage_prompt_synthesis(pre_process_java_code, static_common, java_analysis_result, dependency_classes, method_signature, test_class_name)
    if select == 5:
        path_coverage_prompt_synthesis(pre_process_java_code, static_common, dependency_classes, method_signature, test_class_name)
    return java_prompt_synthesis_result,test_class_name