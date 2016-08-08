# Concordance
Fun exercise doing concordance of a big pile of text, comparing multiple concordance methods.

Unfortunately concordance does have one dependency on the regex library.  So there are a few setup options
to get the concordance app running.

Note you can use any text file, data/bible.txt is provided for ease of testing.

#### Setup #1 - You have python 2.7 and you're comfortable with pip installing
```
pip install regex
python main.py data/bible.txt
```

#### Setup #2 - virtual env, in case you're not sure you have python 2.7 available or don't want to mess up your env.
```
venv/bin/python2.7 main.py data/bible.txt
```

#### Runtimes
The bible took:
wordpunct       0:00:02.455445ms 12755 keys
treebank        0:00:26.392973ms 12779 keys

The first chapter of moby dick took:
wordpunct       0:00:00.006795ms 186 keys
treebank        0:00:00.031439ms 184 keys

All of moby dick took:
wordpunct       0:00:01.229898ms 17458 keys
treebank        0:00:09.740102ms 18989 keys

Interesting that moby dick is faster than the bible, though it looks in fact bigger.

#### The difference between Treebank and wordpunct regex
wife's                         { 1: 6562 }  <--- this is a unique word in treebank, it doesn't exist in wordpunct


#### Notes of interest
- ye is said 439 times in moby dick
- ye is said 3839 times in the bible
- wrote is written 62 times, but wrought is written 100 times in moby dick
- wife is written 407 times in the bible but only 24 times in moby dick.  Apparently religion is more interested in marriage than sailors.
