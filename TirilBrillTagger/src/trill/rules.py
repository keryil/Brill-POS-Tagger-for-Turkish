'''
Created on Jan 19, 2012

@author: kerem
'''
from nltk.tag.brill import ProximateWordsRule, ProximateTokensTemplate,\
    SymmetricProximateTokensTemplate
class ProximateP1Rule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate1SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's p1 tag."""
        try:
            (tag_p1,tag) = token[1]
            return tag_p1
        except ValueError, err:
            raise Exception("%s: %s" % (token, err))

class Proximate1SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate1SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-1):]
    
class Proximate2SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate2SuffixesRule,self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-2):]

class Proximate3SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate3SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-3):]

class Proximate4SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate4SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-4):]

class Proximate5SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate5SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-5):]

class Proximate6SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate6SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-6):]
    
class Proximate7SuffixesRule(ProximateWordsRule):
    PROPERTY_NAME = "suffix"
    def __init__(self, original_tag, replacement_tag, *conditions):
        super(Proximate7SuffixesRule, self).__init__(original_tag, replacement_tag, *conditions)
        
    @staticmethod
    def extract_property(token):
        """:return: The given token's text."""
        text = token[0]
        return text[max(0, len(text)-7):]

class ProximateSuffixesTemplate(ProximateTokensTemplate):
    def __init__(self, rule_class, *boundaries):
        super(ProximateSuffixesTemplate, self).__init__(rule_class,*boundaries)

class SymmetricProximateSuffixesTemplate(SymmetricProximateTokensTemplate):
    def __init__(self, rule_class, *boundaries):
        super(SymmetricProximateSuffixesTemplate, self).__init__(rule_class,*boundaries)
