def set_sources(src_dict):
    sdict = {}
    for k, url in src_dict.iteritems():
        sdict[k] = {'svn_url': url}
    return sdict
