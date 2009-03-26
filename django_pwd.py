#!/bin/env python

def gen_password(raw_password):
    import sha, random
    algo = 'sha1'
    salt = sha.new(str(random.random())).hexdigest()[:5]
    hsh = sha.new(salt+raw_password).hexdigest()
    return '%s$%s$%s' % (algo, salt, hsh)

if __name__ == '__main__':
    import sys
    print gen_password(sys.argv[1])