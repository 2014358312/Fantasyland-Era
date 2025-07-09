from pathlib import Path
import shutil
import sys
import argparse

def batch_copy_rename(m: str, n: str, input_dir: Path):
    # 创建目标目录（自动处理已存在情况）
    target_dir = Path.cwd() / "renamed_files"
    target_dir.mkdir(exist_ok=True)
    
    # 验证输入目录有效性
    if not input_dir.is_dir():
        raise ValueError(f"无效的输入目录: {input_dir}")

    # 遍历指定目录下的所有文件（不包含子目录）
    for file_path in input_dir.iterdir():
        if file_path.is_file() and file_path.suffix.lower() in ['.png', '.dds']:
            try:
                # 构造新文件名
                new_filename = file_path.stem.replace(m, n) + file_path.suffix
                new_filepath = target_dir / new_filename
                
                # 处理文件名冲突：若存在则添加数字后缀
                counter = 1
                while new_filepath.exists():
                    name, ext = new_filename.split('.', 1)
                    new_filename = f"{name}_{counter}.{ext}"
                    new_filepath = target_dir / new_filename
                    counter += 1
                
                # 执行文件复制（保留元数据）
                shutil.copy2(file_path, new_filepath)
                print(f"✅ 成功复制: {file_path.name} → {new_filename}")
                
            except Exception as e:
                print(f"⚠️ 处理文件 {file_path.name} 时出错: {str(e)}")

if __name__ == "__main__":
    # 命令行参数解析
    parser = argparse.ArgumentParser(
        description="批量复制并重命名指定目录下的PNG/DDS文件",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("m", help="需替换的原字符串")
    parser.add_argument("n", help="替换后的新字符串")
    parser.add_argument(
        "-i", "--input-dir",
        type=str,
        default=Path.cwd(),
        help="输入目录路径（支持绝对/相对路径），默认当前目录"
    )
    
    args = parser.parse_args()
    
    try:
        # 处理路径标准化
        input_path = Path(args.input_dir).resolve(strict=True)
        batch_copy_rename(args.m, args.n, input_path)
    except KeyboardInterrupt:
        print("\n操作已取消")
        sys.exit(1)
    except Exception as e:
        print(f"程序终止: {str(e)}")
        sys.exit(1)