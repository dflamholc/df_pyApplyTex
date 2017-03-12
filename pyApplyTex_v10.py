"""
Name-US: df_pyApplyTex_v0.1(v10) 12-03-2017
Description-US: Places textures on all objects in hierarchy baed on object->material matching names. 
Author: David Flamholc, vfxvoodoo.com

"""

# pyApplyTex_version
pyApply = "df_pyApplyTex_v0.1(v10) 12-03-2017"

"""
LICENSE
-------
    Copyright (c) 2016, David Flamholc, VFXVoodoo.com
    Programming: David Flamholc <dflamholc@gmail.com>

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
    WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
    COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
    OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

CHANGE LOG
----------
version: paApplyTex_v08
    - implemented UNDO functions

version: paApplyTex_v09
    - implemented moving newly created tags to last in the stack

version: paApplyTex_v10  -- (df_pyApplyTex_v0.1(v10) 12-03-2017)
    - refactoring of funcitons and variables
    - and FLOW comments
    - scrip header INFO and TO DO list added 


KNOWN BUGS
------------------------
     - object that already have a non matching material on them will keep stacking new matching materials endlessly


INSTRUCTIONS & DEV NOTES
------------------------
    - objects and materials need to have exactly the same name for this script to work 
    - This Software should work on all os platforms.
    - It has only been tested on Cinema 4D r18.

TO DO -- FEATURE IDEAS
-----------------------
    [x] Write script comments
    [] Create Icon
    [] Write Usage Instructions
    [] Convert to Plugin
        [] Get Unique ID
 
    [] check part of name so that matching can be done by _TOKEN only on either material or object
    [] fix material stacking BUG on object that already have a non matching tex tag applied
    [] ADD feature to control mapping of Tex tag X & LENGTH from text file
        Length U == Texture[c4d.TEXTURETAG.LENGTHX] & Length V == Texture[c4d.TEXTURETAG.LENGTHY]
        these are presented in 0%-100% but work in normalised float values 0-1

"""

#====== MODULE IMPORT ======#

import c4d, os

# FUNCTIONS ##############################################################################################

def moveExistingTags(obj):
    firstTag = obj.GetFirstTag()  
    lastTag = firstTag
    tagList = []

    if lastTag:
        while True:
            tagList.append(lastTag)
            if not lastTag.GetNext():
                break
            lastTag = lastTag.GetNext()
            

        # add a CHANGE undo
        doc.AddUndo(c4d.UNDOTYPE_CHANGE, firstTag)
        
        # remove the first tag and insert after last tag
        firstTag.Remove()
        obj.InsertTag(firstTag, lastTag)

    # not sure what we need this list for yet.
    return tagList


def placeTags(obj, objName, matList, matNames):
    tags = obj.GetTags()
    texTag = c4d.TextureTag()
    objTEX = obj.GetTag(c4d.Ttexture)
    objUVW = obj.GetTag(c4d.Tuvw)
    setMAT = matList[matNames.index(objName)]

    # this function is called on every object that with matching material
    # the tags list has been created in the checkName function

    # if the object has a tex tag and the names match - DO NOTING
    if objTEX in tags and objTEX.GetMaterial().GetName() == objName:
        print "This object already has a material applied, matching the object name."

    # IF TEHRE ARE TWO STACKED MATERIALS ONE OF WHICH MATCH THE NAME THEN IGNORE
    elif objTEX in tags and objTEX.GetMaterial().GetName() != objName and objTEX.GetMaterial().GetName() == objName:
        print "This object seems to already have two TEX tags applied."

    # if the object has a TEX tag and a UVW tag, BUT the names DON'T match:
    elif objTEX and objUVW in tags and objTEX.GetMaterial().GetName() != objName:
            # if objTEX.GetMaterial().GetName() == objName:
            #     print "We have already applied both a TEXTURE and UVW tag here."    
            #     break
        print "We found a UVW tag and have STACKED a TEXTURE."
        # APPLY TAG AFTER CURRENT TAG with UVW Projection
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_UVW
        obj.InsertTag(texTag, objTEX)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)
    
    # if the object has ONLY a TEX tag, AND the names DON'T match
    elif objTEX and not objUVW in tags and objTEX.GetMaterial().GetName() != objName:
            # if tag.GetMaterial().GetName() == objName:
            #     print "We have already applied TEXTURE tag here."
            #     break
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

    else:
        # if the object has NONE tags then apply  
        print "TEXTURE tag with name matching the object's has been applied!"
        texTag.SetMaterial(setMAT)
        texTag[c4d.TEXTURETAG_PROJECTION] = c4d.TEXTURETAG_PROJECTION_CUBIC
        obj.InsertTag(texTag)
        doc.AddUndo(c4d.UNDOTYPE_NEW, texTag)

        # move existing material tags to last tag
        moveExistingTags(obj)


def checkName(obj):
    objName = obj.GetName()
    matNames = []
    matList = doc.GetMaterials()

    for mat in matList:
        mName = mat.GetName()
        matNames.append(mName)
    
    # check if the object has a matching material
    try:
        if objName in matNames:
            placeTags(obj, objName, matList, matNames)
        else:
            print "Texture Not Found!"
    except:
        raise StopIteration
    

def recurseObjs(obj, checkName):
    while obj:
        checkName(obj)
        recurseObjs(obj.GetDown(), checkName)
        obj = obj.GetNext()
    return obj


# MAIN ##############################################################################################

def main():
    doc = c4d.documents.GetActiveDocument()
    obj = doc.GetFirstObject()

    # start UNDO
    doc.StartUndo()

    # call the recursive function with callback
    recurseObjs(obj, checkName)

    # end UNDO
    doc.EndUndo()
    
    # update the Cinema 4D UI
    c4d.EventAdd()

if __name__=='__main__':
    
    # THE FLOW ######
    # in the MAIN function we call the recurseObjs function
    # recurseObjs iterates through the hierarchy and calls the checkName function on every object
    # checkName checks the objects name against the names in the material list and runs placeTags
    # placeTags checks the objects tag types
        # 

    main()