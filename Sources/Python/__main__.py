import interpreter as ip
from kb import KnowledgeBase
from algorithm import fol_fc_ask

kb = KnowledgeBase()

filename = '1612348_1612756_Lab02.pl'

try:
    kb.create(filename)
except:
    print("Error while creating knowledge base")

print('Import knowledge base from {} successfully'.format(filename))
while True:
    try:
        query = input("query> ")

        query = ip.parse(query)

        answer_generator = fol_fc_ask(kb, query)
        try:
            while True:
                answer = next(answer_generator)
                if answer is not None:
                    if len(answer) == 1 and answer[0] == {}:
                        print(True)
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
