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
	#print "type tag = " + str(type(tags))
        dlist = [[tag,False] for tag in listTags]

	frameTag.grid()
        for r in range(len(listTags)):
            frameTag.rowconfigure(r, weight=1)    
        Label(frameTag, text="TAGS",justify=CENTER,font=('bold',16)).grid(row=0, column=0, sticky="ew")

        row = 1
	buttons = {}
        for (tag, active) in dlist:
            #nr_label = Label(frameTag, text=tag, anchor="w")
            #active_cb = Checkbutton(frameTag, onvalue=True, offvalue=False)#,command= lambda: filter_tag(data,frameRef,frameTag,tag,active_cb))
            #if active:
            #    active_cb.select()
            #else:
            #    active_cb.deselect()
            #nr_label.grid(row=row, column=0, sticky="ew")
            #active_cb.grid(row=row, column=1, sticky="ew")
	    buttons[tag] = Button(frameTag,text=tag)
	    buttons[tag].grid(row=row, column=0, sticky="ew")
	    buttons[tag].configure(command=lambda tag=tag :filter_tag(data,listTags,frameRef,frameTag,buttons,tag))

            row += 1

	#for key in buttons :
	    #print buttons[key].cget('bg')


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
    Label(editwin,text="Choose references :").pack()
    listbox1 = Listbox(editwin,selectmode = "multiple")
    listbox1.pack()
    for ref in data :
	listbox1.insert(END,ref)
    selbut1 = Button(editwin,text="Select refs")
    selbut1.pack()

    Label(editwin,text="Choose tags :").pack(side=RIGHT)
    listbox2 = Listbox(editwin,selectmode = "multiple")
    listbox2.pack(side=RIGHT)
    for tag in listTags :
	listbox2.insert(END,tag)
    selbut2 = Button(editwin,text="Select tags",command = lambda: addTagstoRefs(listbox2))
    selbut2.pack(side=RIGHT)

    editwin.mainloop()

def addTagstoRefs(listbox) :
    
    global data, listTags
    
    items = listbox.curselection()
    items = [listTags[int(item)] for item in items]
    print items


    
