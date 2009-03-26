from django.models.imageview import images

def getPersonOrder():
    dateDict = {}

    # Get a list of photographer IDs
    ids = [x.values()[0] for x in images.get_values(fields=['photographer'], distinct=True)]

    # For each photographer, get the latest upload_date
    for i in ids:
        im = images.get_latest(photographer__id__exact=i)
        dateDict[im.upload_date] = i

    keys = dateDict.keys()
    keys.sort(reverse=True)
    plist = []
    for k in keys:
        plist.append(dateDict[k])

    return plist

def alternatePersonList():
    plist = getPersonOrder()

    implist = []
    for p in plist:
        implist.append(images.get_list(photographer__id__exact=p,
                                       order_by=['upload_date']))
    return implist

def _dummy():
    pass

def rearrange():
    implist = alternatePersonList()
    ims = []
    for i in range(max(len(x) for x in implist)):
        for j in range(len(implist)):
            try:
                ims.append(implist[j].pop())
            except:
                pass

    pic_index = len(ims)

    for im in ims:
        im.picture_index = pic_index
        im._pre_save = _dummy
        im.save()
        pic_index -=1

if __name__ == '__main__':
    rearrange()
