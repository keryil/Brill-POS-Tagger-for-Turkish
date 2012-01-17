'''
Created on 17 Ara 2011

@author: Kerem
'''
#from nltk.corpus.reader.api import SyntaxCorpusReader
import nltk
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import XMLCorpusReader
from xml.etree.cElementTree import ParseError
win_data_dir = "C:\\Users\\Kerem\\nltk_data"
nix_data_dir = "/home/kerem/nltk_data"
class TurkishTreebankCorpusReader(XMLCorpusReader):
    '''
    classdocs
    '''
    
    
    def sents(self, fileid):
        tree = self.xml(fileid)
        sents_xml = tree.findall("S")
        sents = []
        for xml in sents_xml:
            for child in xml:
                sents.append(child.text)
      
if __name__ == '__main__':
    import os
    print os.getcwd()
    fileids = None
    treebank_path = None
    if os.name == "nt":
        treebank_path = os.path.join(win_data_dir,"corpora", "turkish_treebank")
    else:
        treebank_path = os.path.join(nix_data_dir,"corpora", "turkish_treebank")
    print treebank_path
    fileids = [file for file in os.listdir(treebank_path)]
#    print fileids
    turkish_treebank = LazyCorpusLoader(name="turkish_treebank", 
                                        reader_cls=TurkishTreebankCorpusReader,
                                        fileids=fileids)
#    print turkish_treebank.words()
    for file in turkish_treebank.fileids():
        try:
            turkish_treebank.sents(file)
        except ParseError, e:
            print "ERROR: %s, %s" % (file, e)