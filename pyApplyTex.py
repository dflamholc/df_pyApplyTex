import c4d
from c4d import documents

# get first object

doc = c4d.documents.GetActiveDocument()
obj = doc.GetFirstObject()

# populate list from text file
materialList = []


# iterate through the hierachy
    # for each object check name in list exists
    # iterate through materials -> if same name found apply material


class Collector(): #new class to collect the notes and put into data lists - the idea is to create another class to 

    def __init__(self, op):
        self.op = op

    def setDoc(self, doc=None): # CHECKS HERE - for now its the doc check - but all checks should go here
        if doc is not None:
            self.doc = doc
        else:
            self.doc = c4d.documents.GetActiveDocument()
        print "Collector initialised using document: " + self.doc.GetDocumentName()

    def GetNextObject(self, op=None): # hierarchy non-recursive iterator
        if self.op == None:
            return None
        if self.op.GetDown():
            return self.op.GetDown()
        while not self.op.GetNext() and self.op.GetUp():        
            self.op = self.op.GetUp()
        return self.op.GetNext()

    def findTags(self, op=None):
        while self.op:
            tags = self.op.GetTags()
            for tag in tags:
                Tagtype = tag.GetTypeName()
                # check if object has UVW tag
                # check name of objcet
                # apply material with same name
                # set projection to UVW
                if Tagtype == 'UVW':
                    print "yes"
                    # tagList.append(tag)
                    # if there is no UVW tag
                    # check name of object
                    # apply material with same name
                    # set projection to Cubic
                else:
                    print "no"
                # elif Tagtype == 'To Do':
                    todoList.append(tag)
            # run the iterator function again to stop the while loop
            self.op = self.GetNextObject(self.op)



def main():
    # ALL INITIAL CHECKS
    collector.findTags(obj)
    # print docPath
    
    if not docPath: #check if we've saved the document scene file
        gui.MessageDialog("Please save your scene before running this script.")
        return False
    elif not obj: # check if we have any ojbects
        gui.MessageDialog("You need at least on e object in your scene, to run run this script.")
        return False
    elif not tagList:
        # check if we have any usable tags on objects
        gui.MessageDialog("You need at least one Annotation Tag in your scene, to run run this script.")
        return False