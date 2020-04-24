import speech_recognition as sr
import threading
import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog


########GUI########

class MenuBar:
    def __init__(self, parent):
        myFont = Font(family="Roboto", size=11)
        
        menubar = tk.Menu(parent.master, font=myFont)
        parent.master.config(menu=menubar)

        fileDropdown = tk.Menu(menubar, font=myFont, tearoff=0)
        fileDropdown.add_command(label="New File",
                                 accelerator="Ctrl+N",
                                 command=parent.newFile)
        fileDropdown.add_command(label="Open File",
                                 accelerator="Ctrl+O",
                                 command=parent.openFile)
        fileDropdown.add_separator()
        fileDropdown.add_command(label="Save",
                                 accelerator="Ctrl+S",
                                 command=parent.save)
        fileDropdown.add_command(label="Save As....",
                                 accelerator="Ctrl+S",
                                 command=parent.saveAs)
        fileDropdown.add_separator()
        fileDropdown.add_command(label="Exit", command=parent.master.destroy)

        menubar.add_cascade(label="File", menu=fileDropdown)

        
        voiceCodeDropdown = tk.Menu(menubar, font=myFont, tearoff=0)
        voiceCodeDropdown.add_command(label="Start Dictating",
                                      command=parent.callBack)


        menubar.add_cascade(label="Voice Coding", menu=voiceCodeDropdown)



class Statusbar:
    def __init__(self, parent):

        myFont = Font(family="Roboto", size=11)
        
        self.saveStatus = tk.StringVar()
        self.saveStatus.set("VoiceBasedTextEditor - 0.1")

        self.voiceStatus = tk.StringVar()
        self.voiceStatus.set("Voice Recognition Statuts: Not Active")

        saveLabel = tk.Label(parent.textarea, textvariable=self.saveStatus, fg="black",
                        bg="lightgrey", anchor='sw', font=myFont)
        saveLabel.pack(side=tk.BOTTOM, fill=tk.BOTH)

        voiceLabel = tk.Label(parent.textarea, textvariable=self.voiceStatus, fg="black",
                        bg="lightgrey", anchor='sw', font=myFont)
        voiceLabel.pack(side=tk.BOTTOM, fill=tk.BOTH)
        
    def updateSaveStatus(self, *args):
        if isinstance(args[0], bool):
            self.saveStatus.set("Your File Has Been Saved!")
        else:
            self.saveStatus.set("VoiceBasedTextEditor - 0.1")
            
    def updateVoiceRecogStatus(self, check):
        if check==True:
            self.voiceStatus.set("Voice Recognition Status: Active")
        else:
            self.voiceStatus.set("Voice Recognition Status: Not Active")
        
#   VoiceTextEditor class defines the widgets for the editor 
#   provides all the text related Functionlity:
#   -   Open new file
#   -   Create new file
#   -   Save New File

class VoiceBasedTextEditor:
    def __init__(self, master):

        
        master.title("Untitled - VoiceBasedTextEditor")
        master.geometry("1200x700")

        myFont = Font(family="Roboto", size=18)

        self.master = master
        self.filename = None

        self.textarea = tk.Text(master, font=myFont, undo=True)
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        self.textarea.configure(yscrollcommand=self.scroll.set)
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.menubar = MenuBar(self)
        self.statusbar = Statusbar(self)      
        self.bindShortcuts()

       


    

    def setWindowTitle(self, name=None):
        if name:
            file_name = os.path.basename(name)
            self.master.title(file_name +" - " + name + " - VoiceTextEditor")
        else:
            self.master.title("Untitled - VoiceTextEditor")
    
    def newFile(self, *args):
        self.textarea.delete(1.0, tk.END)
        self.filename = None
        self.setWindowTitle()
    
    def openFile(self, *args):
        self.filename = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=[("All Files", "*.*"),
                       ("Text Files","*.txt*"),
                       ("Python Scripts", "*.py*")]
            )
        if self.filename:
            self.textarea.delete(1.0, tk.END)
            with open(self.filename, "r") as f:
                self.textarea.insert(1.0, f.read())
            self.setWindowTitle(self.filename)
            
    def save(self, *args):
        if self.filename:
            try:
                textareaContent = self.textarea.get(1.0, tk.END)
                with open(self.filename, "w") as f:
                    f.write(textareaContent)
                self.statusbar.updateSaveStatus(True)
            except Exception as e:
                print(e)
        else:
            self.saveAs()
    
    def saveAs(self, *args):
        try:
            newFile = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=[("All Files", "*.*"),
                       ("Text Files","*.txt*"),
                       ("Python Scripts", "*.py*")]
                )
            textareaContent = self.textarea.get(1.0, tk.END)
            with open(newFile, "w") as f:
                f.write(textareaContent)
            self.filename = newFile
            self.setWindowTitle(self.filename)
            self.statusbar.updateSaveStatus(True)
        except Exception as e:
            print(e)

    def bindShortcuts(self):
        self.textarea.bind('<Control-n>', self.newFile)
        self.textarea.bind('<Control-o>', self.openFile)
        self.textarea.bind('<Control-s>', self.save)
        self.textarea.bind('<Control-Shift-S>', self.saveAs)
        self.textarea.bind('<Key>', self.statusbar.updateSaveStatus)

    ###
    #Voice Recognition Funciton  
    ###
    def activateVoiceRecogntion(self):
        self.statusbar.updateVoiceRecogStatus(True)
        r = sr.Recognizer()
        r.pause_threshold = 0.7
        r.energy_threshold = 400

        
        stopEvent = threading.Event()
        stopEvent.set()
        
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=1)
            while True:
                audio = r.listen(source)
            
                try:
                    command = str(r.recognize_google(audio)).lower()
                
                    level = 1

                ###
                #Text Editor File Operations 
                ###
                    if command == "new line":
                        self.textarea.insert(tk.INSERT, "\n")
                    
                    elif command == "next":
                        self.textarea.insert(tk.INSERT,"\t"*level)
                    
                    elif command == "space":
                        self.textarea.insert(tk.INSERT," "*level)
                    
                    elif command == "create new file":
                        self.newFile()
                    
                    elif command == "open file":
                        self.openFile()
                    
                    elif command == "save file":
                        self.save()
                    
                    elif command == "save as":
                        self.saveAs()
                    

                    
                ###
                #Python Assignment Operator
                ###
                    elif command == "equal":
                        self.textarea.insert(tk.INSERT, "=")
                    

                ###
                #Python Comparison Operators 
                ##
                    elif command == "is equal to":
                        self.textarea.insert(tk.INSERT, "==")
                    
                    elif command == "not equal to":
                        self.textarea.insert(tk.INSERT, "!=")
                    
                    elif command == "greater then" or command == "greater than":
                        self.textarea.insert(tk.INSERT, ">")
                    
                    elif command == "less then" or command == "less than":
                        self.textarea.insert(tk.INSERT, "<")
                    
                    elif command == "great equal":
                        self.textarea.insert(tk.INSERT, ">=")
                    
                    elif command == "less equal":
                        self.textarea.insert(tk.INSERT, "<=")
                    

                ###
                #Python Aritmetic Operators
                ###
                    elif command == "add":
                        self.textarea.insert(tk.INSERT, "+")
                    
                    elif command == "subtract":
                        self.textarea.insert(tk.INSERT, "-")
                    
                    elif command == "multiply":
                        self.textarea.insert(tk.INSERT, "*")
                    
                    elif command == "divide":
                        self.textarea.insert(tk.INSERT, "/")
                    
                    
                ###
                #Decision Making Statemts
                ###
                    elif command == "if statement":
                        self.textarea.insert(tk.INSERT, "if expression:\n"
                                                 +"\t"*level+"#your code\n")
                    
                    elif command == "else if statement":
                        self.textarea.insert(tk.INSERT, "elif expression:\n"
                                                 +"\t"*level+"#you code\n")
                    
                    elif command == "else statement":
                        self.textarea.insert(tk.INSERT, "else:\n"
                                                 +"\t"*level+"#your code\n")
                    
                    elif command == "full statement":
                        self.textarea.insert(tk.INSERT, "if expression:\n"
                                                 +"\t"*level+"#your code\n"
                                                 +"elif expression:\n"
                                                 +"\t"*level+"#you code\n"
                                                 +"else:\n"
                                                 +"\t"*level+"#your code\n")
                    

                ###
                #Loops: While & For
                ###
                    elif command == "while loop":
                        self.textarea.insert(tk.INSERT, "while expression:\n"
                                                 +"\t"*level+"#your code\n")
                    
                    elif command == "while else loop":
                        self.textarea.insert(tk.INSERT, "while expression:\n"
                                                 +"\t"*level+"#your code\n"
                                                 +"else:\n"
                                                 +"\t"*level+"#your code\n")
                    
                    elif command == "for loop":
                        self.textarea.insert(tk.INSERT, "for iterating_variable in sequence:\n"
                                                 +"\t"*level+"#your code\n")
                    
                    elif command == "for else loop":
                        self.textarea.insert(tk.INSERT, "for iterating_variable in sequence:\n"
                                                 +"\t"*level+"#your code\n"
                                                 +"else:\n"
                                                 +"\t"*level+"#your code\n")
                    
                    

                    elif "function" in command:
                        statement = command.split(" ", 1)
                        statement2 = statement[1].replace(" ","")
                        if statement[0] == "function":
                            self.textarea.insert(tk.INSERT, "def " + statement2.lower()
                                                     + "(var1, var2):\n"
                                                     + "\t"*level+"#your code\n"
                                                     + "\t"*level+"return\n")
                        
                    
                    elif "print" in command:
                        statement = command.split(" ", 1)
                        if statement[0] == "print":
                            self.textarea.insert(tk.INSERT, statement[0]+"(\""+statement[1]+"\")")
                        
                        
                    elif "string" == command[:6]:
                        statement = command.split(" ", 1)
                        print(statement[0])
                        if statement[0] == "string":
                            self.textarea.insert(tk.INSERT, "\""+statement[1]+"\"")
                        
                        
                    elif "call" in command:
                        statement = command.split(" ", 1)
                        statement2 = statement[1].replace(" ","")
                        if statement[0] == "call":
                            self.textarea.insert(tk.INSERT, statement2+"()")
                        
                        
                    elif "variable" in command:
                        statement = command.split(" ", 1)
                        statement2 = statement[1].replace(" ", "")
                        if statement[0] == "variable":
                            self.textarea.insert(tk.INSERT, statement2)
                            
                    elif "stop" == command:
                        if stopEvent.is_set():
                            break
                    
                except sr.UnknownValueError:
                    print('Sorry did not recognise that')

                
            self.statusbar.updateVoiceRecogStatus(False)

            
    ###
    #Creates a thread for speech recognition function to run on 
    ###
    def callBack(self):
        t1 = threading.Thread(target=self.activateVoiceRecogntion)
        t1.start()

                

if __name__== "__main__":
    #Initialise a master(root) window will provides a space
    #for all widget it is going to host
    master = tk.Tk()
    VoiceBasedTextEditor(master)
    master.mainloop()





 
