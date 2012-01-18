'''
Created on 17 Ara 2011

@author: Kerem
'''
#from nltk.corpus.reader.api import SyntaxCorpusReader
import nltk, re
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import XMLCorpusReader
from xml.etree.cElementTree import ParseError
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import tostring
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
class TurkishTreebankCorpusReader(XMLCorpusReader):
    '''
    classdocs
    '''
    
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
                ig = word.get("IG")
                print ig
                index, tag = tag_re.search(ig).groups(-1)
#                print tag
                parts = tag.split("+")
                relevant_parts = []
#                print parts
                for part in parts:
                    if part not in MAJOR_POS:
                        if relevant_parts == []:
                            continue
                        else:
                            if part not in MINOR_POS:
                                break
                            else:
                                print "MINOR: %s" % part
                                relevant_parts.append(part)
                    else:
                        print "MAJOR: %s" % part
                        relevant_parts.append(part)
#                first_portion = tag.split("+")[0]
#                if text.startswith(first_portion):
#                    tag = tag.replace("%s+" % first_portion, "")
#                print tag
#                print text, tag
                tag = "+".join(relevant_parts)
                print text, tag
#                print "\n"
                words.append((text, tag))
        return words
    
    def tagged_sents(self, fileids):
        sents = []
        for id in fileids:
#            print id
            tree = self.xml(id)
            sents_xml = tree.findall("S")
            for sent_xml in sents_xml:
                sent = []
                for word in sent_xml:
                    text = word.text.rstrip().lstrip()
                    ig = word.get("IG")
#                    print ig
                    index, tag = tag_re.search(ig).groups(-1)
                    parts = tag.split("+")
                    relevant_parts = []
                    for part in parts:
                        if part not in MAJOR_POS:
                            if relevant_parts == []:
                                continue
                            else:
                                if part not in MINOR_POS:
                                    break
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
#                    print text, tag
    #                print "\n"
                    sent.append((text, tag))
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
#    print fileids
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
