from __future__ import absolute_import, division, unicode_literals
import treebank
import unittest

from concordance import segmentize_text, newline_segmenter, sentence_segmenter, WORDPUNCT_TOKENIZER

def test(text):
    return segmentize_text(text, {}, newline_segmenter, WORDPUNCT_TOKENIZER)

class TestWordPunct(unittest.TestCase):

    def test_empty(self):
        testy = None
        c = test(testy)
        self.assertTrue(len(c.keys()) == 0)
        self.assertTrue(c == {})

    def test_empty(self):
        c = test([])
        self.assertTrue(len(c.keys()) == 0)
        self.assertTrue(c == {})

    def test_no_text(self):
        c = test([''])
        self.assertTrue(len(c.keys()) == 0)
        self.assertTrue(c == {})

    def test_single_space(self):
        c = test([' '])
        self.assertTrue(len(c.keys()) == 0)
        self.assertTrue(c == {})

    def test_punctuation_only(self):
        c = test(['!!!'])
        self.assertTrue(len(c.keys()) == 1)
        self.assertIsNotNone(c['!!!'])
        self.assertTrue(c['!!!']['frequency'] == 1)

    def test_name(self):
        c = test(['Mr. Dan'])
        self.assertTrue(len(c.keys()) == 3)
        self.assertIsNotNone(c['mr'])
        self.assertIsNotNone(c['dan'])
        self.assertIsNotNone(c['.'])

    def multi_frequency(self):
        c = test(['Mr. Dan', 'Mr. Dan'])
        self.assertTrue(len(c.keys()) == 2)
        self.assertTrue(c['mr']['frequency'] == 2)
        self.assertTrue(c['dan']['frequency'] == 2)

def treebank_test(text):
    return segmentize_text(text, {}, sentence_segmenter, treebank.TreebankWordTokenizer().tokenize)

class TestTreeBank(unittest.TestCase):

    def test_no_text(self):
        c = treebank_test('')
        self.assertTrue(len(c.keys()) == 0)
        self.assertTrue(c == {})

    def test_single_space(self):
        c = treebank_test(' ')
        self.assertTrue(len(c.keys()) == 0)
        self.assertTrue(c == {})

    def test_punctuation_only(self):
        c = treebank_test('!!!')
        self.assertTrue(len(c.keys()) == 1)
        self.assertIsNotNone(c['!'])
        self.assertTrue(c['!']['frequency'] == 3)

    def test_name(self):
        c = treebank_test('Mr. Dan')
        self.assertTrue(len(c.keys()) == 2)
        self.assertIsNotNone(c['mr.'])
        self.assertIsNotNone(c['dan'])

    def test_unicode(self):
        c = treebank_test(u'La Pe\xf1a')
        self.assertTrue(len(c.keys()) == 2)
        self.assertIsNotNone(c['la'])
        self.assertIsNotNone(c[u'pe\xf1a'])

    def multi_frequency(self):
        c = treebank_test('Mr. Dan is good.  Mr. Dan is great.')
        self.assertTrue(len(c.keys()) == 2)
        self.assertTrue(c['mr.']['frequency'] == 2)
        self.assertTrue(c['dan']['frequency'] == 2)

if __name__ == '__main__':
    unittest.main()
