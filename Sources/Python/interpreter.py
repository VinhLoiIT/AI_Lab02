import pyparsing as pp
import string

class Term:
        
    def apply_bindings(self, bindings):
        return self

class Functor(Term):
    def __init__(self, name, args):
        self.name = name
        self.args = args
        self.arity = len(args)

    def is_fact(self):
        return self._is_constant()

    def clone(self):
        args = list(self.args)
        return Functor(self.name, args)

    def get_var_pos(self):
        for i in range(len(self.args)):
            if isinstance(self.args[i], Variable):
                return True, i
        return False, -1

    def _is_constant(self):
        for arg in self.args:
            if not isinstance(arg, Atom):
                return False
        return True     
    
    def __str__(self):
        return '{}/{}'.format(self.name, self.arity)

    def apply_bindings(self, bindings):
        new_terms = []
        for term in self.args:
            if isinstance(term, Term): 
                new_terms.append(term.apply_bindings(bindings))
            else: 
                new_terms.append(term)
        return Functor(self.name, new_terms)


class Atom(Term):
    def __init__(self, value):
        self.value = value
        self._hash = hash(self.value)

    def __str__(self):
        return str(self.value)
    
    def __repr__(self):
        return str(self)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return isinstance(other, Atom) and self.value == other.value

    def apply_bindings(self, bindings):
        if str(self) in bindings.keys():
            return bindings[self]
        else:
            return self
    
    def clone(self):
        return Atom(self.value)

class Variable(Term):
    def __init__(self, value):
        self.value = value
        self._hash_value = hash(self.value)

    def __hash__(self):
        return self._hash_value    

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return isinstance(other, Variable) and self.value == other.value

    def __repr__(self):
        return str(self)

    def apply_bindings(self, bindings: dict):
        if self in bindings:
            return bindings[self]
        else: 
            return self


class Rule:
    def __init__(self, head: Functor, body: list):
        self.name = head.name
        self.arity = head.arity
        self.head = head
        if body == None:
            self.body = []
        else:
            self.body = body

    def clone(self):
        new_body = []
        for x in self.body:
            if isinstance(x, Term):
                new_body.append(x.clone())
            else:
                new_body.append(x)
        return Rule(self.head.clone(), new_body)

    def __str__(self):
        return '{}/{}'.format(self.name, self.arity)


class Operator(str):
    def __init__(self, value):
        self.value = value
    
    def __str__(self):
        return str(self.value)

    def is_and(self):
        return str(self) == ','

    def is_or(self):
        return str(self) == ';'

def parse_rule_action(tokens):
    return Rule(tokens[0], tokens[1].asList())

def parse_functor_action(tokens):
    return Functor(tokens[0], tokens[2].asList())

pOP = pp.Char(',;')
pOP.setParseAction(lambda tokens: Operator(tokens[0]))

pSPECIAL_CHAR = pp.Char("@+-*/<>=:.&~ ")
pATOM = pp.Word(string.ascii_lowercase, pp.alphanums + "_") ^ pp.sglQuotedString()
#     | [0] ---------------------------------------------------------------------|
pATOM.setParseAction(lambda tokens: Atom(tokens[0]))

pVARIABLE = pp.Word(string.ascii_uppercase + "_", pp.alphanums + "_")
#         | [0] -----------------------------------------------------|
pVARIABLE.setParseAction(lambda tokens: Variable(tokens[0]))

# pNUMBER = pp.Word(pp.nums) + pp.Optional(pp.Char('.') + pp.Word(pp.nums))
# #       | [0] ---------------[1]--------------------------------------|
# pNUMBER.setParseAction(lambda tokens: float(tokens[0] + tokens[1] + tokens[2]) if len(tokens) > 1) else int(tokens[0]))

pFUNCTOR_ARG_TYPE = pATOM ^ pVARIABLE # ^ pFUNCTOR # ^ pNUMBER
pFUNCTOR_ARG_TYPE.setParseAction(lambda tokens: tokens[0])
pFUNCTOR_ARG = pp.Group(pFUNCTOR_ARG_TYPE + pp.ZeroOrMore(pp.Suppress(",") + pFUNCTOR_ARG_TYPE))
pFUNCTOR_ARG.setParseAction(lambda tokens: tokens)
pFUNCTOR = pATOM + "(" + pFUNCTOR_ARG + ")"
pFUNCTOR.setParseAction(parse_functor_action)


pVARARG = pp.Group(pVARIABLE + pp.ZeroOrMore(pp.Suppress(",") + pVARIABLE))
pVARARG.setParseAction(lambda tokens: tokens)
pFUNCTOR_VAR = pATOM + "(" + pVARARG + ")"
pFUNCTOR_VAR.setParseAction(parse_functor_action)

pRULE = pFUNCTOR_VAR + pp.Suppress(":-") + pp.Group(pFUNCTOR_VAR + pp.ZeroOrMore(pOP + pFUNCTOR_VAR))
pRULE.setParseAction(parse_rule_action)

pPARSER = (pRULE ^ pFUNCTOR ^ pATOM) + '.'

def parse(line):
    return pPARSER.parseString(line)[0]

def is_atom(s: str):
    try:
        pATOM.parseString(s)
        return True
    except:
        return False

def is_variable(var: str):
    try:
        pVARIABLE.parseString(var)
        return True
    except:
        return False


def testlib():
    'Ham nay kiem tra xem parse co dung khong bang cach thu mot so truong hop'
    l = [
        "father(Person, Person):-male(X),female(Y),asdf(Z).",
        "father('Mike', 'Monk').",
        "father('Monk', 'Mark').",
        "grandparent(X,Y) :- parent(X, Z), parent(Z, Y).",
        '1231231'
    ]
    for i in range(len(l)):
        try:
            result = parse(l[i])
            print(str(result))
        except Exception:
            print("Cannot parse line " + str(i))

# Uncomment to test interpreter
# testlib()