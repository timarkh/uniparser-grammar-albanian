try:
    from importlib.resources import files, as_file
except ImportError:
    from importlib_resources import files, as_file
from uniparser_morph import Analyzer
import re


class AlbanianAnalyzer(Analyzer):
    rxClitProTagXML = re.compile('(<ana lex="[^"]*" gr="[^"]*),LEX:([^:]+):([^,."]+)([^"]*"[^>]*></ana>)')
    rxClitProTagStandalone = re.compile('^LEX:([^:]+):([^,."]+)$')
    rxGrammColon = re.compile('(gr="[^"]*):')

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

    def insert_clitics(self, words, format='xml'):
        """
        Remove LEX:xxx:yyy (intraclitics) tags from the analyses and create
        separate analyses for them. Work recursively if words is a list. Return
        processed words.
        This is an Albanian-specific postprocessing function.
        TODO: Complete and move to uniparser-morph.
        """
        if format not in ('xml', 'json'):
            return words
        if format == 'xml':
            if type(words) == list:
                for i in range(len(words)):
                    words[i] = self.insert_clitics(words[i], format=format)
                return words
            elif type(words) == str:
                words = self.rxClitProTagXML.sub('<ana lex="\\2" gr="CLIT_PRO,\\3"></ana>\\1\\4', words)
                words = self.rxGrammColon.sub('\\1,', words)
                return words
        elif format == 'json':
            if type(words) != list or len(words) <= 0:
                return words
            if any(type(w) != dict for w in words):
                for i in range(len(words)):
                    words[i] = self.insert_clitics(words[i], format=format)
                return words
            cliticAnalyses = []
            for ana in words:
                if 'gramm' not in ana:
                    continue
                for tag in ana['gramm']:
                    m = self.rxClitProTagStandalone.search(tag)
                    if m is not None:
                        newAna = {
                            'lemma': m.group(1),
                            'gramm': ['CLIT_PRO'] + m.group(2).split(',')
                        }
                        cliticAnalyses.append(newAna)
                ana['gramm'] = [tag for tag in ana['gramm']
                                if self.rxClitProTagStandalone.search(tag) is None]
                ana['gramm'] += cliticAnalyses
            return words
        return words

    def analyze_words(self, words, format=None): #, disambiguate=False):
        """
        Analyze a single word or a (possibly nested) list of words. Return either a list of
        analyses (all possible analyses of the word) or a nested list of lists
        of analyses with the same depth as the original list.
        If format is None, the analyses are Wordform objects.
        If format == 'xml', the analyses for each word are united into an XML string.
        If format == 'json', the analyses are JSON objects (dictionaries).
        Perform CG3 disambiguation if disambiguate == True and CG3 is installed.
        """
        # if disambiguate:
        #     with as_file(files(self.dirName) / 'albanian_disambiguation.cg3') as cgFile:
        #         cgFilePath = str(cgFile)
        #         return super().analyze_words(words, format=format, disambiguate=True,
        #                                      cgFile=cgFilePath)
        return super().analyze_words(words, format=format, disambiguate=False)


if __name__ == '__main__':
    a = AlbanianAnalyzer()
    analyses = a.analyze_words('ndodhi')
    for ana in analyses:
        print(ana.wf, ana.lemma, ana.gramm, ana.gloss)
    analyses = a.analyze_words('ndodhi', format='xml')
    print(analyses)
    analyses = a.analyze_words('ndodhi', format='json')
    for ana in analyses:
        print(ana)

