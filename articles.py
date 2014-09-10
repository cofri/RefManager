#! /usr/bin/python
"""
Utilisation de python 2.7

"""
class Reference :

  def __init__(self,uid,refType,authors,title,journal,year,tags) :
    self.refType = refType
    self.author = authors
    self.title = title
    self.journal = journal
    self.year = year
    self.tags = tags
    self.uid = uid

  def getUID(self) :
    return self.uid

  def getRefType(self) :
    return self.refType
 
  def getAuthor(self) :
    return self.author

  def getTitle(self) :
    return self.title

  def getJournal(self) :
    return self.journal

  def getYear(self) :
    return self.year

  def getTags(self) :
    return self.tags

  def setUID(self,uid) :
    self.uid = uid

  def setRefType(self,refType) :
    self.refType = refType

  def setAuthor(self,author) :
    self.author = author

  def setTitle(self,title) :
    self.title = title

  def setJournal(self,journal) :
    self.journal = journal

  def setYear(self,year) :
    self.year = year

  def setTags(self,tags) :
    self.tags = tags

  def addAuthor(self,authors) :
    self.author += authors

  def addTags(self,tags) :
    self.tags += tags

  
  def printRef(self) :
    print "UID : " + self.uid
    print "Reference type : " + self.refType
    print "Authors : " + str(self.author)
    print "Title : " + self.title
    print "Journal : " + self.journal
    print "Year : " + str(self.year)
    print "Tags : " + str(self.tags)

pass

if __name__ == "__main__" :
  ref = Reference('Friedrich14','article',['Friedrich','Lafait-Boisson'],'Un super article qui parle de rien','IEEE MTS','2014',['3D','inversion'])
  ref.printRef()

  ref.addTags(['cartesien','geophysique'])
  ref.printRef()
