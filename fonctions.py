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

def readBibFile(filename,frameRef,frameTag) :
	
	global data,listTags
	options = {}
	options['filetypes'] =  [('bibtex files', '.bib'),('all files', '.*')]
	filename = tkFileDialog.askopenfilename(**options)

	print "Importing bibtex file ..."
	parser = bibtex.Parser()
	#bib_data = parser.parse_file('/users/cofri/IRCCyN_2014-07-17/Documents/These/Articles/biblio_local_old.bib')
	#bib_data = parser.parse_file('biblio_local_old.bib')
	bib_data = parser.parse_file(filename)
	data = {}
	for i,entry in enumerate(bib_data.entries) :
		uid = str(bib_data.entries.keys()[i])
		tmp = bib_data.entries[bib_data.entries.keys()[i]]
		try :
			refType = str(tmp.type)
		except :
			refType = ''
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
			author = author.split(" and ")
			author = [s.strip() for s in author]
		except :
			author = ''

		data[uid] = {'UID':uid,'refType':refType,'Title':title,'Journal':journal,'Year':year,'Authors':author,
			'Tags':['coucou','lol','neige','pluie']}
		if uid == 'abubakar2012application' :
			data[uid]['Tags'] = ['arthur','lol','blabla','jacob']

	"""
	model = TableModel()
	model.importDict(data)
	model.columnNames = ['UID','Title','Authors','Journal','Year']
	table = TableCanvas(self.frameRef, model=model)
	table.createTableFrame()
	table.redrawTable()
	"""
	print "readBibFile"
	print data.keys()
	drawTable(data,frameRef)
	list_tags(data)
	display_tags(data,frameRef,frameTag)
	return data

def drawTable(data,frame) :

	model = TableModel()
	model.importDict(data)
	model.columnNames = ['UID','refType','Title','Authors','Journal','Year','Tags']
	table = TableCanvas(frame, model=model)
	table.createTableFrame()
	table.redrawTable()


def list_tags(data) :
	global listTags
	listTags = []
	for key in data :
	  for tag in data[key]['Tags'] :
	    if not tag in listTags :
	      listTags.append(tag)
	return listTags

def append_tags(data) :
	global listTags
	for key in data :
	  for tag in data[key]['Tags'] :
	    if not tag in listTags :
	      listTags.append(tag)
	return listTags


def display_tags(data,frameRef,frameTag) :

	global listTags

        dlist = [[tag,False] for tag in listTags]

	frameTag.grid()
        for r in range(len(listTags)):
            frameTag.rowconfigure(r, weight=1)    
        Label(frameTag, text="TAGS",justify=CENTER,font=('bold',16)).grid(row=0, column=0, sticky="ew")

        row = 1
	buttons = {}
        for (tag, active) in dlist:
	    buttons[tag] = Button(frameTag,text=tag)
	    buttons[tag].grid(row=row, column=0, sticky="ew")
	    buttons[tag].configure(command=lambda tag=tag :filter_tag(data,listTags,frameRef,frameTag,buttons,tag))

            row += 1



def filter_tag(data,tags,frameRef,frameTag,buttons,tag) :
	
	print "Filtering tags..."
	print tag
	if buttons[tag].cget('bg') == "#d9d9d9" :
	  buttons[tag].configure(bg = "red")
	else :
	  buttons[tag].configure(bg = "#d9d9d9")
	#print buttons[tag].cget('bg')

	tags_sel = []
	for tag in buttons :
	  if buttons[tag].cget('bg') == "red" :
	    tags_sel.append(tag)
	#print tags_sel

	if tags_sel == [] :
	  refs_sel = data
	else :
	  refs_sel = {}
	  for key in data :
	    nb_tag = 0
	    for tag_sel in tags_sel :
	      if tag_sel in data[key]['Tags'] :
	        nb_tag += 1
	    if nb_tag == len(tags_sel) :
	      refs_sel[key] = data[key]
	if len(refs_sel) == 0 :
	  refs_sel = {'No refs':{'UID':'','refType':'','Title':'','Journal':'','Year':'','Authors':'',
			'Tags':['']}}

	drawTable(refs_sel,frameRef)


def readRefFile(filename,frameRef,frameTag) :
	
    try :
	global data,listTags
	data = {}
	print "readRefFile"
	print data.keys()

	options = {}
	options['filetypes'] =  [('refM files', '.refm'),('all files', '.*')]
	filename = tkFileDialog.askopenfilename(**options)

	fs = open(filename,'rU')
	text_fs = fs.read()
	fs.close()
	text_fs = text_fs.replace("\n","")
	liste = text_fs.split("%ref")
	del liste[0]

	for s in liste :
		s = "".join(s.split("@")[1:])
		reftype = s.split("{")[0].lower()
		uid = s.split(reftype.upper()+"{")[1].split(",")[0]
		title = s.split("title = {")[1].split("},")[0]
		journal = s.split("journal = {")[1].split("},")[0]
		year = int(s.split("year = {")[1].split("},")[0])
		authors = s.split("author = {")[1].split("},")[0]
		authors = authors.split(" and ")
		tags = s.split("tags = {")[1].split("}")[0]
		if tags == '' :
			tags = []
		else :
			tags = tags.split(" ; ")

    		data[uid] = {'UID':uid,'refType':reftype,'Authors':authors,'Title':title,'Journal':journal,'Year':year,'Tags':tags}

	print data.keys()
	drawTable(data,frameRef)
	list_tags(data)
	display_tags(data,frameRef,frameTag)
	return data
    except :
	""" Do nothing """


def addRefFile(filename,frameRef,frameTag) :

    try :	
	global data,listTags
	print "addRefFile"
	print data.keys()

	options = {}
	options['filetypes'] =  [('refM files', '.refm'),('all files', '.*')]
	filename = tkFileDialog.askopenfilename(**options)

	fs = open(filename,'rU')
	text_fs = fs.read()
	fs.close()
	text_fs = text_fs.replace("\n","")
	liste = text_fs.split("%ref")
	del liste[0]
	for s in liste :
		s = "".join(s.split("@")[1:])
		reftype = s.split("{")[0].lower()
		uid = s.split(reftype.upper()+"{")[1].split(",")[0]
		title = s.split("title = {")[1].split("},")[0]
		journal = s.split("journal = {")[1].split("},")[0]
		year = int(s.split("year = {")[1].split("},")[0])
		authors = s.split("author = {")[1].split("},")[0]
		authors = authors.split(" and ")
		tags = s.split("tags = {")[1].split("}")[0]
		if tags == '' :
			tags = []
		else :
			tags = tags.split(" ; ")

    		data[uid] = {'UID':uid,'refType':reftype,'Authors':authors,'Title':title,'Journal':journal,'Year':year,'Tags':tags}

	
	print data.keys()
	drawTable(data,frameRef)
	append_tags(data)
	display_tags(data,frameRef,frameTag)
	return data

    except :
	""" Do nothing """


###############################################################################################################
def saveRefFile() :

    global data

    options = {}
    options['filetypes'] =  [('refM files', '.refm')]
    options['defaultextension'] = '.refm'
    filename = tkFileDialog.asksaveasfilename(**options)

    print "saving references to file " + filename + " ..."

    fs = open(filename,'w')

    for ref in data :
	  fs.write("%ref\n")
	  fs.write("@"+data[ref]['refType'].upper()+"{"+data[ref]['UID']+",\n")
	  fs.write("  author = {")
	  for ind,i in enumerate(data[ref]['Authors']) :
	    if ind > 0 :
	      fs.write(' and ')
	    fs.write(i)
	  fs.write("},\n")
	  fs.write("  title = {" + data[ref]['Title'] + "},\n")
	  fs.write("  journal = {" + data[ref]['Journal'] + "},\n")
	  fs.write("  year = {" + str(data[ref]['Year']) + "},\n")
	  fs.write("  tags = {")
	  for ind,i in enumerate(data[ref]['Tags']) :
	    if ind > 0 :
	      fs.write(' ; ')
	    fs.write(i)
	  fs.write("}\n")
	  fs.write("}\n")
	  fs.write("\n")
    fs.close()


###############################################################################################################
def createNewTag(frameRef,frameTag) :

    global data, listTags

    tagwin = Tk()
    Label(tagwin,text="Give a name to a new tag :").pack()
    newTag = Entry(tagwin,width = 25)
    newTag.pack()
    newTag.focus_set()
    Button(tagwin,text="Enter",command=lambda : addNewTag(tagwin,newTag,frameRef,frameTag)).pack()

    tagwin.mainloop()

def addNewTag(tagwin,newTag,frameRef,frameTag) :
	global data, listTags
	print "new tag added"
	print newTag.get()
	listTags.append(newTag.get())
	tagwin.destroy()
	display_tags(data,frameRef,frameTag)


###############################################################################################################
def editRef(frameRef,frameTag) :

    global data, listTags

    editwin = Tk()
    editwin.title('Edit a reference')
    editwin.geometry(("800x600"))

    var = StringVar(editwin)
    options = [] 
    for key in data :
      options.append(key)
    var.set("Select a reference") # initial value
    option = OptionMenu(editwin, var, *options)
    option.pack()
    ref_sel = var.get()
    print ref_sel
    selbut1 = Button(editwin,text="Confirm ref",command= lambda: chooseRef(editwin,var,frameRef))
    selbut1.pack()

    editwin.mainloop()

###############################################################################################################
def chooseRef(editwin,option,frameRef) :

    global data,listTags

    ref_sel = option.get()
    ref_sel = data[ref_sel]

    Label(editwin,text="UID :").pack()
    s_uid = StringVar(editwin)
    s_uid.set(ref_sel['UID'])
    e_uid = Entry(editwin,textvariable=s_uid,width=300)
    e_uid.pack()

    Label(editwin,text="Type of reference :").pack()
    s_refType = StringVar(editwin)
    s_refType.set(ref_sel['refType'])
    e_refType = Entry(editwin,textvariable=s_refType,width=300)
    e_refType.pack()

    Label(editwin,text="Title :").pack()
    s_title = StringVar(editwin)
    s_title.set(ref_sel['Title'])
    e_title = Entry(editwin,textvariable=s_title,width=300)
    e_title.pack()

    Label(editwin,text="Authors :").pack()
    s_authors = StringVar(editwin)
    text_aut = " and ".join(ref_sel['Authors'])
    s_authors.set(text_aut)
    e_authors = Entry(editwin,textvariable=s_authors,width=300)
    e_authors.pack()

    Label(editwin,text="Journal :").pack()
    s_journal = StringVar(editwin)
    s_journal.set(ref_sel['Journal'])
    e_journal = Entry(editwin,textvariable=s_journal,width=300)
    e_journal.pack()

    Label(editwin,text="Year :").pack()
    s_year = StringVar(editwin)
    s_year.set(ref_sel['Year'])
    e_year = Entry(editwin,textvariable=s_year,width=300)
    e_year.pack()

    selbut2 = Button(editwin,text="Update reference then change tags",
	command = lambda: updateRef(editwin,e_uid,e_refType,e_title,e_authors,e_journal,e_year,frameRef,ref_sel))
    selbut2.pack()


###############################################################################################################
def updateRef(editwin,e_uid,e_refType,e_title,e_authors,e_journal,e_year,frameRef,ref_sel) :
    
    global data, listTags
    
    Label(editwin,text="Tags :").pack()
    listbox2 = Listbox(editwin,selectmode = "multiple")
    listbox2.pack()
    for tag in listTags :
	listbox2.insert(END,tag)
	if tag in ref_sel['Tags'] :
	  listbox2.selection_set(first=END)

    selbut3 = Button(editwin,text="Update tags",command = lambda: updateRef2(editwin,e_uid,e_refType,e_title,e_authors,e_journal,e_year,listbox2,frameRef))
    selbut3.pack()

###############################################################################################################
def updateRef2(editwin,e_uid,e_refType,e_title,e_authors,e_journal,e_year,listbox,frameRef) :
    
    global data, listTags

    items = listbox.curselection()
    items = [listTags[int(item)] for item in items]
    authors = e_authors.get().split(" and ")
    data[e_uid.get()] = {'UID':e_uid.get(),'refType':e_refType.get(),'Title':e_title.get(),'Authors':authors,
      'Journal':e_journal.get(),'Year':int(e_year.get()),'Tags':items}

    drawTable(data,frameRef)
    editwin.destroy()


###############################################################################################################
def deleteTags(frameTag,frameRef) :

    global data, listTags

    tagwin = Tk()
    Label(tagwin,text="Tags to delete :").pack()
    listbox2 = Listbox(tagwin,selectmode = "multiple")
    listbox2.pack()
    for tag in listTags :
	listbox2.insert(END,tag)
    Button(tagwin,text="Delete",command=lambda : deleteSelTags(tagwin,frameRef,frameTag,listbox2)).pack()

    tagwin.mainloop()


def deleteSelTags(tagwin,frameRef,frameTag,listbox) :
	global data, listTags
	items = listbox.curselection()
    	items = [listTags[int(item)] for item in items]

	listtags2 = listTags[:]
	for ind,tag in enumerate(listTags) :
	  if tag in items :
	    print "remove tag " + tag
	    listtags2.remove(tag) 
	listTags = listtags2[:]

	data2 = deepcopy(data)
	for key in data :
	  for ind,tag in enumerate(data[key]['Tags']) :
	    if tag in items :
	      data2[key]['Tags'].remove(tag)

	data = deepcopy(data2)
	tagwin.destroy()
	display_tags(data,frameRef,frameTag)
	drawTable(data,frameRef)


###############################################################################################################

def deleteRefs(frameRef) :

    global data, listTags

    refwin = Tk()
    Label(refwin,text="Tags to delete :").pack()
    listbox = Listbox(refwin,selectmode = "multiple")
    listbox.pack()
    for key in data :
	listbox.insert(END,key)
    Button(refwin,text="Delete",command=lambda : deleteSelRefs(refwin,frameRef,listbox)).pack()

    tagwin.mainloop()


def deleteSelRefs(refwin,frameRef,listbox) :

	global data, listTags
	items = listbox.curselection()
    	items = [data.keys()[int(item)] for item in items]

	data2 = deepcopy(data)
	for key in data :
	    if key in items :
	      del data2[key]

	data = deepcopy(data2)
	refwin.destroy()
	drawTable(data,frameRef)


###############################################################################################################


