"""
Usage:
python main.py <filename>

There is some sample data in data/ folder

Test:
python test.py

There is a scattering of tests in there.

These are some resources I read in helping study the problem, many ideas and code were
provided from both:
https://github.com/nltk/nltk
http://nlp.stanford.edu/software/tokenizer.shtml
http://www.cs.utsa.edu/~wagner/python/concord/concord.html
https://github.com/fnl/segtok

I wanted to run two different algorithms, one a relatively simple regex
the other a more complex regex that handles "human language" a bit more naturally.

For instance Mr. Dan doesn't tokenize to < 'Mr', 'Dan', '.' > like it does in regex
it tokenizes to < 'Mr.', 'Dan' > in Treebank.

I thought there may be potential for treebank to be too slow as it requires a sentence segmentation
which requires basically reading the entire buffer from file.  So I wanted to have both algorithms available
so I could judge the speed trade-off vs "better output"

Weaknesses:
1.  Haven't tested codecs at all, if this is beyond utf8 it'll break.  We could pass in
the encoding via an arg.

Runtimes
The bible took:
wordpunct       0:00:02.455445ms 12755 keys
treebank        0:00:26.392973ms 12779 keys

The first chapter of moby dick took:
wordpunct       0:00:00.006795ms 186 keys
treebank        0:00:00.031439ms 184 keys

"""

from __future__ import absolute_import, unicode_literals

import codecs
from concordance import treebank_concordance, wordpunct
import sys


def main():
    # TODO: would normally use argparse
    if len(sys.argv) < 2 or not(sys.argv[1]):
        sys.exit("'usage: python main.py filename', where filename is the text you want to process.")
    try:
        print("\n")
        print("Runtime of Each Algorithm")
        print("-------------------------------")
        with codecs.open(sys.argv[1], 'r', 'utf-8') as fp:
            wordpunct(fp, sys.argv[1], {})

        with codecs.open(sys.argv[1], 'r', 'utf-8') as fp:
            treebank_concordance(fp, sys.argv[1], {})
    except IOError:
        sys.exit("Whoops!  We couldn't find that file.  'usage: python main.py filename', where filename is the text you want to process.")

if __name__ == '__main__':
    main()
