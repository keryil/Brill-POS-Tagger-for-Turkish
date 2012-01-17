# Natural Language Toolkit: Tokenizers
#
# Copyright (C) 2001-2012 NLTK Project
# Author: Edward Loper <edloper@gradient.cis.upenn.edu>
# URL: <http://nltk.sourceforge.net>
# For license information, see LICENSE.TXT

r"""
Penn Treebank Tokenizer

The Treebank tokenizer uses regular expressions to tokenize text as in Penn Treebank.
This is the method that is invoked by ``word_tokenize()``.  It assumes that the
text has already been segmented into sentences, e.g. using ``sent_tokenize()``.

This tokenizer performs the following steps:

  - split standard contractions, e.g. ``don't -> ``do n't``
  - treat most punctuation characters as separate tokens
  - split off commas and single quotes, when followed by whitespace
  - separate periods that appear at the end of line

    >>> from nltk.tokenize import TreebankWordTokenizer
    >>> s = "Good muffins cost $3.88\nin New York.  Please buy me\ntwo of them.\n\nThanks."
    >>> TreebankWordTokenizer().tokenize(s)
    ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.',
    'Please', 'buy', 'me', 'two', 'of', 'them', '.', 'Thanks', '.']

"""

import re
from nltk.tokenize.api import TokenizerI

######################################################################
#{ Regexp-based treebank tokenizer
######################################################################
# (n.b., this isn't derived from RegexpTokenizer)

class TreebankWordTokenizer(TokenizerI):
    """
    A word tokenizer that tokenizes sentences using the conventions
    used by the Penn Treebank.  Contractions are split in to two tokens, e.g.:

      - ``can't -> ca n't``
      - ``he'll -> he 'll``
      - ``weren't -> were n't``

    NB. this tokenizer assumes that the text is presented as one sentence per line,
    where each line is delimited with a newline character.
    The only periods to be treated as separate tokens are those appearing
    at the end of a line.
    """
    # List of contractions adapted from Robert MacIntyre's tokenizer.
    _CONTRACTIONS2 = [re.compile(r"(?i)(.)('ll|'re|'ve|n't|'s|'m|'d)\b"),
                     re.compile(r"(?i)\b(can)(not)\b"),
                     re.compile(r"(?i)\b(D)('ye)\b"),
                     re.compile(r"(?i)\b(Gim)(me)\b"),
                     re.compile(r"(?i)\b(Gon)(na)\b"),
                     re.compile(r"(?i)\b(Got)(ta)\b"),
                     re.compile(r"(?i)\b(Lem)(me)\b"),
                     re.compile(r"(?i)\b(Mor)('n)\b"),
                     re.compile(r"(?i)\b(T)(is)\b"),
                     re.compile(r"(?i)\b(T)(was)\b"),
                     re.compile(r"(?i)\b(Wan)(na)\b")]
    _CONTRACTIONS3 = [re.compile(r"(?i)\b(Whad)(dd)(ya)\b"),
                     re.compile(r"(?i)\b(Wha)(t)(cha)\b")]

    def tokenize(self, text):
        """Return a tokenized copy of *text*, using the tokenization
        conventions of the Penn Treebank.
        """
        for regexp in self._CONTRACTIONS2:
            text = regexp.sub(r'\1 \2', text)
        for regexp in self._CONTRACTIONS3:
            text = regexp.sub(r'\1 \2 \3', text)

        # Separate most punctuation
        text = re.sub(r"(?u)([^\w\.\'\-\/,&])", r' \1 ', text)

        # Separate commas or single quotes if they're followed by space.
        # (E.g., don't separate 2,500)
        text = re.sub(r"([,']\s)", r' \1', text)

        # Separate periods that come before newline or end of string.
        text = re.sub('\. *(\n|$)', ' . ', text)

        return text.split()



if __name__ == "__main__":
    import doctest
    doctest.testmod(optionflags=doctest.NORMALIZE_WHITESPACE)
