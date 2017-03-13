



    # IF TEHRE ARE TWO STACKED MATERIALS ONE OF WHICH MATCH THE NAME THEN IGNORE
    elif objTEX.GetMaterial().GetName() != objName and objTEX.GetMaterial().GetName() == objName in tags:
        print "This object seems to already have two TEX tags applied."




    # if the object has a TEX tag and a UVW tag, BUT the names DON'T match:
    elif objTEX and objUVW in tags and objTEX.GetMaterial().GetName() != objName:
        if checkObjTags(obj, objName)
            print "NO TAG"
        print "We found a UVW tag and have STACKED a TEXTURE."
        # APPLY TAG AFTER CURRENT TAG with UVW Projection
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
        obj.InsertTag(texTag, objTEX)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)



    
    # if the object has ONLY a TEX tag, AND the names DON'T match
    elif objTEX and not objUVW in tags and objTEX.GetMaterial().GetName() != objName:
        if checkObjTags(obj, objName)
            print "NO TAG"
        print "We have STACKED a TEXTURE tag here."
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