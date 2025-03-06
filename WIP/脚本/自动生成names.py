import os,sys

filepath=r"../../common/country_tags/KLS_countries.txt"

def read_file(file_path):
	with open(file_path, 'r+', encoding='utf-8') as file:
		lines = file.readlines()
	return lines

def write_file(file_path, lines):
	with open(file_path, 'w+', encoding='utf-8') as file:
		file.writelines(lines)

def replace_first_three_chars(lines_no_change, lines, old_char, new_char):
	if lines:  # 确保文件不为空
		# 只替换第一行的前三个字符
		lines[0] = lines_no_change[0][:3].replace(old_char, new_char, 1) + lines[0][3:]
	return lines


def GetCountryTag(filepath):
	contentresult = []
	with open(filepath, 'r', encoding='utf-8') as file:
		content_list = file.readlines() #读取所有行并返回列表
		for line in content_list:
			contentresult.append(line[:3])
	#with open("", 'r', encoding='utf-8') as file:
	return contentresult

def main():
	tagList = []
	targetList = []
	tagList = GetCountryTag(filepath)
	sourseContent = read_file("./00_names_example.txt")
	sourseContent_no_change = read_file("./00_names_example.txt")
	for i in range(len(tagList)):
		#print("targetList: ")
		#print(targetList)
		content = replace_first_three_chars(sourseContent_no_change, sourseContent, "ENG", tagList[i])
		#print("content will be added in this turn: ")
		#print(content)
		#targetList.append(content)
		targetList.extend(content)
		targetList.extend("\n\n")
		#print("\n")
	with open("00_names.txt", 'w+', encoding='utf-8') as file:
		for line in targetList:
			file.writelines(line)

if __name__ == '__main__':
	main()
