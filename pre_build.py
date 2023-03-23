import re
import os
import shutil

rxDiacritics = re.compile('[ëç]')
rxDiaPartsStem = re.compile('( stem:)( *[^\r\n]+)')
rxDiaPartsFlex = re.compile('(-flex:)( *[^\r\n]+)')
rxStemVariants = re.compile('[^ |/]+')
rxFlexVariants = re.compile('[^ /]+')
dictDiacritics = {'ë': 'e', 'ç': 'c'}


def collect_lemmata():
    lemmata = ''
    lexrules = ''
    derivations = ''
    for fname in os.listdir('.'):
        if fname.endswith('.txt') and fname.startswith('sqi_lexemes'):
            f = open(fname, 'r', encoding='utf-8-sig')
            lemmata += f.read() + '\n'
            f.close()
        elif fname.endswith('.txt') and fname.startswith('sqi_lexrules'):
            f = open(fname, 'r', encoding='utf-8-sig')
            lexrules += f.read() + '\n'
            f.close()
        elif fname.endswith('.txt') and fname.startswith('sqi_derivations'):
            f = open(fname, 'r', encoding='utf-8-sig')
            derivations += f.read() + '\n'
            f.close()
    lemmataSet = set(re.findall('-lexeme\n(?: [^\r\n]*\n)+', lemmata, flags=re.DOTALL))
    # lemmata = '\n'.join(sorted(list(lemmataSet),
    #                            key=lambda l: (re.search('gramm: *([^\r\n]*)', l).group(1), l)))
    lemmata = '\n'.join(sorted(list(lemmataSet)))
    return lemmata, lexrules, derivations


def collect_paradigms():
    fIn = open('paradigms.txt', 'r', encoding='utf-8-sig')
    text = fIn.read()
    fIn.close()
    return text


def add_diacriticless(morph):
    """
    Add a diacriticless variant to a stem or an inflection
    """
    morph = morph.group(0)
    if rxDiacritics.search(morph) is None:
        return morph
    return morph + '//' + rxDiacritics.sub(lambda m: dictDiacritics[m.group(0)], morph)


def process_diacritics_stem(line):
    """
    Remove diacritics from one line that contains stems.
    """
    morphCorrected = rxStemVariants.sub(add_diacriticless, line.group(2))
    return line.group(1) + morphCorrected


def process_diacritics_flex(line):
    """
    Remove diacritics from one line that contains inflections.
    """
    morphCorrected = rxFlexVariants.sub(add_diacriticless, line.group(2))
    return line.group(1) + morphCorrected


def simplify(text):
    """
    Add diacriticless variants for stems and inflections.
    """
    text = rxDiaPartsStem.sub(process_diacritics_stem, text)
    text = rxDiaPartsFlex.sub(process_diacritics_flex, text)
    return text


def prepare_files():
    """
    Put all the lemmata to lexemes.txt. Put all the lexical
    rules to lexical_rules.txt. Put all the derivations to
    derivations.txt. Create separate versions of
    relevant files for diacriticless texts.
    Put all grammar files to uniparser_albanian/data_strict/
    (original version) or uniparser_albanian/data_nodiacritics/
    (diacriticless version).
    """
    lemmata, lexrules, derivations = collect_lemmata()
    paradigms = collect_paradigms()
    fOutLemmata = open('uniparser_albanian/data_strict/lexemes.txt', 'w', encoding='utf-8')
    fOutLemmata.write(lemmata)
    fOutLemmata.close()
    fOutLemmataNodiacritics = open('uniparser_albanian/data_nodiacritics/lexemes.txt', 'w', encoding='utf-8')
    fOutLemmataNodiacritics.write(simplify(lemmata))
    fOutLemmataNodiacritics.close()
    if len(lexrules) > 0:
        fOutLexrules = open('uniparser_albanian/data_strict/lex_rules.txt', 'w', encoding='utf-8')
        fOutLexrules.write(lexrules)
        fOutLexrules.close()
        fOutLexrules = open('uniparser_albanian/data_nodiacritics/lex_rules.txt', 'w', encoding='utf-8')
        fOutLexrules.write(lexrules)
        fOutLexrules.close()
    fOutParadigms = open('uniparser_albanian/data_strict/paradigms.txt', 'w', encoding='utf-8')
    fOutParadigms.write(paradigms)
    fOutParadigms.close()
    fOutParadigmsNodiacritics = open('uniparser_albanian/data_nodiacritics/paradigms.txt', 'w', encoding='utf-8')
    fOutParadigmsNodiacritics.write(simplify(paradigms))
    fOutParadigmsNodiacritics.close()
    fOutDerivations = open('uniparser_albanian/data_strict/derivations.txt', 'w', encoding='utf-8')
    fOutDerivations.write(derivations)
    fOutDerivations.close()
    fOutDerivations = open('uniparser_albanian/data_nodiacritics/derivations.txt', 'w', encoding='utf-8')
    fOutDerivations.write(derivations)
    fOutDerivations.close()
    if os.path.exists('bad_analyses.txt'):
        shutil.copy2('bad_analyses.txt', 'uniparser_albanian/data_strict/')
        shutil.copy2('bad_analyses.txt', 'uniparser_albanian/data_nodiacritics/')
    if os.path.exists('albanian_disambiguation.cg3'):
        shutil.copy2('albanian_disambiguation.cg3', 'uniparser_albanian/data_strict/')
        shutil.copy2('albanian_disambiguation.cg3', 'uniparser_albanian/data_nodiacritics/')


def parse_wordlists():
    """
    Analyze wordlists/wordlist.csv.
    """
    from uniparser_albanian import AlbanianAnalyzer
    a = AlbanianAnalyzer(mode='strict')
    a.analyze_wordlist(freqListFile='wordlists/wordlist.csv',
                       parsedFile='wordlists/wordlist_analyzed.txt',
                       unparsedFile='wordlists/wordlist_unanalyzed.txt',
                       verbose=True)


if __name__ == '__main__':
    prepare_files()
    parse_wordlists()
