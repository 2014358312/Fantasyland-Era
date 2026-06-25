from pathlib import Path
from typing import List, Tuple, Dict
import re

def scan_image_files(
	root: str | Path = ".",
	extensions: frozenset[str] = frozenset({".dds", ".png"}),
) -> Tuple[List[List[str]], str]:
	"""
	递归扫描目录下的 dds/png 文件

	返回:
		files:
			[
				[相对路径（不含文件名）, 文件名（无后缀）, 后缀（不含点）],
				...
			]
		current_dir_name:
			脚本所在当前目录的目录名
	"""
	root_path = Path(root).resolve(strict=False)
	files: List[List[str]] = []

	# ★ 单遍递归扫描
	for p in root_path.rglob("*"):
		if not p.is_file():
			continue

		suffix = p.suffix.lower()
		if suffix not in extensions:
			continue

		rel = p.relative_to(root_path)
		rel_parent = str(rel.parent) if rel.parent != Path(".") else "."

		files.append([
			rel_parent,
			p.stem,
			suffix.lstrip("."),
		])

	# 脚本所在当前目录名
	current_dir_name = Path.cwd().name

	# ---------- 控制台输出 ----------
	print("📁 当前目录名:", current_dir_name)
	print("📄 扫描到的图像文件：")
	for item in files:
		print(f"  • 路径: {item[0]:<20} | 名称: {item[1]:<15} | 后缀: {item[2]}")

	return files, current_dir_name

def replace_alternate(text: str, max_n: int = 10) -> str:
    """
    批量替换 alternateN" 和 alternate" 为 altN" 和 alt"
    使用正则表达式，避免 str.translate() 的长度限制
    """
    # 降序生成替换规则
    patterns = []
    for i in range(max_n, 0, -1):
        patterns.append((f'alternate{i}"', f'alt{i}"'))
    patterns.append(('alternate"', 'alt"'))

    # 使用正则替换（确保长匹配优先）
    for old, new in patterns:
        text = re.sub(re.escape(old), new, text)

    return text

def replace_alternate_in_file_read(
    file_path: str,
    max_n: int = 10,
    encoding: str = "utf-8"
) -> None:
    with open(file_path, "r", encoding=encoding) as f:
        content = f.read()

    new_content = replace_alternate(content, max_n)

    with open(file_path, "w", encoding=encoding) as f:
        f.write(new_content)

def replace_alternate_in_file_readline(
    file_path: str,
    max_n: int = 10,
    encoding: str = "utf-8"
) -> None:
    with open(file_path, "r", encoding=encoding) as f:
        lines = []
        while True:
            line = f.readline()
            if not line:
                break
            lines.append(replace_alternate(line, max_n))

    with open(file_path, "w", encoding=encoding) as f:
        f.writelines(lines)

def replace_alternate_in_file_readlines(
    file_path: str,
    max_n: int = 10,
    encoding: str = "utf-8"
) -> None:
    with open(file_path, "r", encoding=encoding) as f:
        lines = f.readlines()

    new_lines = [replace_alternate(line, max_n) for line in lines]

    with open(file_path, "w", encoding=encoding) as f:
        f.writelines(new_lines)

if __name__ == "__main__":
	fileGFX = []
	image_files, cur_dir = scan_image_files(".")
	path0 = "gfx/leaders"
	path = path0 + "/" + cur_dir
	for i in image_files:
		i[0] = path + "/" + i[0]
		i[0] = i[0].replace(".", "")
	with open("images.gfx", "w+", encoding="utf-8") as f:
		f.write("SpriteTypes = {")
		for i in range(len(image_files)):
			fileGFX.append(f"""
				SpriteType = {{
					name = "GFX_{image_files[i][1]}"
					texturefile = "{image_files[i][0]}/{image_files[i][1]}.{image_files[i][2]}"
				}}
			""".replace("\t\t\t", "").replace("//", "/"))
		for i in fileGFX:
			f.write(i)
		f.write("}")
	replace_alternate_in_file_readline("images.gfx")