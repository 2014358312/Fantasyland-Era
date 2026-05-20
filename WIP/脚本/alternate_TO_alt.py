import os
import sys
import re
import mmap
from contextlib import contextmanager
from typing import Iterator, Optional

@contextmanager
def open_file_smart(filepath: str, mode: str = 'r'):
    """
    智能文件打开上下文管理器，自动处理编码
    """
    if 'b' in mode:
        # 二进制模式
        with open(filepath, mode) as f:
            yield f
    else:
        # 文本模式，尝试多种编码
        encodings = ['utf-8', 'latin-1', 'cp1252', 'utf-16-le', 'utf-16-be']
        last_error = None
        
        for encoding in encodings:
            try:
                with open(filepath, mode, encoding=encoding) as f:
                    yield f
                return
            except UnicodeDecodeError as e:
                last_error = e
                continue
        
        # 所有编码都失败
        raise ValueError(f"无法解码文件，尝试的编码: {encodings}") from last_error

def process_large_gfx_file(input_file: str, buffer_size: int = 8192) -> bool:
    """
    处理大型gfx文件的流式版本，适用于大文件
    
    参数:
        buffer_size: 缓冲区大小（字节）
    """
    if not os.path.exists(input_file):
        print(f"错误: 文件不存在 '{input_file}'")
        return False
    
    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_alt{ext if ext else '.gfx'}"
    
    # 预编译正则表达式
    # 匹配包含'name'且后面某处有'alternate'的模式
    # 使用正向预查确保效率
    pattern = re.compile(
        r'(?=.*?name)(?=.*?alternate).*alternate.*',
        re.IGNORECASE | re.DOTALL
    )
    
    stats = {'processed': 0, 'modified': 0}
    
    try:
        with open_file_smart(input_file, 'r') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for line in infile:
                stats['processed'] += 1
                
                if 'name' in line.lower() and 'alternate' in line.lower():
                    # 使用re.sub进行不区分大小写的替换
                    new_line = re.sub(r'alternate', 'alt', line, flags=re.IGNORECASE)
                    outfile.write(new_line)
                    stats['modified'] += 1
                else:
                    outfile.write(line)
        
        print(f"处理完成: 处理 {stats['processed']} 行，修改 {stats['modified']} 行")
        return True
        
    except Exception as e:
        print(f"处理失败: {e}")
        return False

def main():
    """主函数，提供多种使用方式"""
    if len(sys.argv) < 2:
        print("高级GFX文件处理器")
        print("=" * 50)
        print("功能:")
        print("  1. 基本处理: script.py <文件.gfx>")
        print("  2. 批量处理: script.py --batch [模式]")
        print("  3. 大文件处理: script.py --stream <大文件.gfx>")
        print("  4. 测试模式: script.py --test")
        print("\n示例:")
        print("  script.py texture.gfx")
        print("  script.py --batch *.gfx")
        print("  script.py --stream huge.gfx")
        return
    
    arg = sys.argv[1]
    
    if arg == '--batch':
        pattern = sys.argv[2] if len(sys.argv) > 2 else "*.gfx"
        # 这里可以调用批量处理函数
        print(f"批量处理模式: {pattern}")
    elif arg == '--stream':
        if len(sys.argv) > 2:
            process_large_gfx_file(sys.argv[2])
        else:
            print("错误: 需要指定文件名")
    elif arg == '--test':
        # 创建测试文件
        create_test_file()
    else:
        # 默认单个文件处理
        process_gfx_file_optimized(arg)

def create_test_file():
    """创建测试文件"""
    test_content = """# GFX Test File
spriteType = {
    name = "test_sprite_alternate"
    texturefile = "gfx/test.dds"
    alternate = "yes"
}

spriteType = {
    name = "normal_sprite"
    texturefile = "gfx/normal.dds"
}

iconType = {
    name = "icon_alternate_version"
    spriteType = "GFX_icon_alternate"
    alternate = "maybe"
}
"""
    
    with open("test.gfx", "w") as f:
        f.write(test_content)
    
    print("已创建测试文件: test.gfx")
    print("运行: python script.py test.gfx 进行测试")

if __name__ == "__main__":
    main()