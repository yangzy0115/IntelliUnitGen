import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from language_switch.language_switcher import get_text

def show_initial_choice():
    """
    弹窗让用户选择：导入 Java 文件 或 Java 文件目录。
    返回值格式：
    - 成功选择 Java 文件：("file", [文件路径], 文件路径)
    - 成功选择目录：("dir", [所有Java文件路径], 目录路径)
    - 点击取消或关闭窗口：(None, None, None)
    """
    result = {"mode": None, "file_list": None, "path": None}
    user_clicked = {"value": False}  # 外部变量，用于回调中标记操作是否完成

    def choose_file():
        file_path = filedialog.askopenfilename(filetypes=[("Java Files", "*.java")])
        if file_path:
            print(f"\n✅ {get_text('import_java_file_success')}: {file_path}")
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    java_code = f.read()
                    preview = java_code[:500]
                    print(f"🔹 {get_text('code_preview')}:\n")
                    print(preview)
            except Exception as e:
                print(f"❌ {get_text('read_file_error')}: {e}")

            result["mode"] = "file"
            result["file_list"] = [file_path]
            result["path"] = file_path
        else:
            print(f"⚠️ {get_text('no_java_file')}")
        user_clicked["value"] = True
        root.quit()

    def choose_dir():
        folder_path = filedialog.askdirectory(title=get_text('select_java_file_dir'))
        if folder_path:
            java_files = [
                os.path.join(folder_path, f)
                for f in os.listdir(folder_path)
                if f.endswith(".java") and os.path.isfile(os.path.join(folder_path, f))
            ]
            print(f"\n✅ {get_text('Found')} {len(java_files)} {get_text('java_file_count')}")
            for idx, file_path in enumerate(java_files, 1):
                print(f"\n{idx}. {file_path}")
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        preview_lines = lines[:5]  # 取前5行
                        print(f"🔹 {get_text('code_preview_lines')}:")
                        print("".join(preview_lines))
                except Exception as e:
                    print(f"❌ {get_text('read_file_error')}: {e}")

            result["mode"] = "dir"
            result["file_list"] = java_files
            result["path"] = folder_path
        else:
            print(f"⚠️ {get_text('no_dir_selected')}")
        user_clicked["value"] = True
        root.quit()

    # 创建主窗口
    root = tk.Tk()
    root.title(get_text('select_java_file_or_dir'))
    # root.title("Select Java File or Directory")
    root.geometry("360x150")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    label = tk.Label(root, text=get_text('please_select_import_method'), font=("Arial", 12))
    label.pack(pady=10)

    frame = tk.Frame(root)
    frame.pack()

    file_button = tk.Button(frame, text=get_text('select_java_file'), width=15, command=choose_file)
    file_button.pack(side="left", padx=10)

    folder_button = tk.Button(frame, text=get_text('select_dir'), width=15, command=choose_dir)
    folder_button.pack(side="right", padx=10)

    # 窗口关闭时处理
    def on_close():
        print(f"⚠️ {get_text('user_closed_main_window')}")
        root.quit()

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()
    root.destroy()

    if not user_clicked["value"]:
        return None, None, None
    if result["mode"] is None or not result["file_list"]:
        return None, None, None
    return result["mode"], result["file_list"], result["path"]

def show_warning():
    root = tk.Tk()
    root.withdraw()
    result = messagebox.askquestion(get_text('prompt'), get_text('user_closed_main_window_prompt'), icon='warning')
    if result == 'yes':
        print(get_text('user_continue_selecting'))
        return show_initial_choice()
    else:
        print(get_text('user_exit_program'));
        sys.exit()
