from enigma_tools.crypto_tools.crypto_tools import bigram_count, trigram_count, index_of_coincidence
import json


class StatisticsCli:

    def __init__(self, parser):
        self.parser = parser
        self._add_parser_arguments()

    def process_args(self, args):
        inpt = None
        if args['input_string'] != None:
            inpt = args['input_string']
        elif args['input_file'] != None:
            fpath = args['input_file']
            with open(fpath, 'r') as f:
                inpt = f.read()
        bigrams = None
        bcount = None
        trigrams = None
        tcount = None
        ioc = None
        if args['bigram'] == True:
            bigrams, bcount = bigram_count(inpt)
        if args['trigram'] == True:
            trigrams, tcount = trigram_count(inpt)
        if args['index_of_coincidence'] == True:
            ioc = index_of_coincidence(inpt)
        if args['output_file'] != None:
            fout = args['output_file']
            with open(fout, 'w+') as f:
                if bigrams:
                    f.write(json.dumps(bigrams, indent=4))
                    f.write(bcount)
                if trigrams:
                    f.write(trigrams)
                    f.write(tcount)
                if ioc:
                    f.write(ioc)
        elif bigrams:
            bigrams = [[k,v] for k,v in bigrams.items()]
            bigrams = sorted(bigrams)
            bigrams.sort(key=lambda x : x[1], reverse=True)
            bigram_str = f"Total Count: {bcount}  "
            for bigram in bigrams:
                bigram_str += f"{bigram[0]}-{bigram[1]}  "
            print(bigram_str)
        elif trigrams:
            trigrams = [[k,v] for k,v in trigrams.items()]
            trigrams = sorted(trigrams)
            trigrams.sort(key=lambda x : x[1], reverse=True)
            trigram_str = f"Total Count: {tcount}  "
            for trigram in trigrams:
                trigram_str += f"{trigram[0]}-{trigram[1]}  "
            print(trigram_str)
        elif ioc:
            ioc_str = f"Character Count: {ioc[0]}  IOC {ioc[1]:.3f}  NORMALIZED IOC {ioc[2]:.3f}"
            print(ioc_str)

    def _add_parser_arguments(self):
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument('-s', '--input-string', type=str, help='')
        group.add_argument('-i', '--input-file', type=str, help='')
        group.required = True
        group = self.parser.add_mutually_exclusive_group()
        group.add_argument('-b', '--bigram', action='store_true',  help='')
        group.add_argument('-t', '--trigram', action='store_true', help='')
        group.add_argument('-ioc', '--index_of_coincidence', action='store_true', help='')
        group.required = True
        self.parser.add_argument('-o', '--output-file', type=str, help='')