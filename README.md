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
venv/bin/pyton-2.7 main.py data/bible.txt
```

