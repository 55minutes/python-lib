def intersect(s1, s2):
    d = {}
    if len(s1) < len(s2):  # iterate over the longer list
        s1,s2 = s2,s1
    for x in s1:
        d[x] = 1
    return unique(filter(d.has_key, s2))

def union(s1, s2):
    return unique(s1 + s2)

def minus(s1, s2):
    d={}
    for x in s1:
        d[x] = 1
    for x in s2:
        if d.has_key(x):
            del(d[x])
    return d.keys()

def unique(s1):
    d = {}
    for x in s1:
        d[x] = 1
    return d.keys()

def duplicates(s1):
    d = {}
    dups = []
    for x in s1:
        d[x] = d.get(x, 0) + 1
    try:
        looper = d.iteritems()
    except:
        looper = d.items()
    for k, v in looper:
        if v > 1:
            dups.append(k)
    return dups