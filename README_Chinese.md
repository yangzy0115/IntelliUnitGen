# IntelliUnitGen

IntelliUnitGen 是一个基于大模型的 Java 单元测试用例生成工具，能够根据 Java 代码自动生成高质量的单元测试用例。

## 使用前准备

1. 获取 OpenAI API Key
   - 访问 [OpenAI API 平台](https://platform.openai.com/api-keys) 获取您的 API Key
   - 确保您有足够的 API 调用额度

2. 运行程序时输入 API Key
   - 首次运行程序(打开AutoUnitGen.py并运行)时，请您在控制台输入 API Key
   - API Key 将在程序运行期间保存在临时文件中
   - 程序退出时会自动删除临时文件，确保安全性
   - 下次运行程序时需要重新输入 API Key

## 功能特点

- 支持多种测试覆盖类型：
  - 语句覆盖
  - 条件覆盖
  - 分支覆盖
  - 决策覆盖
  - 路径覆盖
- 自动分析代码结构和依赖关系
- 智能生成测试用例
- 自动修复编译和运行错误
- 支持私有方法测试
- 自动处理泛型类型

## 使用方法

1. 确保已安装 Python 3.8 或更高版本
2. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. 运行程序：
   ```bash
   python AutoUnitGen.py
   ```
4. 按照提示选择测试覆盖类型和输入 Java 代码文件或目录

## 注意事项

- 请确保您的 API Key 安全，不要分享给他人
- 建议在生成测试用例时使用 GPT-4 模型，以获得更好的生成效果
- 程序会自动处理代码中的私有方法和泛型类型
- 如果生成的测试用例编译或运行失败，程序会自动尝试修复

## 依赖项

- Python 3.8+
- OpenAI API
- Java Development Kit (JDK)
- Maven

## 许可证

MIT License 