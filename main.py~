#! /usr/bin/python

import sys
import os.path
#from articles import Reference

def main() :

  constRefFilename = "__biblio.txt"
  
  listRefs = []
  if os.path.isfile(constRefFilename) :
    loadRefFile(constRefFilename,listRefs)

  listTags = []
  for ref in listRefs :
    for tag in ref['tags'] :
      if not tag in listTags :
        listTags.append(tag)

  entree = -1
  while entree != 0 :
    print "========================================="
    print "Menu :"
    print "1 - List all references"
    print "2 - Add a reference manually"
    print "3 - Load a file for references" 
    print "4 - Save refs to file"
    print "5 - Search"
    print "6 - Edit tags"
    print "0 - Exit"

    entree = ''
    while not isinstance(entree, (int,long)) :
      try :
        entree = input()
      except KeyboardInterrupt :
        raise
      except :
        print "You should enter an integer"

    if entree == 1 :
      if len(listRefs) == 0 :
        print "No references !"
      else :
        print "Only UID (1) or all fields (2) ?"
        choice = input()
        if choice == 1 :
          print "=================="
          print "List of references :"
          for ref in listRefs :
            print ref['UID']
          print "=================="
          raw_input()
        elif choice == 2 :
          print "=================="
          print "List of references :"
          for ref in listRefs :
            printRef(ref)
            print "- - - - - - - - -"
          print "=================="
          raw_input()

    if entree == 2 :
      addManualRef(listRefs)

    if entree == 3 :
      print "Filename to import :"
      filename = raw_input()
      if filename == '' :
        filename = constRefFilename
      loadRefFile(filename,listRefs)

    if entree == 4 :
      print "Filename to save references (leave blank to default file) :"
      filename = raw_input()
      if filename == '' :
        filename = constRefFilename
      saveRefToFile(filename,listRefs)

    if entree == 5 :
      searchInRefs(listRefs)

    if entree == 6 :
      editTags(listRefs,listTags)


  print "Exit program"
  sys.exit(1)
######## END MAIN FUNCTION ########  

######## BEGIN addManualRef Function ########
def addManualRef(listRefs) :

    print "UID :"
    uid = raw_input()
    reflist = ['article','inproceedings','phdthesis','book','masterthesis','techreport']
    reftype = ''
    while not reftype in reflist :
      print "Reference type (article,inproceedings,phdthesis,book,masterthesis,techreport) (should be one of these): "
      reftype = raw_input()
      reftype = reftype.lower()
    print "Authors (format: Name1, A.; Name2, D.) : "
    authors = raw_input()
    print "Title : "
    title = raw_input()
    print "Journal : "
    journal = raw_input()
    print "Year : "
    year = ''
    while isinstance(year,(int,long)) == False :
      try :
        year = input()
      except :
        print "You should enter an integer"
    print "Tags (leave blank if no tag, format: tag1;tag2;tag3) : "
    tags = raw_input()

    authors = authors.split(';')
    authors = [s.strip() for s in authors]
    tags = tags.split(';') 
    tags = [s.strip() for s in tags]
    new_ref = {'UID':uid,'refType':reftype,'author':authors,'title':title,'journal':journal,'year':year,'tags':tags}

    print "========================== "
    print "New reference : "
    new_ref.printRef()

    #writeRefToFile(constRefFilename,new_ref)
    listRefs.append(new_ref)

    print "Back to menu"
    return listRefs

######## END addManualRef Function ########


######## BEGIN printRef Function ########
def printRef(ref) :
    print "UID : " + ref['UID']
    print "Reference type : " + ref['refType']
    print "Authors : " + str(ref['author'])
    print "Title : " + ref['title']
    print "Journal : " + ref['journal']
    print "Year : " + str(ref['year'])
    print "Tags : " + str(ref['tags'])


######## END printRef Function ########

######## BEGIN writeRefToFile Function ########
def writeRefToFile(filename,ref) :
  fs = open(filename,'a')
  fs.write("%ref\n")
  fs.write("@"+ref['refType'].upper()+"{"+ref['UID']+",\n")
  fs.write("  author = {")
  for ind,i in enumerate(ref['author']) :
    if ind > 0 :
      fs.write(' and ')
    fs.write(i)
  fs.write("},\n")
  fs.write("  title = {" + ref['title'] + "},\n")
  fs.write("  journal = {" + ref['journal'] + "},\n")
  fs.write("  year = {" + str(ref['year']) + "},\n")
  fs.write("  tags = {")
  for ind,i in enumerate(ref['tags']) :
    if ind > 0 :
      fs.write(' ; ')
    fs.write(i)
  fs.write("}\n")
  fs.write("}\n")
  fs.write("\n")
  fs.close()

######## END writefRefToFile Function ########


######## BEGIN loadRefFile Function ########
def loadRefFile(filename,listRefs) :

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

    listRefs.append({'UID':uid,'refType':reftype,'author':authors,'title':title,'journal':journal,'year':year,'tags':tags})

  print "References uploaded"
  # return listRefs

######## END loadRefFile Function ########


######## BEGIN saveRefToFile Function ########
def saveRefToFile(filename,listRefs) :

  for ref in listRefs :
    writeRefToFile(filename,ref)

######## END saveRefToFile Function ########


######## BEGIN searchInRefs Function ########
def searchInRefs(listRefs) :

  print "1 - Search in all fields"
  print "2 - Search in authors"
  print "3 - Search in title"
  print "4 - Search in journal"
  print "5 - Search in tags"

  entree = ''
  while not isinstance(entree, (int,long)) :
    try :
      entree = input()
    except KeyboardInterrupt :
      raise
    except :
      print "You should enter an integer"

  print "What string?"
  word = raw_input()
  refs_sel = []

  if entree == 2 or entree == 1 :
    for ref in listRefs :
      for ind,aut in enumerate(ref['author']) :
        value = ref['author'][ind].find(word)
        if value > -1 :
          refs_sel.append(ref)
          break

  if entree == 3 or entree == 1 :
    for ref in listRefs :
      value = ref['title'].find(word)
      if value > -1 :
        refs_sel.append(ref)

  if entree == 4 or entree == 1 :
    for ref in listRefs :
      value = ref['journal'].find(word)
      if value > -1 :
        refs_sel.append(ref)

  if entree == 5 or entree == 1 :
    for ref in listRefs :
      for ind,tag in enumerate(ref['tags']) :
        value = ref['tags'][ind].find(word)
        if value > -1 :
          refs_sel.append(ref)
          break

  print "References found"
  for ref in refs_sel :
    print ref['UID']

######## END searchInRefs Function ########


######## BEGIN editTags Function ########
def editTags(listRefs,listTags) :

  print "List of existing tags :"
  print listTags 

  print "--------------------"
  print "1 - Create new tag"
  print "2 - Add existing tag to reference"

  entree = ''
  while not isinstance(entree, (int,long)) :
    try :
      entree = input()
    except KeyboardInterrupt :
      raise
    except :
      print "You should enter an integer"

  if entree == 1 :
    print "Name new tag :"
    new_tag = raw_input()
    listTags.append(new_tag)
  elif entree == 2 :
    print "Choose reference UID:"
    ref_sel = raw_input()
    if not ref_sel in [ref['UID'] for ref in listRefs] :
      print "This UID doesn't exist"
      return
    print "Choose tag :"
    tag_sel = raw_input()
    if not tag_sel in listTags :
      print "This tag doesn't exist"
      return
    for ref in listRefs :
      if ref['UID'] == ref_sel :
        ref['tags'] += [tag_sel]
    print ("Tag " + tag_sel + " added to ref " + ref_sel)


######## END editTags Function ########


if __name__ == "__main__" :
  main()
