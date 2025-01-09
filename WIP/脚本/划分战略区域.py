import os,sys,string
from tkinter import *

files_path = r"../../history/states/"

def calc_prov(files_path):
	provincesList = []
	files_list = os.listdir(files_path)
	files_list.sort(key=lambda x:int(x.split('-')[0]))
	for file_name in files_list:
		#print(file_name)
		file_full_name = os.path.join(files_path, file_name)
		#print(file_full_name)
		with open(file_full_name, "r+", encoding="utf-8") as f:
			content = f.read().splitlines()
			content = [line.strip("\t") for line in content]
			#print(content)
		provincesContent = ""
		for i in range(len(content)):
			if "provinces" in content[i]:
				start = i
				break
		for i in range(i, len(content)):
			if "}" in content[i]:
				end = i
				break
		for i in range(start, end):
			provincesContent = provincesContent + content[i]
		for i in range(len(provincesContent)):
			if not provincesContent[0].isdigit():
				provincesContent = provincesContent[1:]
		#print(provincesContent)
		provincesList.append(provincesContent)
	return provincesList

def a(e):
	global statesList
	global stateList
	state = []
	errorStateList = []
	text = t.get(1.0,END)  #获取所有
	#print(t.get(INSERT,END))#获取光标处到结尾
	statesList = text.split('\n')
	statesList = list(filter(None, statesList))
	try:
		for i in range(len(statesList)):
			strategicregion = ""
			stateList = statesList[i].split(' ')
			for j in range(len(stateList)):
				z = int(stateList[j])
				if z<=len(provincesList):
					for k in range(len(provincesList)):
						if z==k-1:
							state.append(provincesList[k-2])
				else:
					errorStateList.append(i+1)
					errorStateList.append(z)
			strategicregion = " ".join(state)
			strategicregion = strategicregion.replace("  "," ")
			state.clear()
			writeStrategicregion(strategicregion, i)
	except Exception as e:
		print("try except error: ", e)
	#print(statesList)

def writeStrategicregion(prov, i):
	if not os.path.exists('00_Python_strategicregions'):
		os.makedirs('00_Python_strategicregions')
	text = "00_Python_strategicregions/"+str(i)+".txt"
	with open(text, "w+", encoding="utf-8") as f:
		f.write(prov)

if __name__ == "__main__":
	path = os.path.dirname(files_path)
	provincesList = []
	provincesList = calc_prov(path)
	statesList = []
	root = Tk()
	root.title("生成战略区域")

	d = Label(root, wraplength=320, text="每行输入一个战略区域里面所有state的编号，以空格分开。所有行输入完后点击获取数据，文件夹将在同目录下生成。")
	d.grid(row=0,column=0,columnspan=3)
	t = Text(root,width=50,height=20,font=('宋体',10))
	t.grid(row=1,column=0,columnspan=3)
 
	b = Button(root,text='获取数据')
	b.grid(row=2,column=1)
 
	b.bind('<Button-1>',a)

	root.mainloop()