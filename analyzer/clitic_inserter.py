import re
import os


rxPartsGloss = re.compile(' *(?:parts|gloss)="[^"]*"')


def delete_doubles(line):
    m = re.search('^(.*<w>)((<ana.*?/ana>){2,})(.*)$', line, flags=re.DOTALL)
    if m is None:
        return line
    ana = set(re.findall('<ana.*?/ana>', m.group(2)))
    line = m.group(1) + ''.join([x for x in sorted(ana)]) + m.group(4)
    return line
    

for root, dirs, files in os.walk('./'):
    for fname in files:
        if not fname.endswith('wordlist.csv-parsed.txt'):
            continue
        fIn = open(os.path.join(root, fname), 'r', encoding='utf-8-sig')
        fOut = open(os.path.join(root, fname.replace('.txt', '-clitics.txt')),
                    'w', encoding='utf-8')
        for line in fIn:
##            line = re.sub(u'(V\\.2\\.sg\\.imp\\.act)\\.LEX:[^"]*("'
##                          u'.*([^aeiouë]j[aei]|[aeiouë][aei])</w>)',
##                          u'\\1\\2', line)
            line = delete_doubles(line)
            line = rxPartsGloss.sub('', line)
            line = re.sub('(<ana lex="[^"]*" gr="[^"]*),LEX:([^:]+):([^."]+)([^"]*"[^>]*></ana>)',
                          '<ana lex="\\2" gr="CLIT_PRO,\\3"></ana>\\1\\4', line)
            line = re.sub('(gr="[^"]*):', '\\1,', line)
            fOut.write(line)
        fOut.close()
        fIn.close()
        print(fname, ' processed.')

