# IntelliUnitGen

IntelliUnitGen is a large language model-based Java unit test case generation tool that automatically generates high-quality unit test cases based on Java code.

## Prerequisites

1. Obtain OpenAI API Key
   - Visit the [OpenAI API Platform](https://platform.openai.com/api-keys) to obtain your API Key
   - Ensure you have sufficient API call quota

2. API Key Input During Program Execution
   - Upon first execution (when running AutoUnitGen.py), you will be prompted to enter your API Key in the console
   - The API Key will be stored in a temporary file during program execution
   - The temporary file will be automatically deleted upon program termination to ensure security
   - The API Key must be re-entered for subsequent program executions

## Key Features

- Support for multiple test coverage types:
  - Statement Coverage
  - Condition Coverage
  - Branch Coverage
  - Decision Coverage
  - Path Coverage
- Automatic code structure and dependency analysis
- Intelligent test case generation
- Automatic compilation and runtime error correction
- Private method testing support
- Automatic generic type handling

## Usage Instructions

1. Ensure Python 3.8 or higher is installed
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute the program:
   ```bash
   python AutoUnitGen.py
   ```
4. Follow the prompts to select test coverage type and input Java code file or directory

## Important Notes

- Ensure the security of your API Key and do not share it with others
- It is recommended to use the GPT-4 model for test case generation to achieve optimal results
- The program automatically handles private methods and generic types in the code
- If generated test cases fail to compile or run, the program will automatically attempt to fix them

## Dependencies

- Python 3.8+
- OpenAI API
- Java Development Kit (JDK)
- Maven

## License

MIT License
