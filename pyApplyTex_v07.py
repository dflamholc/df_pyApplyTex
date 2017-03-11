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
        
        try:
            # if the object has a tex tag and the names match - DO NOTING
            if obj.GetTag(c4d.Ttexture) in tags and obj.GetTag(c4d.Ttexture).GetMaterial().GetName() == objName:
                print "This object already has a material applied, matching the object name."

            # IF TEHRE ARE TWO STACKED MATERIALS ONE OF WHICH MATCH THE NAME THEN IGNORE

            # if the object has a TEX tag and a UVW tag, BUT the names DON'T match:
            elif obj.GetTag(c4d.Ttexture) and obj.GetTag(c4d.Tuvw) in tags and obj.GetTag(c4d.Ttexture).GetMaterial().GetName() != objName:
                print "We have already applied both a TEXTURE and UVW tag here."
                # APPLY TAG AFTER CURRENT TAG with UVW Projection
                texTag.SetMaterial(matList[matNames.index(objName)])
                texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
                obj.InsertTag(texTag, obj.GetTag(c4d.Ttexture))
                doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)
            
            # if the object has ONLY a TEX tag, AND the names DON'T match
            elif obj.GetTag(c4d.Ttexture) and not obj.GetTag(c4d.Tuvw) in tags and obj.GetTag(c4d.Ttexture).GetMaterial().GetName() != objName:
                print "We have alreaqdy applied TEXTURE tag here."
                # APPLY TEX tag AFTER CURRENT tag with CUBIC Projection
                texTag.SetMaterial(matList[matNames.index(objName)])
                texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CUBIC
                obj.InsertTag(texTag, obj.GetTag(c4d.Ttexture))
                doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

            # if the object has ONLY a UVW tag AND the names DON'T match 
            elif obj.GetTag(c4d.Tuvw) and not obj.GetTag(c4d.Ttexture) in tags:
                print "We have only a UVW tag here"
                # APPLY TEX tag with UVW projectoin
                texTag.SetMaterial(matList[matNames.index(objName)])
                texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
                obj.InsertTag(texTag)
                doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

            else:
                # if the object has NONE tags then apply  
                print "TEXTURE tag with name matching the object's has been applied!"
                texTag.SetMaterial(matList[matNames.index(objName)])
                texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CUBIC
                obj.InsertTag(texTag)
                doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

        except:
            raise StopIteration
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

    # start UNDO
    doc.StartUndo()

    # call the recursive function with callback
    recurseObjs(obj, checkName, matList)

    # end UNDO
    doc.EndUndo()
    
    # update the Cinema 4D UI
    c4d.EventAdd()

if __name__=='__main__':
    main()