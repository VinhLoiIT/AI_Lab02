import interpreter as ip

class KnowledgeBase(object):

    def __init__(self):
        self._fact = {}
        self._rules = {}

    def create(self, filepath):
        f = open(filepath, 'r')
        for line in f.readlines():
            line = line.strip()

            if line.startswith('%') or len(line) == 0:
                # TODO: ^: only support comment is first char of line
                continue

            result = ip.parse(line)

            if isinstance(result, ip.Rule):
                self.add_rule(result)
            elif isinstance(result, ip.Functor):
                if result.is_fact():
                    self.add_fact(result)
                else:
                    raise SyntaxError('Fact cannot contain variable')
            elif isinstance(result, ip.Atom):
                self.add_fact(result)
            else:
                raise KBError("Unknow parsed")

    def clone(self):
        kb = KnowledgeBase()
        for key in self._fact.keys():
            kb._fact[key] = [list(x) for x in self._fact[key]]
        for key in self._rules.keys():
            kb.add_rule(self._rules[key].clone())
        return kb

    def add_fact(self, fact):
        if isinstance(fact, ip.Atom):
            self._fact[str(fact)] = True
        elif isinstance(fact, ip.Functor):
            if str(fact) not in self._fact.keys():
                self._fact[str(fact)] = [fact.args]
            else:
                self._fact[str(fact)].append(fact.args)
        else:
            raise KBError("Invalid fact")

    def add_rule(self, rule: ip.Rule):
        self._rules[str(rule)] = rule

    def query_constant(self, q):
        assert self.is_constant(q)
        if str(q) in self._fact.keys():
            if isinstance(q, ip.Functor):
                for args in self._fact[str(q)]:
                    if args == q.args:
                        return True
                return False
            else:
                return True
        elif str(q) in self._rules.keys():
            return forward_chaining(self, q)
        else:
            raise KBError()
                
    def query_ask(self, q: ip.Functor):
        assert not self.is_constant(q)
        return self._unify(q)

    def is_constant(self, query):
        return isinstance(query, ip.Atom) or (isinstance(query, ip.Functor) and query.is_fact())

    def _unify(self, functor: ip.Functor):
        if str(functor) in self._fact.keys():
            self.answer = []
            self._unify_fact(functor, dict())
            return self.answer

        elif str(functor) in self._rules.keys():
            self.answer = []
            # self._unify_rule(functor)
            answer = forward_chaining(self, functor)
            return self.answer

        else:
            return False

        return False

    def _unify_rule(self, rule: ip.Rule):
        raise NotImplementedError()

    def _unify_fact(self, functor: ip.Functor, theta):
        contain_var, pos = functor.get_var_pos()
        if contain_var:
            for fact in self._fact[str(functor)]:
                args = functor.args.copy()
                args[pos] = fact[pos]
                newfunctor = ip.Functor(functor.name, args)

                theta[functor.args[pos]] = fact[pos]
                
                self._unify_fact(newfunctor, theta)
        else:
            if self.query_constant(functor):
                self.answer.append(dict(theta))
        
    def subst(self, functor: ip.Functor, args: dict):
        functor = functor.clone()
        for i in range(len(functor.args)):
            if functor.args[i] in args.keys():
                functor.args[i] = args[functor.args[i]]
        return functor

    def and_fact(self, fact1, fact2):
        assert self.is_constant(fact1) and self.is_constant(fact2)
        return self.query_constant(fact1) and self.query_constant(fact2)

    def or_fact(self, fact1, fact2):
        assert self.is_constant(fact1) and self.is_constant(fact2)
        return self.query_constant(fact1) or self.query_constant(fact2)


    # def _unify_fact_kb(self, fact: ip.Functor):
    #     pass


class KBError(ValueError):
    pass

class SyntaxError(KBError):
    pass

def calc_term(kb, term1, operator, term2):
    if isinstance(term1, ip.Functor):
        term1 = kb.query_constant(term1)
    if isinstance(term2, ip.Functor):
        term2 = kb.query_constant(term2)

    if operator == ',':
        result = term1 and term2
    elif operator == ';':
        result = term1 or term2
    else:
        raise KBError("ERRORRRRRRRRRR")
        result = True # TODO: support NOT operator
    return result

def check_semantic(kb, rule_body):
    if len(rule_body) > 1:
        
        stack_term = []
        stack_operator = []
        for i in range(len(rule_body)):
            if isinstance(rule_body[i], ip.Functor):
                stack_term.append(rule_body[i])
            else:
                if len(stack_operator) == 0:
                    stack_operator.append(rule_body[i])
                    continue
                else:
                    # TODO: currently AND, OR operator support
                    term1 = stack_term[len(stack_term) - 1]
                    stack_term.pop()
                    term2 = stack_term[len(stack_term) - 1]
                    stack_term.pop()
                    operator = stack_operator[len(stack_operator) - 1]
                    stack_operator.pop()

                    # TODO: only work with AND and OR operator
                    stack_term.append(calc_term(kb, term1, operator, term2))
                    stack_operator.append(rule_body[i])

        # TODO: currently AND, OR operator support
        term1 = stack_term[len(stack_term) - 1]
        stack_term.pop()
        term2 = stack_term[len(stack_term) - 1]
        stack_term.pop()
        operator = stack_operator[len(stack_operator) - 1]
        stack_operator.pop()
        return calc_term(kb,term1, operator, term2)
    else:
        return kb.query_constant(rule_body[0])

def find_match(kb:KnowledgeBase, rule_body, subst_list: list, tried_subst:list, current_subst: dict, index, result):
    'Tim cac phep the co the thoa man rule_body (su dung de quy) va tra ve result'
    # result = []
    # current_subst = {}

    if index >= len(rule_body):
        # if tried
        for tried in tried_subst:
            if current_subst == tried:
                return
        tried_subst.append(current_subst)

        test_rule = list(rule_body)
        for i in range(len(test_rule)):
            if isinstance(test_rule[i], ip.Functor):
                test_rule[i] = kb.subst(test_rule[i], current_subst)
                if not kb.is_constant(test_rule[i]):
                    return
        if check_semantic(kb, test_rule):
            l = dict(current_subst)
            result.append(l)
        return
    
    for i in range(index, len(rule_body)):
        if i % 2 == 0: # is functor position
            theta = kb.subst(rule_body[i], current_subst)
            if kb.is_constant(theta):
                if kb.query_constant(theta):
                    find_match(kb, rule_body, subst_list, tried_subst, current_subst, index + 2, result)
                return
            else:
                for subst in subst_list[i]:
                    save_current_subst = dict(current_subst)
                    for key in subst.keys():
                        if key not in current_subst.keys():
                            current_subst[key] = subst[key]
                    find_match(kb, rule_body, subst_list, tried_subst, current_subst, index + 2, result)
                    current_subst = save_current_subst

def forward_chaining(kb:KnowledgeBase, query):
    assert kb.is_constant(query)
    kb = kb.clone()
    for rule_name in kb._rules.keys():
        rule = kb._rules[rule_name]

        subst_list = []
        for p in rule.body:
            if isinstance(p, ip.Functor):
                p_subst_list = kb.query_ask(p)
                # for i in range(len(p_subst_list)):
                #     p_subst_list[i] = kb.subst(p, p_subst_list[i])

                subst_list.append(p_subst_list)
            else:
                subst_list.append(p)

        result = []
        current_subst = {}
        tried_subst = []
        find_match(kb, rule.body, subst_list, tried_subst, current_subst, 0, result)
    
        for match in result:
            args = [match[x] for x in rule.head.args]
            new_fact = ip.Functor(rule.name, args)
            kb.add_fact(new_fact)
            if kb.is_constant(query):
                flag = kb.query_constant(query)
                if flag:
                    return True
        return False

                
# test forward_chaning
# kb = KnowledgeBase()
# filename = '1612348_1612756_Lab02.pl'

# try:
#     kb.create(filename)
# except:
#     print("Error while creating knowledge base")

# print('Import knowledge base from {} successfully'.format(filename))