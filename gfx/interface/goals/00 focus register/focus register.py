import os
from tkinter import messagebox

def main(localDirPath):
	print(localDirPath)
	fileList = []
	ulList = []
	charList = []
	fileNameList = []
	ignoreList = []
	extraFormat = ""
	for dirPath, dirName, fileName in os.walk(localDirPath):
		for file in fileName:
			filePath = os.path.join(dirPath, file).replace("\\", "/")
			filePath = filePath.partition('gfx')[1] + filePath.partition('gfx')[2]
			fileNameNoFormat = file.partition('.')[0]
			if (file.endswith(".dds") or file.endswith(".png")) and fileNameNoFormat not in fileNameList:
				fileList.append(filePath)
				fileNameList.append(fileNameNoFormat)
				for index, every_char in enumerate(fileNameNoFormat):
					charList.append(every_char)
				if charList[0].isupper() and charList[1].isupper() and charList[2].isupper():
					ulList.append("1")
				else:
					ulList.append("0")
				charList.clear()
			elif file.endswith(".py") or file.endswith(".exe"):
				pass
			else:
				ignoreList.append(filePath)
	with open("goals.gfx", "w", encoding="utf-8") as f:
		f.write("spriteTypes = {\n")
		for i in range(len(fileList)):
			f.write("\n")
			f.write("\tspriteType = {\n")
			if fileNameList[i].startswith("generic"):
				extraFormat = "goal_"
			elif ulList[i]=="1":
				extraFormat = "focus_"
			f.write("\t\tname = \"GFX_" + extraFormat + fileNameList[i] + "\"\n")
			f.write("\t\ttexturefile = \"" + fileList[i] + "\"\n")
			f.write("\t}\n")
			extraFormat = ""
		f.write("}")
	with open("goals_shine.gfx", "w", encoding="utf-8") as f:
		f.write("spriteTypes = {\n")
		for i in range(len(fileList)):
			f.write("\n")
			f.write("\tspriteType = {\n")
			if fileNameList[i].startswith("generic"):
				extraFormat = "goal_"
			elif ulList[i]=="1":
				extraFormat = "focus_"
			f.write("\t\tname = \"GFX_" + extraFormat + fileNameList[i] + "_shine\"\n")
			f.write("\t\ttexturefile = \"" + fileList[i] + "\"\n")
			f.write("\t\teffectFile = \"gfx/FX/buttonstate.lua\"\n")
			f.write("\t\tanimation = {\"\n")
			f.write("\t\t\tanimationmaskfile = \"" + fileList[i] + "\"\n")
			f.write("\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\" 	# <- the animated file\n")
			f.write("\t\t\tanimationrotation = -90.0		# -90 clockwise 90 counterclockwise(by default)\n")
			f.write("\t\t\tanimationlooping = no			# yes or no ;)\n")
			f.write("\t\t\tanimationtime = 0.75				# in seconds\n")
			f.write("\t\t\tanimationdelay = 0			# in seconds\n")
			f.write("\t\t\tanimationblendmode = \"add\"       #add, multiply, overlay\n")
			f.write("\t\t\tanimationtype = \"scrolling\"      #scrolling, rotating, pulsing\n")
			f.write("\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }\n")
			f.write("\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }\n")
			f.write("\t\t}\n")
			f.write("\t\tanimation = {\"\n")
			f.write("\t\t\tanimationmaskfile = \"" + fileList[i] + "\"\n")
			f.write("\t\t\tanimationtexturefile = \"gfx/interface/goals/shine_overlay.dds\" 	# <- the animated file\n")
			f.write("\t\t\tanimationrotation = 90.0		# -90 clockwise 90 counterclockwise(by default)\n")
			f.write("\t\t\tanimationlooping = no			# yes or no ;)\n")
			f.write("\t\t\tanimationtime = 0.75				# in seconds\n")
			f.write("\t\t\tanimationdelay = 0			# in seconds\n")
			f.write("\t\t\tanimationblendmode = \"add\"       #add, multiply, overlay\n")
			f.write("\t\t\tanimationtype = \"scrolling\"      #scrolling, rotating, pulsing\n")
			f.write("\t\t\tanimationrotationoffset = { x = 0.0 y = 0.0 }\n")
			f.write("\t\t\tanimationtexturescale = { x = 1.0 y = 1.0 }\n")
			f.write("\t\t}\n")
			f.write("\t\tlegacy_lazy_load = no\n")
			f.write("\t}\n")
			extraFormat = ""
		f.write("}")
	if ignoreList:
		with open("ingoredFile.gfx", "w", encoding="utf-8") as f:
			for line in ignoreList:
				f.write(line + "\n")
	print(f"fileList: {fileList}\nfileNameList: {fileNameList}\nignoreList: {ignoreList}\nulList: {ulList}")
	messagebox.showinfo("提示", "注册完成，文件已生成在本程序所在目录下")


if __name__ == "__main__":
	localDirPath = os.path.dirname(__file__)
	print(localDirPath)
	main(localDirPath)
	#messagebox.showerror("错误", "本程序当前仅支持dds或png格式，现所在文件夹不含dds或png格式文件，")	