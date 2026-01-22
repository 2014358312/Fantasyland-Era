import tkinter as tk
from tkinter import filedialog
import pyradox

def wait_for_keypress():
    """
    等待用户按任意键继续（实际是回车键，为跨平台兼容性）
    """
    input("\n按Enter键退出程序...")

def select_txt_file():
    """
    通过资源管理器选择txt文件，返回文件路径。
    如果用户取消选择，返回None。
    """
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(
        title="选择文本文件",
        filetypes=[("Text files", "*.txt")]  # 限制为txt文件
    )
    root.destroy()  # 清理tkinter窗口
    return file_path if file_path else None

def read_file_content(file_path):
    """
    读取文件内容并返回字符串。
    自动处理编码和文件关闭。
    """
    try:
        with open(file_path, 'r+', encoding='utf-8') as file:
            content = file.read()
        return content
    except UnicodeDecodeError:
        # 尝试其他常见编码
        with open(file_path, 'r+', encoding='gbk') as file:
            content = file.read()
        return content
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return None

def starts_with_hash_alternative(text):
    """
    使用startswith方法的替代实现
    """
    if not text:
        return False
    
    cleaned_text = text.lstrip(' \t')
    return cleaned_text.startswith('#') if cleaned_text else False

def convert_list_to_strings(input_list):
    return [str(element) for element in input_list]

def remove_bom(content):
    """
    手动移除字符串开头的BOM字符 (U+FEFF)
    """
    if content and content[0] == '\ufeff': # 检查第一个字符是否是BOM
        content = content[1:] # 如果是，则从第二个字符开始截取
        print("检测到并已移除BOM头。")
    return content

def main(content):
    """
    主函数，接收文件内容并执行后续逻辑。
    content: 字符串形式的文件内容。
    """
    if content is None:
        print("文件内容为空，无法处理。")
        return
    '''
    # === 以下为留白区域，可在此添加后续代码 ===
    print("文件内容已成功传递到main函数。")
    print("内容预览（前500字符）:")
    print(content[:500] + "..." if len(content) > 500 else content)
    
    # 示例操作：统计行数和字符数
    lines = content.splitlines()
    char_count = len(content)
    print(f"\n基础统计: 行数={len(lines)}, 字符数={char_count}")
    
    # 可在此扩展功能，例如：
    # - 文本处理（分析、过滤、转换）
    # - 数据提取（正则表达式、解析）
    # - 与其他模块交互（数据库、API调用）
    # === 留白结束 ===
    '''
    focusidList = []
    focusidListFilter = []
    if content is not None:
        content = remove_bom(content) # 额外调用去除函数
    result = pyradox.parse(content)
    focus = result["focus_tree"]
    if focus:
        fociList = [v for k, v in focus.items() if k == "focus" or k == "shared_focus" or k == "joint_focus"]
        for i in range(len(fociList)):
            text = [v for k, v in fociList[i].items() if k == "text"]
            if text:
                focusidList.append(text[0])
            else:
                focusidList.extend([v for k, v in fociList[i].items() if k == "id"])
    sharedFociList = [v for k, v in result.items() if k == "focus" or k == "shared_focus" or k == "joint_focus"]
    if sharedFociList:
        for i in range(len(sharedFociList)):
            text = [v for k, v in sharedFociList[i].items() if k == "text"]
            if text:
                focusidList.append(text[0])
            else:
                focusidList.extend([v for k, v in sharedFociList[i].items() if k == "id"])
    focusidList = convert_list_to_strings(focusidList)
    with open("result.yml", "w+", encoding="utf-8") as file:
        file.write("l_simp_chinese:"+"\n")
        for focusid in focusidList:
            file.write(" "+focusid+": \"\""+"\n")
            file.write(" "+focusid+"_desc: \"\""+"\n")
    print("检测到所选取文件存在{}个有效国策id。".format(len(focusidList)))
    print("结果已经保存在当前目录下的result.yml文件中。")

if __name__ == "__main__":
    # 1. 选择文件
    path = select_txt_file()
    if not path:
        print("未选择文件，程序退出。")
        exit()

    # 2. 读取内容
    content = read_file_content(path)
    if content is None:
        print("文件读取失败，程序退出。")
        exit()

    # 3. 传递到主函数
    main(content)

    wait_for_keypress()