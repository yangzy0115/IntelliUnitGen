import os
import re
from typing import Dict, List, Tuple

def extract_classes_from_file(file_path: str, project_path: str) -> List[Tuple[str, str, bool, str]]:
    """
    Extract class names and their package names from a Java file.
    
    Args:
        file_path: Path to the Java file
        project_path: Root path of the project
        
    Returns:
        List of tuples containing (package_name, class_name, is_inner_class, outer_class)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract package name using regex
        package_match = re.search(r'package\s+([\w.]+);', content)
        package_name = package_match.group(1) if package_match else ''
        
        # Find all class definitions
        classes = []
        
        # 1. 首先找到所有类定义，包括内部类
        class_matches = re.finditer(
            r'(?:public\s+)?(?:abstract\s+)?(?:final\s+)?class\s+(\w+)(?:\s+extends\s+[\w.<>]+)?(?:\s+implements\s+[\w.<>,\s]+)?\s*{',
            content
        )
        
        # 2. 记录所有类名和它们的位置
        class_positions = []
        for match in class_matches:
            class_name = match.group(1)
            start_pos = match.start()
            class_positions.append((class_name, start_pos))
        
        # 3. 分析类的嵌套关系
        for i, (class_name, start_pos) in enumerate(class_positions):
            is_inner_class = False
            outer_class = None
            
            # 检查是否是内部类
            if i > 0:  # 不是第一个类
                # 查找这个类之前的最近的大括号位置
                prev_brace_pos = content.rfind('{', 0, start_pos)
                if prev_brace_pos != -1:
                    # 检查这个类是否在另一个类的定义块内
                    for j in range(i-1, -1, -1):
                        prev_class_name, prev_class_pos = class_positions[j]
                        if prev_class_pos < prev_brace_pos:
                            is_inner_class = True
                            outer_class = prev_class_name
                            break
            
            # 跳过匿名内部类（通常包含$符号）
            if '$' not in class_name:
                classes.append((package_name, class_name, is_inner_class, outer_class))
                
        return classes
    except Exception as e:
        print(f"Error processing file {file_path}: {str(e)}")
        return []

def get_project_classes(project_path: str) -> Dict[str, List[str]]:
    """
    Extract all classes and their package names from a Java project.
    
    Args:
        project_path: Root path of the project
        
    Returns:
        Dictionary with package names as keys and lists of class names as values.
        For inner classes, the class name will be in the format "OuterClass.InnerClass"
    """
    package_info = {}
    
    # Walk through the project directory
    for root, _, files in os.walk(project_path):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                classes = extract_classes_from_file(file_path, project_path)
                
                # Add classes to package_info
                for package_name, class_name, is_inner_class, outer_class in classes:
                    if package_name not in package_info:
                        package_info[package_name] = []
                    
                    # 对于内部类，使用 "OuterClass.InnerClass" 格式
                    if is_inner_class and outer_class:
                        full_class_name = f"{outer_class}.{class_name}"
                    else:
                        full_class_name = class_name
                        
                    if full_class_name not in package_info[package_name]:  # Avoid duplicates
                        package_info[package_name].append(full_class_name)
    
    return package_info

if __name__ == "__main__":
    # Example usage
    project_path = (
        r"E:\YAU_BIT\Research\Project Implementation\Project1"
        r"\Sub-project 2\Sub-project 2.1\Sub-project 2.1.1"
        r"\Now\Experiment\0516_commons-cli-master_all"
    )
    package_info = get_project_classes(project_path)
    
    # Print the results
    print("\nProject Classes Information:")
    print("-" * 50)
    if not package_info:
        print("No Java classes found in the project.")
    else:
        for package, classes in sorted(package_info.items()):
            print(f"\nPackage: {package}")
            for class_name in sorted(classes):
                print(f"  - {class_name}") 