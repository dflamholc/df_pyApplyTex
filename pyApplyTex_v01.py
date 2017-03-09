import c4d
from c4d import documents



doc = c4d.documents.GetActiveDocument()
obj = doc.GetFirstObject()
mat = doc.GetFirstMaterial()

    
def GetNextObject(op): # hierarchy non-recursive iterator
    if op == None:
        return None
    if op.GetDown():
        return op.GetDown()
    while not op.GetNext() and op.GetUp():        
        op = op.GetUp()
    return op.GetNext()

def findUVWtag(op):
    
    count = 0
    
    while op:
        count += 1
        tags = op.GetTags()
        for tag in tags:
            Tagtype = tag.GetTypeName()
            if Tagtype == 'UVW':
                print "yes"
                print op.GetName()
                # tagList.append(tag)
            else:
                print "no"
                print op.GetName()
                # todoList.append(tag)
        # run the iterator function again to stop the while loop
        op = GetNextObject(op)
    return count


count = findUVWtag(obj)


materials = []

def findMat(mat):
    while mat:
        materials.append(mat)
    mat = mat.GetNext()
    

findMat(mat)

for mat in materials:
    print mat

print "iterated " + str(count) + " ojbects"