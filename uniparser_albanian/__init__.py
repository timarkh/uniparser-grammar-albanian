try:
    from importlib.resources import files, as_file
except ImportError:
    from importlib_resources import files, as_file
from uniparser_morph import Analyzer
import re


class AlbanianAnalyzer(Analyzer):
    def __init__(self, mode='strict', verbose_grammar=False):
        """
        Initialize the analyzer by reading the grammar files.
        If mode=='strict' (default), load the data as is.
        If mode=='nodiacritics', load the data for (possibly) diacriticless texts.
        """
        super().__init__(verbose_grammar=verbose_grammar)
        self.mode = mode
        if mode not in ('strict', 'nodiacritics'):
            return
        self.glossing = False
        self.dirName = 'uniparser_albanian.data_' + mode
        with as_file(files(self.dirName) / 'paradigms.txt') as self.paradigmFile,\
             as_file(files(self.dirName) / 'lexemes.txt') as self.lexFile,\
             as_file(files(self.dirName) / 'lex_rules.txt') as self.lexRulesFile,\
             as_file(files(self.dirName) / 'derivations.txt') as self.derivFile,\
             as_file(files(self.dirName) / 'stem_conversions.txt') as self.conversionFile,\
             as_file(files(self.dirName) / 'clitics.txt') as self.cliticFile,\
             as_file(files(self.dirName) / 'bad_analyses.txt') as self.delAnaFile:
            self.load_grammar()
        self.initialize_parser()
        self.m.MIN_REPLACEMENT_WORD_LEN = 9
        self.m.MIN_REPLACEMENT_STEM_LEN = 7

    def analyze_words(self, words, format=None, disambiguate=False, replacementsAllowed=0):
        """
        Analyze a single word or a (possibly nested) list of words. Return either a list of
        analyses (all possible analyses of the word) or a nested list of lists
        of analyses with the same depth as the original list.
        If format is None, the analyses are Wordform objects.
        If format == 'xml', the analyses for each word are united into an XML string.
        If format == 'json', the analyses are JSON objects (dictionaries).
        Perform CG3 disambiguation if disambiguate == True and CG3 is installed.
        """
        if disambiguate:
            with as_file(files(self.dirName) / 'albanian_disambiguation.cg3') as cgFile:
                cgFilePath = str(cgFile)
                return super().analyze_words(words, format=format, disambiguate=True,
                                             cgFile=cgFilePath, replacementsAllowed=replacementsAllowed)
        return super().analyze_words(words, format=format, disambiguate=False, replacementsAllowed=replacementsAllowed)


if __name__ == '__main__':
    a = AlbanianAnalyzer()
    # Check clitics
    analyses = a.analyze_words('ndodhi')
    for ana in analyses:
        print(ana.wf, ana.lemma, ana.gramm, ana.gloss)
    analyses = a.analyze_words('ndodhi', format='xml')
    print(analyses)
    analyses = a.analyze_words('ndodhi', format='json')
    for ana in analyses:
        print(ana)

    # Check sentences
    analyses = a.analyze_words([['i'], ['Të', 'dua', '.']],
                               format='xml')
    for ana in analyses:
        print(ana)
    analyses = a.analyze_words([['i'], ['Të', 'dua', '.']],
                               format='conll', disambiguate=False)
    print(analyses)
    analyses = a.analyze_words(['Morfologjinë', [['i'], ['Të', 'dua', '.']]],
                               format='conll', disambiguate=True)
    print(analyses)
