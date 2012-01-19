'''
Created on Jan 19, 2012

@author: kerem
'''
if not locals().has_key("tagger_pass"):
    tagger_pass = None
if not locals().has_key("p1_tagger"):
    p1_tagger = None

def set_tagger_pass(tpass):
#    global tagger_pass
    import __builtin__
    __builtin__.tagger_pass = tpass
#    print "Set tagger_pass to %s" % __builtin__.tagger_pass

def get_tagger_pass():
    import __builtin__
#    print "get_tagger_pass() called!! --> %s" % __builtin__.tagger_pass
    return __builtin__.tagger_pass

def set_p1_tagger(tagger):
#    global p1_tagger
    import __builtin__
    __builtin__.p1_tagger = tagger
#    print "Set p1_tagger to %s" % __builtin__.p1_tagger
    
def get_p1_tagger():
#    global p1_tagger
    import __builtin__
    return __builtin__.p1_tagger