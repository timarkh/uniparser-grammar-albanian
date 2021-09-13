# Albanian morphological analyzer

This is a rule-based morphological analyzer for Albanian (``sqi``). It is based on a formalized description of literary Albanian morphology, which also includes a number of dialectal (Gheg) elements, and uses [uniparser-morph](https://github.com/timarkh/uniparser-morph) for parsing. It performs full morphological analysis of Albanian words (lemmatization, POS tagging, grammatical tagging).

## How to use
### Python package
The analyzer is available as a Python package. If you want to analyze Albanian texts in Python, install the module:

```
pip3 install uniparser-albanian
```

Import the module and create an instance of ``AlbanianAnalyzer`` class. Set ``mode='strict'`` if you are going to process text in standard orthography, or ``mode='nodiacritics'`` if you expect some words to lack the diacritics (*c* instead of *ç* and *e* instead of *ë*). After that, you can either parse tokens or lists of tokens with ``analyze_words()``, or parse a frequency list with ``analyze_wordlist()``. Here is a simple example:

```python
from uniparser_albanian import AlbanianAnalyzer
a = AlbanianAnalyzer(mode='strict')

analyses = a.analyze_words('Morfologjinë')
# The parser is initialized before first use, so expect
# some delay here (usually several seconds)

# You will get a list of Wordform objects
# The analysis attributes are stored in its properties
# as string values, e.g.:
for ana in analyses:
        print(ana.wf, ana.lemma, ana.gramm)

# You can also pass lists (even nested lists) and specify
# output format ('xml', 'json' or 'conll')
# If you pass a list, you will get a list of analyses
# with the same structure
analyses = a.analyze_words([['i'], ['Të', 'dua', '.']],
	                       format='xml')
analyses = a.analyze_words([['i'], ['Të', 'dua', '.']],
	                       format='conll')
analyses = a.analyze_words(['Morfologjinë', [['i'], ['Të', 'dua', '.']]],
	                       format='json')
```

Refer to the [uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/) for the full list of options.

<!---
### Disambiguation
Apart from the analyzer, this repository contains a set of [Constraint Grammar](https://visl.sdu.dk/constraint_grammar.html) rules that can be used for partial disambiguation of analyzed Albanian texts. If you want to use them, set ``disambiguation=True`` when calling ``analyze_words``:

```python
analyses = a.analyze_words(['Të', 'dua'], disambiguate=True)
```

In order for this to work, you have to install the ``cg3`` executable separately. On Ubuntu/Debian, you can use ``apt-get``:

```
sudo apt-get install cg3
```

On Windows, download the binary and add the path to the ``PATH`` environment variable. See [the documentation](https://visl.sdu.dk/cg3/single/#installation) for other options.

Note that each time you call ``analyze_words()`` with ``disambiguate=True``, the CG grammar is loaded and compiled from scratch, which makes the analysis even slower. If you are analyzing a large text, it would make sense to pass the entire text contents in a single function call rather than do it sentence-by-sentence, for optimal performance.
-->

### Word lists
Alternatively, you can use a preprocessed word list. The ``wordlists`` directory contains a list of words from a 31-million-word [Albanian corpus](http://albanian.web-corpora.net/) (``wordlist.csv``) with 456,000 unique tokens, list of analyzed tokens (``wordlist_analyzed.txt``; each line contains all possible analyses for one word in an XML format), and list of tokens the parser could not analyze (``wordlist_unanalyzed.txt``). The recall of the analyzer on the corpus texts is about 93% and the corpus is sufficiently large, so if you just use the analyzed word list, the recall on your texts will probably exceed 90%.

## Description format
The description is carried out in the ``uniparser-morph`` format and involves a description of the inflection (paradigms.txt), a grammatical dictionary (sqi_lexemes_XXX.txt files), a list of productive lemma-changing derivations (derivations.txt), and a short list of analyses that should be avoided (bad_analyses.txt). The dictionary contains descriptions of individual lexemes, each of which is accompanied by information about its stem, its part-of-speech tag and some other grammatical/dialectal information, its inflectional type (paradigm), and English translation. See more about the format [in the uniparser-morph documentation](https://uniparser-morph.readthedocs.io/en/latest/format.html).
