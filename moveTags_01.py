import c4d
from c4d import gui
#Welcome to the world of Python



def moveExistingTags(obj):
    firstTag = obj.GetFirstTag()
    
    # me. referes to the tag. we need to store a temp variable so that we can remove the tag after we've got to the next tag    
    lastTag = firstTag

    # iterate over the tags to find the last one
    if lastTag:
        while True:
            if not lastTag.GetNext():
                break
            lastTag = lastTag.GetNext()

        firstTag.Remove()

        obj.InsertTag(firstTag, lastTag)
    
    return firstTag



def main():
    obj = doc.GetFirstObject()
    
    moveExistingTags(obj)

    c4d.EventAdd()


if __name__=='__main__':
    main()
