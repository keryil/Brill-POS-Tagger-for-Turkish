'''
Created on Jan 19, 2012

@author: kerem
'''
from nltk.tag.brill import ProximateTokensTemplate,\
    SymmetricProximateTokensTemplate, ProximateTokensRule
from nltk.tag.util import untag
#from trill import tagger
from trill.globalvars import get_p1_tagger, get_tagger_pass, set_tagger_pass
    
class ProximateTokensTemplate(ProximateTokensTemplate):
    def _applicable_conditions(self, tokens, index, start, end):
            """
            :return: A set of all conditions for proximate token rules
            that are applicable to *tokens[index]*, given boundaries of
            (start, end).  I.e., return a list of all tuples
            (start, end, value), such the property value of at least one token
            between *index+start* and *index+end* (inclusive) is *value*.
            """
            
            conditions = []
            try:
                s = max(0, index+start)
            except TypeError, e:
                raise Exception("%s\n%s, %s, %s" % (e, index, start, end))
            e = min(index+end+1, len(tokens))
            p1_tokens = None
            if get_tagger_pass() == "P2":
                set_tagger_pass("P1")
                p1_tokens = get_p1_tagger().tag(untag(tokens))
                set_tagger_pass("P2")
            for i in range(s, e):
                value = None
                if get_tagger_pass() == "P1":
                    value = self._rule_class.extract_property(tokens[i])
                else:
                    try:
                        value = self._rule_class.extract_property(tokens[i], p1_token=p1_tokens[i])
                    except TypeError, err:
                        raise Exception("tokens: %s, p1_tokens: %s, tagger_pass: %s\n%s" % (tokens,p1_tokens,get_tagger_pass(),err))
                conditions.append( (start, end, value) )
            return conditions
    
class SymmetricProximateTokensTemplate(SymmetricProximateTokensTemplate):
    """
    Simulates two ``ProximateTokensTemplate`` templates which are symmetric
    across the location of the token.  For rules of the form "If the
    *n*th token is tagged ``A``, and any tag preceding or following
    the *n*th token by a distance between x and y is ``B``, and
    ... , then change the tag of the *n*th token from ``A`` to ``C``."

    One ``ProximateTokensTemplate`` is formed by passing in the
    same arguments given to this class's constructor: tuples
    representing intervals in which a tag may be found.  The other
    ``ProximateTokensTemplate`` is constructed with the negative
    of all the arguments in reversed order.  For example, a
    ``SymmetricProximateTokensTemplate`` using the pair (-2,-1) and the
    constructor ``SymmetricProximateTokensTemplate`` generates the same rules as a
    ``SymmetricProximateTokensTemplate`` using (-2,-1) plus a second
    ``SymmetricProximateTokensTemplate`` using (1,2).

    This is useful because we typically don't want templates to
    specify only "following" or only "preceding"; we'd like our
    rules to be able to look in either direction.

    Construct a template for generating proximate token brill
    rules.

    :type rule_class: class
    :param rule_class: The proximate token brill rule class that
        should be used to generate new rules.  This class must be a
        subclass of ``ProximateTokensRule``.
    :type boundaries: tuple(int, int)
    :param boundaries: A list of tuples (start, end), each of
        which specifies a range for which a condition should be
        created by each rule.
    :raise ValueError: If start>end for any boundary.
    """

    def __init__(self, rule_class, *boundaries):
        self._ptt1 = ProximateTokensTemplate(rule_class, *boundaries)
        reversed = [(-e,-s) for (s,e) in boundaries]
        self._ptt2 = ProximateTokensTemplate(rule_class, *reversed)
    

class ProximateTokensRule(ProximateTokensRule):
    def applies(self, tokens, index):
        
                    
        # Inherit docs from BrillRule

        # Does the given token have this rule's "original tag"?
        if tokens[index][1] != self.original_tag:
            return False

        # Check to make sure that every condition holds.
        for (start, end, val) in self._conditions:
            # Find the (absolute) start and end indices.
            s = max(0, index+start)
            e = min(index+end+1, len(tokens))
            p1_tokens = None
            if get_tagger_pass() == "P2":
                set_tagger_pass("P1")
                p1_tokens = get_p1_tagger().tag(untag(tokens))
                set_tagger_pass("P2")
            # Look for *any* token that satisfies the condition.
            for i in range(s, e):
                if get_tagger_pass() == "P1":
                    if self.extract_property(tokens[i]) == val:
                        break
                elif get_tagger_pass() == "P2":
                    if self.extract_property(tokens[i], p1_token=p1_tokens[i]) == val:
                        break
                else:
                    raise Exception("Invalid tagger_pass: %s" % (get_tagger_pass()))
            else:
                # No token satisfied the condition; return false.
                return False

        # Every condition checked out, so the rule is applicable.
        return True
    
class ProximateTagsRule(ProximateTokensRule):
    """
    A rule which examines the tags of nearby tokens.
    See ``ProximateTokensRule`` for details.
    Also see ``SymmetricProximateTokensTemplate`` which generates these rules.
    """
    PROPERTY_NAME = 'tag' # for printing.
    yaml_tag = '!ProximateTagsRule'
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's tag."""
        return token[1]

class ProximateWordsRule(ProximateTokensRule):
    """
    A rule which examines the base types of nearby tokens.
    See ``ProximateTokensRule`` for details.
    Also see ``SymmetricProximateTokensTemplate`` which generates these rules.
    """
    PROPERTY_NAME = 'text' # for printing.
    yaml_tag = '!ProximateWordsRule'
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        return token[0]

class ProximateP1Rule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(ProximateP1Rule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's p1 tag."""
        try:
            word, p1_tag = p1_token
            return p1_tag
        except ValueError, err:
            raise Exception("%s, %s: %s" % (token, p1_token, err))

class Proximate1PrefixesRule(ProximateWordsRule):
    PROPERTY_NAME = "prefix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate1PrefixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[:min(1, len(text)-1)]
    
class Proximate2PrefixesRule(ProximateWordsRule):
    PROPERTY_NAME = "prefix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate2PrefixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[:min(2, len(text)-1)]

class Proximate3PrefixesRule(ProximateWordsRule):
    PROPERTY_NAME = "prefix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate3PrefixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[:min(3, len(text)-1)]

class Proximate4PrefixesRule(ProximateWordsRule):
    PROPERTY_NAME = "prefix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate4PrefixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[:min(4, len(text)-1)]

class Proximate5PrefixesRule(ProximateWordsRule):
    PROPERTY_NAME = "prefix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate5PrefixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[:min(5, len(text)-1)]

class Proximate6PrefixesRule(ProximateWordsRule):
    PROPERTY_NAME = "prefix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate6PrefixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[:min(6, len(text)-1)]

class Proximate1SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate1SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-1):]
    
class Proximate2SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate2SuffixesRule,self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-2):]

class Proximate3SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate3SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-3):]

class Proximate4SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate4SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-4):]

class Proximate5SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate5SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-5):]

class Proximate6SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate6SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-6):]
    
class Proximate7SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate7SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token, p1_token=None):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-7):]

class ProximateSuffixesTemplate(ProximateTokensTemplate):
    def __init__(self, rule_class, *boundaries):
        super(ProximateSuffixesTemplate, self).__init__(rule_class,*boundaries)

class SymmetricProximateSuffixesTemplate(SymmetricProximateTokensTemplate):
    def __init__(self, rule_class, *boundaries):
        super(SymmetricProximateSuffixesTemplate, self).__init__(rule_class,*boundaries)
