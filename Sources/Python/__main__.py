import interpreter as ip
from kb import KnowledgeBase

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

        if kb.is_constant(query):
            if kb.query_constant(query):
                print("true")
            else:
                print("false")
        else:
            answer = kb.query_ask(query)
            for item in answer:
                print(item)
    
    except Exception as e:
        print("Invalid query: {}".format(e))

# a = ['asdf', '12312']
# b = ['asd', '12312']
# print(a)
# print(b)
# print(str(a == b))