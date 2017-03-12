import c4d, os

# FUNCTIONS #####################################################

def moveExistingTags(obj):
    firstTag = obj.GetFirstTag()  
    lastTag = firstTag

    if lastTag:
        while True:
            if not lastTag.GetNext():
                break
            lastTag = lastTag.GetNext()

        # add a CHANGE undo
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, firstTag)
        
        # remove the first tag and insert after last tag
        firstTag.Remove()
        obj.InsertTag(firstTag, lastTag)

    return firstTag

# place the tags on respective objects
def placeTags(obj, tags, objName, texTag, matList, matNames):
    objTEX = obj.GetTag(c4d.Ttexture)
    objUVW = obj.GetTag(c4d.Tuvw)
    setMAT = matList[matNames.index(objName)]

    # if the object has a tex tag and the names match - DO NOTING
    if objTEX in tags and objTEX.GetMaterial().GetName() == objName:
        print "This object already has a material applied, matching the object name."

    # IF TEHRE ARE TWO STACKED MATERIALS ONE OF WHICH MATCH THE NAME THEN IGNORE

    # if the object has a TEX tag and a UVW tag, BUT the names DON'T match:
    elif objTEX and objUVW in tags and objTEX.GetMaterial().GetName() != objName:
        print "We have already applied both a TEXTURE and UVW tag here."
        # APPLY TAG AFTER CURRENT TAG with UVW Projection
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
        obj.InsertTag(texTag, objTEX)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)
    
    # if the object has ONLY a TEX tag, AND the names DON'T match
    elif objTEX and not objUVW in tags and objTEX.GetMaterial().GetName() != objName:
        print "We have already applied TEXTURE tag here."
        # APPLY TEX tag AFTER CURRENT tag with CUBIC Projection
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CUBIC
        obj.InsertTag(texTag, objTEX)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

    # if the object has ONLY a UVW tag AND the names DON'T match 
    elif objUVW and not objTEX in tags:
        print "We have only a UVW tag here. A TEXTURE tag has been applied!"
        # APPLY TEX tag with UVW projectoin
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
        obj.InsertTag(texTag)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

        # move existing material tags to last tag
        moveExistingTags(obj)

    else:
        # if the object has NONE tags then apply  
        print "TEXTURE tag with name matching the object's has been applied!"
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CUBIC
        obj.InsertTag(texTag)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

        # move existing material tags to last tag
        moveExistingTags(obj)

# check the name of each object
def checkName(obj, matList):
    
    objName = obj.GetName()
    matNames = []
    texTag = c4d.TextureTag()

    for mat in matList:
        mName = mat.GetName()
        matNames.append(mName)

    # collect the tags from the object in a list
    tags = obj.GetTags()
    
    # check if the object has a matching material
    try:
        if objName in matNames:
            placeTags(obj, tags, objName, texTag, matList, matNames)
        else:
            print "Texture Not Found!"
    except:
        raise StopIteration
    
# iterate through the scene
def recurseObjs(obj, checkName, matList):
    while obj:
        checkName(obj, matList)
        recurseObjs(obj.GetDown(), checkName, matList)
        obj = obj.GetNext()
    return obj


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