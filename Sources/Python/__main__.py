import interpreter as ip
from kb import KnowledgeBase
from algorithm import fol_fc_ask, fol_bc_ask
import argparse as args

def setup(filepath, ask_method):
    kb = KnowledgeBase(ask_method)
    try:
        kb.create(filepath)
    except Exception as e:
        print("Error while creating knowledge base: {}".format(e))
        return kb

    print('Import knowledge base from {} successfully'.format(filepath))
    return kb

def query(kb, sentence):
    try:
        query_ask = ip.parse(sentence)
        answer_generator = kb.ask(kb, query_ask) 
        try:
            while True:
                answer = next(answer_generator)
                if answer is not None:
                    if len(answer.keys()) == 0:
                        print("true.")
                        break
                    else:
                        print(answer)
                        if input('Enter ; to continue: ') != ';':
                            break   
                else:
                    print("false.")
                
        except StopIteration:
            print("false.")
    
    except Exception as e:
        print("Invalid query: {}".format(e))

def console(kb):
    while True:
        sentence = input('prolog> ')
        query(kb, sentence)

if __name__ == '__main__':
    # console('1612348_1612756_Lab02.pl', fol_bc_ask)

    # l = [
    #     "husband(X,'Princess Anna').",
    #     "husband(X,Y).",
    #     "husband('Timothy Laurence','Princess Anna').",
    #     "husband('Timothy Laurence','Princess Anna')."
    # ]
    # for q in l:
    #     query(kb, q)

    argparser = args.ArgumentParser('Prolog Python')
    argparser.add_argument('-f', '--file', help='Knowledge base file path', type=str, dest='filepath')
    argparser.add_argument('-m', '--method', help='Inference method', choices=['fc','bc'], required=True, dest='method')
    args = argparser.parse_args()

    print(args)

    if args.method == 'fc':
        method = fol_fc_ask
    else:
        method = fol_bc_ask

    kb = setup(args.filepath, method)
    console(kb)

