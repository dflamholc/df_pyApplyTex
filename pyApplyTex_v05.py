

import c4d, os

# FUNCTIONS #####################################################

# check the name of each object
def checkName(obj, matList):
    
    objName = obj.GetName()
    matNames = []
    texTag = c4d.TextureTag()

    for mat in matList:
        mName = mat.GetName()
        matNames.append(mName)

    # check if the object has a matching material
    if objName in matNames:
        # collect the tags from the object in a list
        tags = obj.GetTags()
        # print tags
        
        # if the object has a tex tag and the names match - DO NOTING
        if obj.GetTag(c4d.Ttexture).GetMaterial().GetName() == objName:
            print "This object already has a material applied, matching the object name."

        # if the object has a tex tag and NOT a UVW tag, AND the names DON'T match - APPLY TAG AFTER CURRENT TAG with CUBIC Projection
        elif obj.GetTag(c4d.Ttexture) and not obj.GetTag(c4d.Tuvw) in tags and not obj.GetTag().GetMaterial().GetName() == objName:
            print "We have already applied a TEXTURE tag here."
        
        # if the object has a tex tag and a UVW tag and the names 
        elif obj.GetTag(c4d.Ttexture) and obj.GetTag(c4d.Tuvw) in tags and not obj.GetTag().GetMaterial().GetName() == objName:
            print "We have alreaqdy applied both a TEXTURE and UVW tag here."

        elif obj.GetTag(c4d.Tuvw) and not obj.GetTag(c4d.Ttexture)in tags:
            print "We have only a UVW tag here"
            texTag.SetMaterial(matList[matNames.index(objName)])
            texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
            obj.InsertTag(texTag)
        else:
            print "TEXTURE tag with name matching the object's has been applied!"
            texTag.SetMaterial(matList[matNames.index(objName)])
            texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CUBIC
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

    # update the Cinema 4D UI
    c4d.EventAdd()


if __name__=='__main__':
    main()

'''
Ttexture    Texture tag. (TextureTag)
Tuvw    UVW tag. (UVWTag)
'''

