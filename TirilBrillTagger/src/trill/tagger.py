'''
Created on Jan 18, 2012

@author: kerem
'''
from nltk.corpus.util import LazyCorpusLoader

win_data_dir = "C:\\Users\\Kerem\\nltk_data"
nix_data_dir = "/home/kerem/nltk_data"
import os, yaml
def error_list (train_sents, test_sents, radius=2):
    """
    Returns a list of human-readable strings indicating the errors in the
    given tagging of the corpus.

    :param train_sents: The correct tagging of the corpus
    :type train_sents: list(tuple)
    :param test_sents: The tagged corpus
    :type test_sents: list(tuple)
    :param radius: How many tokens on either side of a wrongly-tagged token
        to include in the error string.  For example, if radius=2,
        each error string will show the incorrect token plus two
        tokens on either side.
    :type radius: int
    """
    hdr = (('%25s | %s | %s\n' + '-'*26+'+'+'-'*24+'+'+'-'*26) %
           ('left context', 'word/test->gold'.center(22), 'right context'))
    errors = [hdr]
    for (train_sent, test_sent) in zip(train_sents, test_sents):
        for wordnum, (word, train_pos) in enumerate(train_sent):
            test_pos = test_sent[wordnum][1]
            if train_pos != test_pos:
                left = ' '.join('%s/%s' % w for w in train_sent[:wordnum])
                right = ' '.join('%s/%s' % w for w in train_sent[wordnum+1:])
                mid = '%s/%s->%s' % (word, test_pos, train_pos)
                errors.append('%25s | %s | %s' %
                              (left[-25:], mid.center(22), right[:25]))

    return errors

def demo(num_sents=5635, max_rules=200, min_score=3,
         error_output="errors.out", rule_output="rules.yaml",
         randomize=False, train=.8, trace=3):
    """
    Brill Tagger Demonstration

    :param num_sents: how many sentences of training and testing data to use
    :type num_sents: int
    :param max_rules: maximum number of rule instances to create
    :type max_rules: int
    :param min_score: the minimum score for a rule in order for it to
        be considered
    :type min_score: int
    :param error_output: the file where errors will be saved
    :type error_output: str
    :param rule_output: the file where rules will be saved
    :type rule_output: str
    :param randomize: whether the training data should be a random subset
        of the corpus
    :type randomize: bool
    :param train: the fraction of the the corpus to be used for training
        (1=all)
    :type train: float
    :param trace: the level of diagnostic tracing output to produce (0-4)
    :type trace: int
    """

    from trill.tools.turkish_treebank_reader import TurkishTreebankCorpusReader 
    from nltk import tag
    from nltk.tag import brill
    
    if os.name == "nt":
        treebank_path = os.path.join(win_data_dir, "corpora", "turkish_treebank")
    else:
        treebank_path = os.path.join(nix_data_dir, "corpora", "turkish_treebank")
    print treebank_path
    fileids = [f for f in os.listdir(treebank_path)]
    
    treebank = LazyCorpusLoader(name="turkish_treebank",
                                        reader_cls=TurkishTreebankCorpusReader,
                                        fileids=fileids)
    nn_cd_tagger = tag.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD'),
                                     (r'.*', 'NN')])

    # train is the proportion of data used in training; the rest is reserved
    # for testing.
    print "Loading tagged data... "
    tagged_data = treebank.tagged_sents()
    if randomize:
        random.seed(len(sents))
        random.shuffle(sents)
    cutoff = int(num_sents*train)
    training_data = tagged_data[:cutoff]
    gold_data = tagged_data[cutoff:num_sents]
    testing_data = [[t[0] for t in sent] for sent in gold_data]
    print "Done loading."

    # Unigram tagger
    print "Training unigram tagger:"
    unigram_tagger = tag.UnigramTagger(training_data,
                                       backoff=nn_cd_tagger)
    if gold_data:
        print "    [accuracy: %f]" % unigram_tagger.evaluate(gold_data)

    # Bigram tagger
    print "Training bigram tagger:"
    bigram_tagger = tag.BigramTagger(training_data,
                                     backoff=unigram_tagger)
    if gold_data:
        print "    [accuracy: %f]" % bigram_tagger.evaluate(gold_data)

    # Brill tagger
    templates = [
      brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,1)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (2,2)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,2)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateTagsRule, (1,3)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,1)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (2,2)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,2)),
      brill.SymmetricProximateTokensTemplate(brill.ProximateWordsRule, (1,3)),
      brill.ProximateTokensTemplate(brill.ProximateTagsRule, (-1, -1), (1,1)),
      brill.ProximateTokensTemplate(brill.ProximateWordsRule, (-1, -1), (1,1)),
      ]
    trainer = brill.FastBrillTaggerTrainer(bigram_tagger, templates, trace)
    #trainer = brill.BrillTaggerTrainer(u, templates, trace)
    brill_tagger = trainer.train(training_data, max_rules, min_score)

    if gold_data:
        print("\nBrill accuracy: %f" % brill_tagger.evaluate(gold_data))

    if trace <= 1:
        print("\nRules: ")
        for rule in brill_tagger.rules():
            print(str(rule))

    print_rules = file(rule_output, 'w')
    yaml.dump(brill_tagger, print_rules)
    print_rules.close()

    testing_data = brill_tagger.batch_tag(testing_data)
    error_file = file(error_output, 'w')
    error_file.write('Errors for Brill Tagger %r\n\n' % rule_output)
    for e in error_list(gold_data, testing_data):
        error_file.write(e+'\n')
    error_file.close()
    print ("Done; rules and errors saved to %s and %s." %
           (rule_output, error_output))


if __name__ == '__main__':
    demo()
    pass