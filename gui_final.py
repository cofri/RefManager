import sys
from Tkinter import *
from fonctions import *
from main import *
#sys.path.append("tkintertable-1.1/")
#sys.path.append("pybtex-0.18/")
sys.path.append("../tkintertable-1.1/")
sys.path.append("../pybtex/")
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from pybtex.database.input import bibtex
from copy import deepcopy
import tkFileDialog

###############################################################################################
######## CLASS App ########
class App:

    def __init__(self, master):
	
	global data
	global listTags
	data = {}
	listTags = []

	# Define the grid
	master.grid()
	for r in range(5):
            master.rowconfigure(r, weight=1)    
        for c in range(4):
            master.columnconfigure(c, weight=1)
	master.title('Coucou')
	master.geometry(("1200x700"))
        
	# Block for refs
	frameRef = LabelFrame(master,padx=10,pady=10)
	frameRef.grid(row=0,column=1,rowspan=5,columnspan=3,sticky="nwes")

	# Block for tags
	frameTag = LabelFrame(master,padx=10,pady=10)
        frameTag.grid(row=0,column=0,rowspan=4)
	#ChoixTag(frameTag)
	#display_tags(data,frameRef,frameTag)

	# Block quit
	frameQuit = Frame(master,bg="green")
	frameQuit.grid(row=5,column=0,sticky="ewns")
	Button(frameQuit,text="QUIT",command=lambda:master.destroy(),bg="red").pack(fill=BOTH,expand=1)
		
	# Main Menu
	menu = MainMenu(master,frameRef,frameTag)	

	# Block test 2
	#frame4 = Frame(master)
	#frame4.grid(row=1,column=1,columnspan=3,sticky="ewns")
	#table = TableCanvas(frame4)
	#table.createTableFrame()
	#data = {'rec1': {'col1': 99.88, 'col2': 108.79, 'label': 'rec1'},'rec2': {'col1': 99.88, 'col2': 108.79, 'label': 'rec2'}}
	#model = TableModel()
	#model.importDict(data)
	#table = TableCanvas(frame4, model=model)
	#table.createTableFrame()
	#table.redrawTable()
	#w = Spinbox(frame4,values=(1, 2, 4, 8))
	#w.pack()
	#e = Entry(frame4, textvariable="blabla")
	#e.pack()



###############################################################################################
######## CLASS ChoixTag ########
class ChoixTag:

    def __init__(self, frame):
	
	tags = list_tags(data)
        data = [[tag,False] for tag in tags]

	frame.grid()
        for r in range(len(tags)):
            frame.rowconfigure(r, weight=1)    
        for c in range(2):
            frame.columnconfigure(c, weight=1)
        Label(frame, text="Tag", anchor="w",justify=LEFT,font=('bold',16)).grid(row=0, column=0, sticky="ew")
        Label(frame, text="Filter",justify=RIGHT,font=('bold',16)).grid(row=0, column=1, sticky="ew")

        row = 1
        for (tag, active) in data:
            nr_label = Label(frame, text=tag, anchor="w")
            active_cb = Checkbutton(frame, onvalue=True, offvalue=False)
            if active:
                active_cb.select()
            else:
                active_cb.deselect()
            nr_label.grid(row=row, column=0, sticky="ew")
            active_cb.grid(row=row, column=1, sticky="ew")
            row += 1



###############################################################################################
######## CLASS mainMenu ########

class MainMenu :

  def __init__(self, master,frameRef,frameTag):

	global data
	self.frameRef = frameRef
	menubar = Menu(master)
	# create a pulldown menu, and add it to the menu bar
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open bibtex file", command= lambda : readBibFile('',frameRef,frameTag))
	filemenu.add_command(label="Open RefM file", command=lambda : readRefFile('',frameRef,frameTag))
	filemenu.add_command(label="Add RefM file", command=lambda : addRefFile('',frameRef,frameTag))
	filemenu.add_command(label="Save to RefM file", command=lambda : saveRefFile())
	filemenu.add_command(label="Exit", command=master.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	# create more pulldown menus
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Create new tag", command= lambda :createNewTag(frameRef,frameTag))
	editmenu.add_command(label="Delete tag(s)", command=lambda : deleteTags(frameTag,frameRef))
	editmenu.add_command(label="Edit reference", command=lambda : editRef(frameRef,frameTag))
	editmenu.add_command(label="Remove reference(s)", command=lambda : deleteRefs(frameRef))
	menubar.add_cascade(label="Edit", menu=editmenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About", command=lambda : printText())
	menubar.add_cascade(label="Help", menu=helpmenu)

	# display the menu
	master.config(menu=menubar)

def printText() :
	print "Coucou les clous"
	

###############################################################################################
######## main function ########
if __name__ == "__main__":

	root = Tk()
	app = App(root)
	root.mainloop()
	#root.destroy() # optional; see description below


