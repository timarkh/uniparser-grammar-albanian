uniparser-grammar-albanian
==========================

This is a formalized description of standard Albanian morphology, which also includes a number of dialectal and historical elements. The description is carried out in the UniParser format and involves a description of the inflection (paradigms.txt) and a grammatical dictionary (sqi_lexemes_XXX.txt files). The dictionary contains descriptions of individual lexemes, each of which is accompanied by information about its stem, its part-of-speech tag and some other grammatical information, its inflectional type (paradigm), and English translation.

This description can be used for morphological analysis of Albanian texts in the following ways:

1. The ``wordlists`` directory contains annotated frequency list of tokens based on the Albanian corpus (about 20 million words of contemporary texts), which contains 125,500 unique tokens (case-insensitive). The simplest solution is to use this analyzed wordlist for analyzing your texts. The recall of the analyzer on the corpus texts is about 93% and the corpus is sufficiently large, so if you use the wordlist, the recall on your texts is likely to be around 90% as well. Additionally, this directory includes a list of tokens the analyzer did not recognize.

2. The ``analyzer`` directory contains the UniParser set of scripts together with all necessary language files. You can use it to analyze your own frequency word list. Your have to name your list "wordlist.csv" and put it to that directory. Each line should contain one token and its frequency, tab-delimited. Then you have to run ``finalizer/gramm_finalizer.py`` to collect the data from all source files. This script will create two files, ``lexemes.txt`` and ``paradigms.txt``, which you have to transfer to ``analyzer``. When you run ``analyzer/UniParser/analyze.py``, the analyzer will produce two files, one with analyzed tokens, the other with unanalyzed ones. (You can also use other file names and separators with command line options, see the code of analyze.py.) This way, you will not be restricted by our word list, but the analyzer works pretty slowly (500-1000 tokens per second). After the analysis, you may want to run the ``analyzer/clitic_inserter.py`` script. It will go through the analyzed word list, remove attributes that are irrelevant for Albanian, and reformat analyses which include verbal intraclitics.

3. Finally, you are free to convert/adapt the description to whatever kind of morphological analysis you prefer to use.


