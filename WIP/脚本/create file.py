import argparse
import os

def create_gfx_files(identifier):
	"""根据标识符创建指定格式的gfx文件"""
	# 构建文件名
	advisor_file = f"{identifier}_advisor.gfx"
	character_file = f"{identifier}_character.gfx"
	
	# 定义文件内容
	advisor_content = [
		"spriteTypes = {",
		"",
		"\tspriteType = {",
		f"\t\tname = \"GFX_idea_advisor_{identifier}_\"",
		f"\t\ttexturefile = \"gfx/interface/ideas/advisors/{identifier}/idea_advisor_{identifier}_.dds\"",
		"\t}",
		"}"
	]
	
	character_content = [
		"spriteTypes = {",
		"",
		"\tspriteType = {",
		f"\t\tname = \"GFX_Portrait_{identifier}_\"",
		f"\t\ttexturefile = \"gfx/leaders/{identifier}/Portrait_{identifier}_.dds\"",
		"\t}",
		"}"
	]

	# 检查文件是否存在
	existing_files = []
	for file_path in [advisor_file, character_file]:
		if os.path.exists(file_path):
			existing_files.append(file_path)
	
	# 处理覆盖确认
	if existing_files:
		print(f"检测到以下文件已存在:")
		for path in existing_files:
			print(f"  - {path}")
		confirm = input("是否覆盖现有文件？(y/N): ").strip().lower()
		if confirm != 'y':
			print("操作已取消")
			return
	
	try:
		# 写入advisor文件
		with open(advisor_file, 'w+', encoding='utf-8') as f:
			for i in advisor_content:
				f.write(i)
				f.write("\n")
		# 写入character文件
		with open(character_file, 'w+', encoding='utf-8') as f:
			for j in character_content:
				f.write(j)
				f.write("\n")
		
		print(f"成功创建文件:")
		print(f"  {advisor_file} ({len(advisor_content)} 字符)")
		print(f"  {character_file} ({len(character_content)} 字符)")
		
	except IOError as e:
		print(f"文件操作失败: {str(e)}")
		raise

def main():
	# 创建命令行解析器
	parser = argparse.ArgumentParser(
		description="根据输入参数生成特定格式的gfx文件",
		formatter_class=argparse.ArgumentDefaultsHelpFormatter
	)
	
	# 添加位置参数
	parser.add_argument('identifier', 
						type=str,
						help="用于生成文件名的唯一标识符")
	
	# 解析参数
	args = parser.parse_args()
	
	# 执行文件创建
	create_gfx_files(args.identifier)

if __name__ == "__main__":
	main()