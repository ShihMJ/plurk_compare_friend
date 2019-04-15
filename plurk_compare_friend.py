from tkinter import *
import tkinter.filedialog
from Compare_friend import Compare_list
from Get_friend_now import make_friend_file
from icon_class import Icon
import base64
import os

class GUI(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid()
        self.filename = ""
        self.createWidgets()
 
    def createWidgets(self):
        self.inputText = Label(self.master)
        self.inputText["text"] = "帳號:"
        self.inputText.grid(row=0, column=0)
        self.inputField = Entry(self.master)
        self.inputField.grid(row=0, column=1, columnspan = 2, sticky = W + E)
 
        self.outputText = Label(self.master)
        self.outputText["text"] = "Output:"
        self.outputText.grid(row=1, column=0)
        self.outputField = Text(self.master)
        self.outputField.grid(row=1, column=1, columnspan = 2, sticky = W + E)
         
        self.new = Button(self.master)
        self.new["text"] = "作成名單"
        self.new.grid(row=2, column = 0)
        self.new["command"] = self.newMethod
        self.load_file = Button(self.master)
        self.load_file["text"] = "選擇檔案"
        self.load_file.grid(row=2, column = 1)
        self.load_file["command"] = self.loadMethod

        self.compare_file = Button(self.master)
        self.compare_file["text"] = "好友比較"
        self.compare_file.grid(row=2, column = 2)
        self.compare_file["command"] = self.compareMethod

        self.displayText = Label(self.master)
        self.displayText["text"] = "你好啊旅行者"
        self.displayText.grid(row=3, column=0, columnspan=7)

    def newMethod(self):
        self.outputField.delete(1.0, 'end')
        self.my_account = self.inputField.get()
        if self.my_account == "":
            self.displayText["text"] = "請輸入帳號"
        else:
            self.MFF = make_friend_file(self.my_account)
            self.MFF.get_friend()
            if self.MFF.my_info_json :
                self.displayText["text"] = "已生成好友名單"
            else :
                self.displayText["text"] = "帳號不存在"
            
    def loadMethod(self):
    	self.filename = tkinter.filedialog.askopenfilename()
    	if self.filename != '':
    		self.displayText["text"] = "你選擇的檔案是：" + self.filename
    	else:
    		self.displayText["text"] = "請選擇檔案"

    def compareMethod(self):
    	self.outputField.delete(1.0, 'end')
    	self.my_account = self.inputField.get()
    	if self.my_account == "":
    		self.displayText["text"] = "請輸入帳號"
    	elif self.filename == "":
    		self.displayText["text"] = "請選擇檔案"
    	else:
            self.CL = Compare_list(self.filename, self.my_account)
            if self.CL.compare_friend() :
                self.deleted_friend = self.CL.deleted_friend
                if self.deleted_friend != []:
                    for friend in self.deleted_friend :
                        # check if there is emoji (or char not in range U+0000-U+FFFF)
                        friend_string = [friend[i] for i in range(len(friend)) if ord(friend[i]) in range(65536)]
                        friend_string = ''.join(friend_string)
                        self.outputField.insert(tkinter.END, str(friend_string))
                        self.outputField.insert(tkinter.END, "\n")
                else :
                    self.outputField.insert(1.0, "沒有被刪除的好友")
            else :
                self.outputField.insert(1.0, "帳號不存在")

if __name__ == '__main__':
    root = Tk()
    root.columnconfigure(1, weight = 1)
    root.rowconfigure(1, weight = 1)
    root.geometry("400x100")
    root.winfo_toplevel().title("噗浪邊緣人2.1")

    icon = Icon().icon
    icondata= base64.b64decode(icon)
    # The temp file is icon.ico
    tempFile= "icon.ico"
    iconfile= open(tempFile,"wb")
    # Extract the icon
    iconfile.write(icondata)
    iconfile.close()
    root.wm_iconbitmap(tempFile)
    # remove the temp file
    os.remove(tempFile)

    app = GUI(master=root)

    app.mainloop()