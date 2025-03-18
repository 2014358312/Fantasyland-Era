import os
import random
import re

def process_txt_files(folder_path):
    # 遍历指定文件夹内的所有文件
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):  # 确保只处理 txt 文件
            file_path = os.path.join(folder_path, filename)
            process_file(file_path)

def process_file(file_path):
    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 检查是否有 "resources" 字段
    resources_index = None
    resources_count = 0
    for i, line in enumerate(lines):
        if re.search(r'\bresources\b', line):
            resources_index = i
            break

    if resources_index is None:
        print(f"跳过文件：{file_path}（未找到 'resources' 字段）")
        return

    # 计算 resources 字段中的元素数量
    for line in lines[resources_index + 1:]:
        if re.match(r'\t\t\w+=\d+', line):  # 匹配资源字段
            resources_count += 1
        elif re.match(r'\t\}', line):  # 匹配 resources 字段的结束
            break

    if resources_count < 6:
        print(f"跳过文件：{file_path}（'resources' 字段不足 6 个元素）")
        return

    # 生成新的随机数
    resources = {
        'oil': generate_random_value([20, 35, 35, 10], 0.75),
        'aluminium': generate_random_value([15, 30, 40, 15], 0.80),
        'rubber': generate_random_value([40, 35, 20, 5], 0.95),
        'tungsten': generate_random_value([30, 40, 25, 5], 0.90),
        'steel': generate_random_value([10, 20, 40, 30], 0.70),
        'chromium': generate_random_value([25, 35, 30, 10], 0.90)
    }

    # 替换现有的 resources 字段
    new_lines = lines[:resources_index + 1] + [
        f"\t\toil={resources['oil']}\n",
        f"\t\taluminium={resources['aluminium']}\n",
        f"\t\trubber={resources['rubber']}\n",
        f"\t\ttungsten={resources['tungsten']}\n",
        f"\t\tsteel={resources['steel']}\n",
        f"\t\tchromium={resources['chromium']}\n",
        "\t}\n"
    ] + lines[resources_index + 8:]

    # 保存修改后的内容
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(new_lines)

    print(f"已处理文件：{file_path}")

def generate_random_value(probabilities, zero_probability):
    # 按照指定的概率生成随机数
    ranges = [(1, 10), (11, 20), (21, 30), (31, 40)]
    random_value = random.choices(
        [random.randint(start, end) for start, end in ranges],
        weights=probabilities
    )[0]
    # 按照指定的概率变为 0
    return random_value if random.random() > zero_probability else 0

# 主函数
def main():
    folder_path = r"C:\Users\Lenovo\Desktop\states"
    if not os.path.isdir(folder_path):
        print("无效的文件夹路径")
        return

    process_txt_files(folder_path)
    print("处理完成")

if __name__ == "__main__":
    main()