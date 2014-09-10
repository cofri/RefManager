import sys
from Tkinter import *
from fonctions import *
from main import *
#sys.path.append("tkintertable-1.1/")
#sys.path.append("pybtex-0.18/")
sys.path.append("../tkintertable-1.1.2/")
sys.path.append("../pybtex/")
from tkintertable.Tables import TableCanvas
from tkintertable.TableModels import TableModel
from pybtex.database.input import bibtex
from copy import deepcopy

###############################################################################################
######## CLASS App ########
class App:

    def __init__(self, master):
	

	data = {}

	# Define the grid
	master.grid()
	for r in range(2):
            master.rowconfigure(r, weight=1)    
        for c in range(4):
            master.columnconfigure(c, weight=1)
	master.title('Coucou')
	master.geometry(("1000x700"))
        
	# Block for refs
	frameRef = LabelFrame(master,padx=10,pady=10)
	frameRef.grid(row=0,column=1,rowspan=2,columnspan=3,sticky="nwe")

	# Block for tags
	frameTag = LabelFrame(master,padx=10,pady=10)
        frameTag.grid(row=0,column=0)
	#ChoixTag(frameTag)
	display_tags(data,frameRef,frameTag)

	# Block test
	frameQuit = Frame(master,bg="green")
	frameQuit.grid(row=1,column=0,sticky="ewns")
	Button(frameQuit,text="QUIT",command=master.quit,bg="red").pack(fill=BOTH,expand=1)
		
	# Main Menu
	menu = MainMenu(master,frameRef,frameTag)	
	print "menu.data = "
	print menu.data

	# Block test 2
	frame4 = Frame(master)
	frame4.grid(row=1,column=1,columnspan=3,sticky="ewns")
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
######## CLASS VisuRef ########
class VisuRef:

    def __init__(self, master):

	frame = master
	#frame.pack()
        #frame = Frame(master)
        #frame.pack()

        #frame.grid_columnconfigure(1, weight=1)
        #Label(frame, text="UID", anchor="w").grid(row=0, column=0, sticky="ew")
        #Label(frame, text="Title", anchor="w").grid(row=0, column=1, sticky="ew")
	#data = [['uid1','title 1'],['uid2','title 2'],['uid3','title 3']]
        #row = 1
        #for (uid, title) in data:
        #    nr_label = Label(frame, text=uid, anchor="w")
        #    nr_title = Label(frame, text=title, anchor="w")
        #    nr_label.grid(row=row, column=0, sticky="ew")
        #    nr_title.grid(row=row, column=1, sticky="ew")
        #    row += 1
	"""
	parser = bibtex.Parser()
	#bib_data = parser.parse_file('biblio_test.bib')
	#bib_data = parser.parse_file('/users/cofri/IRCCyN_2014-07-17/Documents/These/Articles/biblio_local_old.bib')
	bib_data = parser.parse_file('biblio_local_old.bib')
	data = {}
	for i,entry in enumerate(bib_data.entries) :
		uid = str(bib_data.entries.keys()[i])
		tmp = bib_data.entries[bib_data.entries.keys()[i]]
		try :
			title = str(tmp.fields['title'])
		except :
			title = ''
		try :
			journal = str(tmp.fields['journal'])
		except :
			journal = ''
		try :
			year = int(tmp.fields['year'])
		except :
			year = ''
		try :
			author = str(tmp.fields['author'])
		except :
			author = ''
		data[uid] = {'UID':uid,'Title':title,'Journal':journal,'Year':year,'Authors':author}
	#"""
	#print "data = "
	#print data
	"""
	order_labels = {'UID':0,'Title':1,'Authors':2,'Journal':3,'Year':4}
	order_labels2 = {0:'UID',1:'Title',2:'Authors',3:'Journal',4:'Year'}
	model = TableModel()
	model.importDict(data)
	model.columnNames = ['UID','Title','Authors','Journal','Year']
	self.table = TableCanvas(frame, model=model)
	self.table.createTableFrame()
	self.table.redrawTable()
	#"""


###############################################################################################
######## CLASS mainMenu ########

class MainMenu :

  def __init__(self, master,frameRef,frameTag):
	
	global visu
	self.data = {}
	self.frameRef = frameRef
	menubar = Menu(master)
	# create a pulldown menu, and add it to the menu bar
	filemenu = Menu(menubar, tearoff=0)
	filemenu.add_command(label="Open bibtex file", command= lambda : self.readBibFile('',frameRef,frameTag))
	filemenu.add_command(label="Save", command=self.printText)
	filemenu.add_command(label="Exit", command=master.quit)
	menubar.add_cascade(label="File", menu=filemenu)

	# create more pulldown menus
	editmenu = Menu(menubar, tearoff=0)
	editmenu.add_command(label="Cut", command=self.printText)
	editmenu.add_command(label="Copy", command=self.printText)
	editmenu.add_command(label="Paste", command=self.printText)
	menubar.add_cascade(label="Edit", menu=editmenu)

	helpmenu = Menu(menubar, tearoff=0)
	helpmenu.add_command(label="About", command=self.printText)
	menubar.add_cascade(label="Help", menu=helpmenu)

	# display the menu
	master.config(menu=menubar)

  def printText(self) :
	print "Coucou les clous"

  def readBibFile(self,filename,frameRef,frameTag) :
	self.data = readBibFile(self,filename,frameRef,frameTag)
	print "self.data = "
	print self.data

###############################################################################################
######## main function ########
if __name__ == "__main__":

	root = Tk()
	app = App(root)
	root.mainloop()
	#root.destroy() # optional; see description below


