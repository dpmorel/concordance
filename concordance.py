from __future__ import absolute_import, unicode_literals

import codecs
import datetime
import re
import os
import segment
import string
import sys
import treebank

WORDPUNCT_TOKENIZER = re.compile(r'\w+|[^\w\s]+').findall

def sentence_segmenter(fp):
    """
    Transform text from a file into a list of sentences.
    Uses segtok sentence segmentation https://github.com/fnl/segtok
    """
    if hasattr(fp, 'read'):
        sentences = segment.split_multi(fp.read())
        return sentences

    if isinstance(fp, basestring):
        return segment.split_multi(fp)

    raise ValueError('fp is of unknown type for parsing')


def newline_segmenter(fp):
    """
    Does nothing, should probably just use a lambda
    """
    return fp


def to_file(filename, concordance):
    """
    Open a file and write the concordance to the file.
    """
    out = open(filename, 'w')
    out.write(to_string(concordance))
    out.close()


def to_string(concordance):
    """
    Sorts the concordance alphabetically and writes to string.
    """
    def item_to_string(item):
        return "{}: {}".format(item['frequency'], ','.join(item['line_num_list']))

    words = concordance.keys()
    words.sort()
    return "\n".join(
        [
            "{0: <30} {{ {1} }}".format( words[j], item_to_string(concordance[words[j]]))
            for j in range(0, len(words))
        ]
    )


def concord_token(token, concordance, line_num, is_new_token):
    """
    Update the concordance with the token either adding a new token to the concordance
    or updating the existing token in the dict with an increased frequency and new line number.

    Initially I made the 'update' of an existing token immutable, such that it cloned the list
    each time and then appended.  This resulted in significant slowness during the clone, thus
    mutable approach.
    """
    if len(token) > 0:
        if (is_new_token):
            concordance[token]['frequency'] += 1
            concordance[token]['line_num_list'].append(str(line_num))
        else:
            concordance[token] = {
                'frequency': 1,
                'line_num_list': [str(line_num)]
            }


def tokenize_segment(segment, index, concordance={}, tokenizer=WORDPUNCT_TOKENIZER):
    """
    Tokenizes the segment.  A segment is typically a line or a sentence.
    Tokenizing splits it into parts by the given tokenizer, for instance it may
    create tokens of words and punctuation
    """
    [
        concord_token(
            token.lower(),
            concordance,
            index,
            token.lower() in concordance
        )
        for token in tokenizer(segment) if len(token) > 0
    ]
    return concordance


def segmentize_text(fp, concordance={}, segmenter = newline_segmenter, tokenizer = WORDPUNCT_TOKENIZER):
    """
    This is the main method.

    Create a concordance, first by iterating the file into segments,
    then by iterating the segments into tokens (usually words)
    and then by handling each token by creating a dict

    Assumptions:
    1.  We're only doing lower case because I just felt it made sense.
    New and new, we'd probably want to count as the same words
    2.  I've been leaving in punctuation, though I keep toying with adding/removing it.
    """
    [
        tokenize_segment(segment, index, concordance, tokenizer)
        for index, segment in enumerate(segmenter(fp)) if len(segment) > 0
    ]
    return concordance


def execute_concordance(fp, filename, concordance={}, segmenter = newline_segmenter, tokenizer = WORDPUNCT_TOKENIZER, name = 'concord'):
    """
    Executor that wraps the concordance in a stop watch and outputs the results to file
    """
    start = datetime.datetime.now()
    concordance = segmentize_text(fp, concordance, segmenter, tokenizer)
    end = datetime.datetime.now()
    print "{0: <15} {1}ms {2} keys".format(name, (end-start), len(concordance.keys()))
    outfilename = "out/{}_{}_concordance.txt".format(
        os.path.splitext(os.path.basename(filename))[0],
        name)
    to_file(outfilename, concordance)
    print "concordance output at {}".format(outfilename)


def treebank_concordance(fp, filename, concordance={}):
    """
    Treebank concordance algorithm uses Treebank tokenizer as described in treebank.py to
    create a concordance from text.  Treebank alorithm relies on sentence segmentation to optimally
    create a concordance.

    The reason Treebank looked like an interesting and better algorithm to a simple regex tokenizer is the way it
    handles punctuation.

    >>> from nltk.tokenize import TreebankWordTokenizer
    >>> s = '''Good muffins cost $3.88\\nin New York.  Please buy me\\ntwo of them.\\nThanks.'''
    >>> TreebankWordTokenizer().tokenize(s)
    ['Good', 'muffins', 'cost', '$', '3.88', 'in', 'New', 'York.', 'Please', 'buy', 'me', 'two', 'of', 'them.', 'Thanks', '.']
    >>> s = "They'll save and invest more."
    >>> TreebankWordTokenizer().tokenize(s)
    ['They', "'ll", 'save', 'and', 'invest', 'more', '.']
    >>> s = "hi, my name can't hello,"
    >>> TreebankWordTokenizer().tokenize(s)
    ['hi', ',', 'my', 'name', 'ca', "n't", 'hello', ',']
    """
    execute_concordance(fp, filename, concordance, sentence_segmenter, treebank.TreebankWordTokenizer().tokenize, 'treebank')

def wordpunct(fp, filename, concordance={}):
    """
    The word and punctuation concordance algorithm uses a simple regex to tokenize
    words based on characters and punctuation.  It tokens as below (taken from NLTK description):

    >>> from nltk.tokenize import WordPunctTokenizer
    >>> s = "Good muffins cost $3.88\\nin New York.  Please buy me\\ntwo of them.\\n\\nThanks."
    >>> WordPunctTokenizer().tokenize(s)
        ['Good', 'muffins', 'cost', '$', '3', '.', '88', 'in', 'New', 'York',
        '.', 'Please', 'buy', 'me', 'two', 'of', 'them', '.', 'Thanks', '.']
    """
    execute_concordance(fp, filename, concordance, newline_segmenter, WORDPUNCT_TOKENIZER, 'wordpunct')
