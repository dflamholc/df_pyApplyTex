

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
        # this is WRONG.. we're checking every tag
        
        # looping through each objects set of tags, checking them one by one
        for tag in tags:
            # set up a variable for the typename
            Tagtype = tag.GetTypeName()

            # check if there is already a material with that name
            if Tagtype == "Texture" and tag.GetMaterial().GetName() == objName:
                print "Texture with correct name already applied!"

            elif Tagtype == "UVW":
                # check if an ojbect has a UVW tag
                # if the object has a UVW tag -> apply UVW projection
                texTag.SetMaterial(matList[matNames.index(objName)])
                texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
                obj.InsertTag(texTag)
            
            else:
                # if not then apply the material with Cubic projection
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

