import re


def xml2conll(fnameIn, fnameOut):
    fIn = open(fnameIn, 'r', encoding='utf-8')
    fOut = open(fnameOut, 'w', encoding='utf-8')
    for line in fIn:
        if len(line) <= 3:
            continue
        mAna = re.search('(<ana.*>)([^<>]+)</w>', line)
        if mAna is None:
            continue
        word = mAna.group(2)
        analyses = mAna.group(1)
        lemmata = set()
        pos = set()
        gramm = set()
        for ana in re.findall('<ana lex="([^"]+)" gr="([^"]+)"', analyses):
            lemmata.add(ana[0])
            pos.add(re.sub(',.*', '', ana[1]))
            gramm.add(re.sub('^[^,]*[A-Z,-]*', '', ana[1]))
        fOut.write(word + '\t' + '|'.join(l for l in sorted(lemmata)) + '\t'
                   + '|'.join(p for p in sorted(pos)) + '\t'
                   + '|'.join(g for g in sorted(gramm)) + '\n')
    fIn.close()
    fOut.close()


if __name__ == '__main__':
    xml2conll('wordlist.csv-parsed.txt', 'analyses_conll.txt')
