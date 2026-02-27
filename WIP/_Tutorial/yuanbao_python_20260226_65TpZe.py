import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import re
import pyradox

class CharacterCreatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("角色ID管理系统 - 马年专用")
        self.root.geometry("500x400")
        
        # 设置窗口图标（如果存在）
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        
        # 主框架
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 标题
        title_label = ttk.Label(main_frame, text="角色信息录入系统", 
                               font=("微软雅黑", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # 创建输入字段
        self.create_input_fields(main_frame)
        
        # 创建按钮
        self.create_buttons(main_frame)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪 - 请填写所有字段")
        status_bar = ttk.Label(root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        # 配置网格权重
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
    
    def create_input_fields(self, parent):
        """创建输入字段"""
        labels = ["角色ID (idea_token):", "角色名字:", "特质:", "职位称呼:"]
        self.entries = {}
        
        for i, label_text in enumerate(labels):
            # 标签
            label = ttk.Label(parent, text=label_text, font=("宋体", 10))
            label.grid(row=i+1, column=0, sticky=tk.W, pady=5)
            
            # 输入框
            entry = ttk.Entry(parent, width=40)
            entry.grid(row=i+1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
            
            # 存储引用
            field_name = label_text.split(" ")[0].replace("(", "").replace(":", "")
            self.entries[field_name] = entry
            
            # 绑定输入事件
            entry.bind("<KeyRelease>", self.update_status)
    
    def create_buttons(self, parent):
        """创建按钮"""
        # 执行按钮
        self.execute_btn = ttk.Button(parent, text="执行", command=self.execute_operations,
                                    state=tk.DISABLED)
        self.execute_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # 清除按钮
        clear_btn = ttk.Button(parent, text="清除", command=self.clear_fields)
        clear_btn.grid(row=6, column=0, pady=5, sticky=tk.E)
        
        # 浏览文件按钮
        browse_btn = ttk.Button(parent, text="浏览character文件夹", 
                               command=self.browse_character_dir)
        browse_btn.grid(row=6, column=1, pady=5, sticky=tk.W, padx=(10, 0))
    
    def update_status(self, event=None):
        """更新状态和按钮状态"""
        all_filled = all(entry.get().strip() for entry in self.entries.values())
        self.execute_btn.config(state=tk.NORMAL if all_filled else tk.DISABLED)
        
        if all_filled:
            self.status_var.set("就绪 - 可以执行")
        else:
            self.status_var.set("请填写所有字段")
    
    def clear_fields(self):
        """清除所有输入字段"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.status_var.set("已清除所有字段")
        self.execute_btn.config(state=tk.DISABLED)
    
    def browse_character_dir(self):
        """浏览character文件夹"""
        try:
            character_dir = "../../common/characters/"
            if os.path.exists(character_dir):
                os.startfile(os.path.abspath(character_dir))
                self.status_var.set(f"已打开文件夹: {character_dir}")
            else:
                messagebox.showwarning("警告", f"文件夹不存在: {character_dir}")
        except Exception as e:
            messagebox.showerror("错误", f"无法打开文件夹: {e}")
    
    def execute_operations(self):
        """执行所有操作"""
        try:
            # 获取输入值
            idea_token = self.entries["角色ID"].get().strip()
            name = self.entries["角色名字"].get().strip()
            trait = self.entries["特质"].get().strip()
            desc = self.entries["职位称呼"].get().strip()
            
            if not all([idea_token, name, trait, desc]):
                messagebox.showerror("错误", "所有字段都必须填写！")
                return
            
            # 第一步：检查角色ID是否已存在
            self.check_character_id(idea_token, name)
            
            # 第二步：写入zzz_FE_dummy_secondary.txt文件
            #self.write_to_secondary_file(idea_token)
            
            # 第三步：打开_vice.txt文件（留白）
            #self.open_vice_file()
            
            # 第四步：打开FE_secondary.gfx文件（留白）
            #self.open_gfx_file()
            
            # 第五步：显示完成提示
            self.show_completion_dialog()
            
        except Exception as e:
            messagebox.showerror("执行错误", f"执行过程中发生错误:\n{str(e)}")
            self.status_var.set(f"错误: {str(e)}")
    
    def check_character_id(self, idea_token, name):
        """第一步：检查角色ID是否已存在"""
        wp=False
        try:
            character_dir = "../../common/characters/"
            
            file_name = f"{idea_token[:3]}.txt"
            file_path = os.path.join(character_dir, file_name)
            if not os.path.isfile(file_path):
                with open(file_path, 'w+', encoding='utf-8') as f:
                    f.write("characters = {\n}")
            
            # 遍历所有txt文件
            for filename in os.listdir(character_dir):
                if filename.endswith('.txt'):
                    filepath = os.path.join(character_dir, filename)
                    with open(filepath, 'r+', encoding='utf-8') as f:
                        context = f.read()
                    result = pyradox.parse(context)
                    charactersNode = result["characters"]
                    charactersList = [k for k, v in charactersNode.items()]
                    if idea_token in charactersList:
                        characterNode = charactersNode[idea_token]
                        try:
                            characterNode.append("advisor", "123", in_group = True)
                        except Exception as e:
                            pass
                        characterAdvisorList = [v for k, v in characterNode.items() if k == "advisor"]
                        characterAdvisorList.append(characterAdvisorList[0])
                        #for i in characterAdvisorList:
                        #    print(i)
                        characterHoGNode = characterAdvisorList[-1]
                        #print(characterHoGNode)
                        characterHoGNode["slot"] = "head_of_government_character"
                        characterHoGNode["idea_token"] = f"{idea_token}_character"
                        characterHoGNode["available"] = {"#": "#"}
                        characterHoGAvailableNode = characterHoGNode["available"]
                        characterHoGAvailableNode["no_head_of_gov_trigger"] = "yes"
                        characterHoGNode["traits"] = {"#": "#"}
                        print(characterNode)
                        wp=True
                charactersList.clear()
                del result
            if not wp:
                with open(file_path, 'r+', encoding='utf-8') as f:
                    context = f.read()
                result = pyradox.parse(context)
                charactersNode = result["characters"]
                charactersNode[idea_token] = {"name": name}
                characterNode = charactersNode[idea_token]
                characterNode["portraits"] = {"#": "#"}
                characterPortraitNode = characterNode["portraits"]
                characterPortraitNode["civilian"] = {"#": "#"}
                characterPortraitCivilianNode = characterPortraitNode["civilian"]
                characterPortraitCivilianNode["large"] = f"GFX_Portrait_{idea_token}"
                characterPortraitCivilianNode["small"] = f"GFX_idea_advisor_{idea_token}"
                characterPortraitNode["army"] = {"#": "#"}
                characterPortraitArmyNode = characterPortraitNode["army"]
                characterPortraitArmyNode["large"] = f"GFX_Portrait_{idea_token}"
                characterPortraitArmyNode["small"] = f"GFX_idea_advisor_{idea_token}"
                with open(file_path, 'w+', encoding='utf-8') as f:
                    f.write(str(result))
                with open(file_path, 'r+', encoding='utf-8') as f:
                    lines = f.readlines()
                target_string="# = \"#\""
                filtered_lines = [line for line in lines if target_string not in line]
                with open(file_path, 'w+', encoding='utf-8') as f:
                    f.writelines(filtered_lines)
                
            
        except Exception as e:
            raise Exception(f"检查角色ID时出错: {e}")
    
    def write_to_secondary_file(self, idea_token):
        """第二步：写入zzz_FE_dummy_secondary.txt文件"""
        try:
            filepath = "../../common/ideas/zzz_FE_dummy_secondary.txt"
            
            # 确保目录存在
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            # 读取文件内容
            with open(filepath, 'r+', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 在倒数第二行插入新内容
            insert_index = max(0, len(lines) - 2)
            new_lines = [
                f'GFX_Portort_{idea_token} = {{}}\n',
                f'SECONDARY_{idea_token}_name = {{}}\n',
                f'SECONDARY_{idea_token}_trait = {{}}\n',
                f'SECONDARY_{idea_token}_desc = {{}}\n',
                '\n'  # 添加空行分隔
            ]
            
            # 插入新行
            lines[insert_index:insert_index] = new_lines
            
            # 写入文件
            with open(filepath, 'w+', encoding='utf-8') as f:
                f.writelines(lines)
            
            self.status_var.set(f"已更新文件: {os.path.basename(filepath)}")
            
        except FileNotFoundError:
            # 如果文件不存在，创建它
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# 自动生成的文件\n")
                f.write(f"# 角色ID: {idea_token}\n\n")
                f.write(f'GFX_Portort_{idea_token} = {{}}\n')
                f.write(f'SECONDARY_{idea_token}_name = {name}\n')
                f.write(f'SECONDARY_{idea_token}_trait = {trait}\n')
                f.write(f'SECONDARY_{idea_token}_desc = {desc}\n')
            self.status_var.set(f"已创建文件: {os.path.basename(filepath)}")
        except Exception as e:
            raise Exception(f"写入文件时出错: {e}")
    
    def open_vice_file(self):
        """第三步：打开_vice.txt文件（留白）"""
        try:
            filepath = "../../common/ideas/_vice.txt"
            if os.path.exists(filepath):
                self.status_var.set(f"已打开文件: {os.path.basename(filepath)}")
                # 这里可以添加打开文件的代码
                # 例如：os.startfile(filepath)
            else:
                self.status_var.set(f"文件不存在: {os.path.basename(filepath)}")
        except Exception as e:
            self.status_var.set(f"打开vice文件时出错: {e}")
    
    def open_gfx_file(self):
        """第四步：打开FE_secondary.gfx文件（留白）"""
        try:
            filepath = "../../interface/FE_secondary.gfx"
            if os.path.exists(filepath):
                self.status_var.set(f"已打开文件: {os.path.basename(filepath)}")
                # 这里可以添加打开文件的代码
                # 例如：os.startfile(filepath)
            else:
                self.status_var.set(f"文件不存在: {os.path.basename(filepath)}")
        except Exception as e:
            self.status_var.set(f"打开gfx文件时出错: {e}")
    
    def show_completion_dialog(self):
        """第五步：显示完成提示对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("操作完成")
        dialog.geometry("300x150")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # 使对话框居中
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() - dialog.winfo_width()) // 2
        y = self.root.winfo_y() + (self.root.winfo_height() - dialog.winfo_height()) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # 消息标签
        msg_label = ttk.Label(dialog, text="操作已成功执行！", 
                             font=("微软雅黑", 12))
        msg_label.pack(pady=20)
        
        # 确定并退出按钮
        ok_btn = ttk.Button(dialog, text="确定并退出", 
                           command=lambda: [dialog.destroy(), self.root.quit()])
        ok_btn.pack(pady=10)
        
        # 只关闭对话框按钮
        close_btn = ttk.Button(dialog, text="只关闭此窗口", 
                              command=dialog.destroy)
        close_btn.pack(pady=5)

def main():
    root = tk.Tk()
    app = CharacterCreatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()