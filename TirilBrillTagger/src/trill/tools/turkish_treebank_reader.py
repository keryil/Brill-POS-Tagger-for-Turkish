'''
Created on 17 Ara 2011

@author: Kerem
'''
#from nltk.corpus.reader.api import SyntaxCorpusReader
import nltk, re, os
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import XMLCorpusReader
from xml.etree.cElementTree import ParseError
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
from globalvars import *
from trill.globalvars import get_tagger_pass
win_data_dir = "C:\\Users\\Kerem\\nltk_data"
nix_data_dir = "/home/kerem/nltk_data"
#tag_re = re.compile("\[\(.*?\)*?\(\d,\"(.+?)\"\)\]")
#tag_re = re.compile("\[(\([^\(\)]*?\))*?\(\d+,\"(.+?)\"\)\]")
#tag_re = re.compile("\[(\(\d+,\"[^\"]+?\"\))*?\(\d+,\"([^\"]+?)\"\)\]")
tag_re = re.compile("\[(\(\d+,\".+?\"\))*\(\d+,\"(.+?)\"\)\]")
MAJOR_POS = ["Noun", "Adj", "Adv", "Verb", "Pron", "Conj", "Det", "Postp", \
             "Ques", "Interj", "Num", "Dup", "Punc"]
MINOR_POS = ["Inf", "PastPart", "FutPart", "Prop", "Zero", "PresPart", "DemonsP", \
             "QuesP", "ReflexP", "QuantP", "Card", "Ord", "Percent", "Range", "Real", \
             "Ratio", "Distrib", "Time"]
PERSON = "A1sg,A2sg,A3sg,A1pl,A2pl,A3pl".split(",")
POSSESSIVE = "P1sg,P2sg,P3sg,P1pl,P2pl,P3pl,Pnon".split(",")
CASE = "Nom,Acc,Dat,Loc,Abl,Gen,Ins,Equ".split(",")
VERB_POLARITY = "Pos,Neg".split(",")
VERB_INFLECTION = "Past,Narr,Fut,Aor,Pres,Desr,Cond,Neces,Opt,Imp1,Prog1,Prog2".split(",")
VERB_DERIVATION = "Pass,Caus,Reflex,Receipt,Able,Repeat,Hastilty,EverSince,Almost,Stay,Start".split(",")

P2 = VERB_POLARITY + VERB_INFLECTION + POSSESSIVE

fileids = fileids = None
treebank_path = None
if os.name == "nt":
    treebank_path = os.path.join(win_data_dir, "corpora", "turkish_treebank")
else:
    treebank_path = os.path.join(nix_data_dir, "corpora", "turkish_treebank")
print treebank_path
fileids = [file for file in os.listdir(treebank_path)]

class TurkishTreebankCorpusReader(XMLCorpusReader):
    '''
    classdocs
    '''
    # this is for two-pass tagging
    tagger_mode = "P1"
    def __init__(self, root, fileids, wrap_etree=False, tagger_mode="P1", p1_tagger=None):
        super(TurkishTreebankCorpusReader,self).__init__(root, fileids, wrap_etree)
        self.p1_tagger = p1_tagger
        self.mode = tagger_mode
        
    def words(self, fileids):
        words = []
        for fileid in fileids:
            tree = self.xml(fileid)
    #        print tree
            words_xml = tree.findall("S/W")
            for xml in words_xml:
    #            print xml
                words.append(xml.text.rstrip().lstrip())
                
        return words
    
    def tagged_words(self, fileids):
        words = []
        for id in fileids:
            print "File: %s" % id
            tree = self.xml(id)
            words_xml = tree.findall("S/W")
            words = []
            for word in words_xml:
#                print "\n%s: %s" % (word.get("IX"), word.text)
#                print tostring(word, encoding="utf-8").rstrip()
#                print word.get("IG")
                text = word.text.rstrip().lstrip()
                tag = self._parse_word_tag(word)
                print text, tag
#                print "\n"
                words.append((text, tag))
        return words
    
    def _parse_word_tag(self, word):
        ig = word.get("IG")
#                    print ig
        index, tag = tag_re.search(ig).groups(-1)
        parts = tag.split("+")
        relevant_parts = []
        MINOR = MINOR_POS
        MAJOR = MAJOR_POS
        if get_tagger_pass() == "P1":
            MINOR = MINOR_POS
#                        MINOR = MINOR_POS + CASE + PERSON + VERB_INFLECTION + VERB_POLARITY
        else:
            MINOR = MINOR_POS + VERB_INFLECTION
            
        for part in parts:
            if part not in MAJOR:
                if relevant_parts == []:
                    continue
                else:
                    if part not in MINOR:
                        continue
                    else:
#                                    print "MINOR: %s" % part
                        relevant_parts.append(part)
            else:
#                            print "MAJOR: %s" % part
                relevant_parts.append(part)
#                first_portion = tag.split("+")[0]
#                if text.startswith(first_portion):
#                    tag = tag.replace("%s+" % first_portion, "")
#                print tag
#                print text, tag
        tag = "+".join(relevant_parts)
        return tag
#                    print text, tag
    
    def tagged_sents(self, fileids=fileids):
        sents = []
        for id in fileids:
#            print id
            tree = self.xml(id)
            sents_xml = tree.findall("S")
            sent_p1 = None
            
                    
            for sent_xml in sents_xml:
                sent = []
                if self.mode == "P2":
                    raw_sent = [word.text.rstrip().lstrip() for word in sent_xml]
                    sent_p1 = self.p1_tagger.tag(raw_sent)
                    for word, (text, tag_p1) in zip(sent_xml, sent_p1):
#                        text = word.text.rstrip().lstrip()
                        tag = self._parse_word_tag(word)
        #                print "\n"
                        sent.append((text, (tag_p1, tag)))
                    if sent != []:
                        sents.append(sent)
                else:    
                    for word in sent_xml:
                        text = word.text.rstrip().lstrip()
                        tag = self._parse_word_tag(word)
        #                print "\n"
                        sent.append((text, tag))
                    if sent != []:
                        sents.append(sent)
#                print "Appended %s" % sent
        return sents
    
    
    def sents(self, fileids):
        sents = []
        for fileid in fileids:
            tree = self.xml(fileid)
            sents_xml = tree.findall("S")
            for xml in sents_xml:
                sent = []
                for child in xml:
                    sent.append(child.text.rstrip().lstrip())
                sents.append(sent)
        return sents
    
    
if __name__ == '__main__':
    import os
    print os.getcwd()
    fileids = None
    treebank_path = None
    if os.name == "nt":
        treebank_path = os.path.join(win_data_dir, "corpora", "turkish_treebank")
    else:
        treebank_path = os.path.join(nix_data_dir, "corpora", "turkish_treebank")
    print treebank_path
    fileids = [file for file in os.listdir(treebank_path)]
    print fileids
    turkish_treebank = LazyCorpusLoader(name="turkish_treebank",
                                        reader_cls=TurkishTreebankCorpusReader,
                                        fileids=fileids)
    sents = turkish_treebank.tagged_sents(fileids)
    print len(sents)
#    for sent in sents:
#        print sent
#    print turkish_treebank.words()
#    for file in turkish_treebank.fileids():
#        try:
##            print turkish_treebank.sents(file)
#            print turkish_treebank.tagged_words(file)
#        except ParseError, e:
#            print file
#            tree = ElementTree()
#            tree.parse(open(os.path.join(treebank_path, file)))
#            print tree
#            print "ERROR: %s, %s" % (file, e)