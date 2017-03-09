

import c4d, os

# FUNCTIONS #####################################################

# check the name of each object
def checkName(obj, matNames):
    
    objName = obj.GetName()
    # print objName

    # compare each object with the list of materials
    
    if objName in matNames:
        print "Lets apply some tags!"
        # check if there is already a material with that name
        # if not then apply the material
        # check if an ojbect has a UVW tag
        # if the object has a UVW tag -> aplly UVW projection
        # else apply Cubic projection
        mat = matNames.index(objName)
        
        texTag = c4d.TextureTag()
        texTag.SetMaterial(mat)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
        obj.InsertTag(texTag)


    else:
        print "Texture Not Found!"

    

# iterate through the scene
def recurseObjs(obj, checkName, matNames):
    while obj:
        
        checkName(obj, matNames)

        recurseObjs(obj.GetDown(), checkName, matNames)
        
        obj = obj.GetNext()
    
    return obj


# extra
#################
# read a text file with individual cubic tile scale values for each texture name


# MAIN #####################################################

def main():
    doc = c4d.documents.GetActiveDocument()
    obj = doc.GetFirstObject()
    # store all materials in a list
    matList = doc.GetMaterials()
    matNames = []

    for mat in matList:
        mName = mat.GetName()
        matNames.append(mName)
    
    # call the recursive function with callback
    recurseObjs(obj, checkName, matNames)



if __name__=='__main__':
    main()



