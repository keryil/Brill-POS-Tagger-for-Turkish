'''
Created on 17 Ara 2011

@author: Kerem
'''
#from nltk.corpus.reader.api import SyntaxCorpusReader
import nltk
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import XMLCorpusReader
from xml.etree.cElementTree import ParseError

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
    fileids = [file for file in os.listdir("../../../res/treebank/")]
#    print fileids
    turkish_treebank = LazyCorpusLoader(name="turkish_treebank", 
                                        reader_cls=TurkishTreebankCorpusReader,
                                        fileids=fileids)
#    print turkish_treebank.words()
    for file in turkish_treebank.fileids():
        try:
            print turkish_treebank.sents(file)
        except ParseError, e:
            print "ERROR: %s, %s" % (file, e)