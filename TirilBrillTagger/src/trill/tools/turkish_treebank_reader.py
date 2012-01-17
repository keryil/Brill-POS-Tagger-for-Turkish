'''
Created on 17 Ara 2011

@author: Kerem
'''
#from nltk.corpus.reader.api import SyntaxCorpusReader
from nltk.corpus.util import LazyCorpusLoader
from nltk.corpus.reader import XMLCorpusReader
from xml.etree.cElementTree import ParseError

class TurkishTreebankCorpusReader(XMLCorpusReader):
    '''
    classdocs
    '''

    def abc(self):
        pass
      
if __name__ == '__main__':
    import os
    print os.getcwd()
    fileids = [line.rstrip() for line in open("../filelist.txt")]
    print fileids
    turkish_treebank = LazyCorpusLoader(name="turkish_treebank", 
                                        reader_cls=TurkishTreebankCorpusReader,
                                        fileids=fileids)
#    print turkish_treebank.words()
    for file in turkish_treebank.fileids():
        try:
#            continue
            print turkish_treebank.words(file)
        except ParseError, e:
            print "ERROR: file, e"