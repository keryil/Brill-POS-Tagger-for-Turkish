# -*- coding: utf-8 -*-
'''
Created on 17 Oca 2012

@author: Kerem

This module is here to change the treebank files so that illegal characters are escaped.
'''

import os


win_data_dir = "C:\\Users\\Kerem\\nltk_data\\corpora\\turkish_treebank"
nix_data_dir = "/home/kerem/nltk_data/corpora/turkish_treebank"
#IG='[(1,"Sherlock_holmes'ü+Noun+A3sg+Pnon+Nom")]'
import re
#apos_re = re.compile("IG\d*=\'\[\(\d+,\"([^\)]*?\'[^\)]*?)\"\)\]\'")
#apos_re = re.compile("IG\d*=\'\[(\(([^)(]+?\'[^)(]+?)\)+)\]\'")
apos_re = re.compile("IG\d*=\'\[([^\[\]]*?\'[^\[\]]*?)\]\'")


def change(file_path):
    content = open(file_path).readlines()
    new_lines = []
    for line in content:
        new_line = line
        match = apos_re.search(new_line)
        while match:
            new_line = new_line.replace(match.group(1), match.group(1).replace("'", "&apos;"))
            match = apos_re.search(new_line)
        new_lines.append(new_line)
    f = open(file_path, "w")
    f.writelines(new_lines)

if __name__ == '__main__':
#    line1 = """<W IX="10" LEM="" MORPH=" " IG='[(1,"Sherlock_holmes'ü+Noun+A3sg+Pnon+Nom")]' REL="[12,1,(OBJECT)]" ORG_IG1='[(1,"sherlock+Noun+A3sg+Pnon+Nom")]' ORG_IG2='[(1,"holmes'ü+Noun+A3sg+Pnon+Nom")]'> Sherlock_Holmes'ü </W>"""
#    line2 = """<W IX="11" LEM="" MORPH=" " IG='[(1,"20'li_30+Num+Card")(2,"Noun+Zero+A3sg+Pnon+Nom")(3,"Adj+With")(4,"Noun+Zero+A3sg+Pnon+Nom")]' REL="[12,1,(MODIFIER)]" ORG_IG1='[(1,"20+Num+Card")(2,"Noun+Zero+A3sg+Pnon+Nom")(3,"Adj+With")(4,"Noun+Zero+A3sg+Pnon+Nom")]' ORG_IG2='[(1,"30+Num+Card")(2,"Noun+Zero+A3sg+Pnon+Nom")(3,"Adj+With")(4,"Noun+Zero+A3sg+Pnon+Nom")]'> 20'li_30'lu </W>"""
    data = win_data_dir
#    new_line = line1
#    match = apos_re.search(new_line)
#    while match:
#        print "Replacing %s" % match.group(1)
#        new_line = new_line.replace(match.group(1), match.group(1).replace("'", "&apos;"))
#        match = apos_re.search(new_line)
#    print line1
#    print new_line
#    
#    new_line = line2
#    match = apos_re.search(new_line)
#    while match:
#        print "Replacing %s" % match.group(1)
#        new_line = new_line.replace(match.group(1), match.group(1).replace("'", "&apos;"))
#        match = apos_re.search(new_line)
#    print line2
#    print new_line
#    
#    exit()
    
    if os.name != "nt":
        data = nix_data_dir
    for file in os.listdir(data):
        change(os.path.join(data,file))