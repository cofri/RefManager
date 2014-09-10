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

def readBibFile(self,filename,frameRef,frameTag) :
	print "Importing bibtex file ..."

	parser = bibtex.Parser()
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
		data[uid] = {'UID':uid,'Title':title,'Journal':journal,'Year':year,'Authors':author,'Tags':['coucou','lol']}
		if uid == 'abubakar2012application' :
			data[uid]['Tags'] = ['arthur','lol']

	"""
	model = TableModel()
	model.importDict(data)
	model.columnNames = ['UID','Title','Authors','Journal','Year']
	table = TableCanvas(self.frameRef, model=model)
	table.createTableFrame()
	table.redrawTable()
	"""
	drawTable(data,frameRef)
	list_tags(data)
	display_tags(data,frameRef,frameTag)
	return data

def drawTable(data,frame) :

	model = TableModel()
	model.importDict(data)
	model.columnNames = ['UID','Title','Authors','Journal','Year','Tags']
	table = TableCanvas(frame, model=model)
	table.createTableFrame()
	table.redrawTable()


def list_tags(data) :

	listTags = []
	for key in data :
	  for tag in data[key]['Tags'] :
	    if not tag in listTags :
	      listTags.append(tag)
	print "list Tags = " 
	print listTags
	return listTags


def display_tags(data,frameRef,frameTag) :

	tags = list_tags(data)
	print "type tag = " + str(type(tags))
        dlist = [[tag,False] for tag in tags]

	frameTag.grid()
        for r in range(len(tags)):
            frameTag.rowconfigure(r, weight=1)    
        for c in range(2):
            frameTag.columnconfigure(c, weight=1)
        Label(frameTag, text="Tag", anchor="w",justify=LEFT,font=('bold',16)).grid(row=0, column=0, sticky="ew")
        Label(frameTag, text="Filter",justify=RIGHT,font=('bold',16)).grid(row=0, column=1, sticky="ew")

        row = 1
        for (tag, active) in dlist:
            nr_label = Label(frameTag, text=tag, anchor="w")
            active_cb = Checkbutton(frameTag, onvalue=True, offvalue=False,command= lambda: filter_tag(data,frameRef,frameTag,tag,active_cb))
            if active:
                active_cb.select()
            else:
                active_cb.deselect()
            nr_label.grid(row=row, column=0, sticky="ew")
            active_cb.grid(row=row, column=1, sticky="ew")
            row += 1



def filter_tag(data,frameRef,frameTag,tag,active_cb) :
 print "Tag " + tag + " active? " + str(active_cb)
 tags_sel = [tag]
 refs_sel = {}
 print "Filtering refs with tags..."
 if active_cb == True :
  for key in data :
    for tag_sel in tags_sel :
      if tag_sel in data[key]['Tags'] :
        refs_sel[key] = data[key]
        break

 if len(refs_sel) == 0 :
  refs_sel['rien'] = {'UID':'rien','Title':'rien','Journal':'rien','Year':'rien','Authors':'rien','Tags':['rien']}
 drawTable(refs_sel,frameRef)

