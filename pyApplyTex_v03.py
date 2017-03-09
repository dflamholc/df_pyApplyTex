

import c4d, os

# FUNCTIONS #####################################################

# check the name of each object
def checkName(obj, matList):
    
    objName = obj.GetName()
    matNames = []

    for mat in matList:
        mName = mat.GetName()
        matNames.append(mName)

    if objName in matNames:
        # print "Lets apply some tags!"
        tags = obj.GetTags()
        for tag in tags:
            Tagtype = tag.GetTypeName()
            if Tagtype == "UVW":

                print "found a UVW tag"
        # check if there is already a material with that name
        # if not then apply the material
        # check if an ojbect has a UVW tag
        # if the object has a UVW tag -> aplly UVW projection
        # else apply Cubic projection
        
        texTag = c4d.TextureTag()
        texTag.SetMaterial(matList[matNames.index(objName)])
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
        obj.InsertTag(texTag)


    else:
        print "Texture Not Found!"

    

# iterate through the scene
def recurseObjs(obj, checkName, matList):
    while obj:
        checkName(obj, matList)
        recurseObjs(obj.GetDown(), checkName, matList)
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

    
    # call the recursive function with callback
    recurseObjs(obj, checkName, matList)


if __name__=='__main__':
    main()



