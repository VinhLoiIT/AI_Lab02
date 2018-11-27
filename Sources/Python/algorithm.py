'''Algorithm'''

from interpreter import Variable, Atom, Functor, Term
from kb import KnowledgeBase, KBError

def compose(f, g, composition=None):
  if composition == None: 
      composition = {}

  for key in f.keys():
    if isinstance(f[key], Term):
      composition[key] = f[key].apply_bindings(g)
    elif composition is not f:
      composition[key] = f[key]
  composition.update(g)
  return composition

def unify(term1: Term, term2: Term, bindings = None):
    if bindings is None:
        bindings = dict()
    return _unify(term1, term2, bindings)

def _unify(term1: Term, term2: Term, bindings = {}):
    # base cases
    if term1 == term2:
        return bindings
    # recursive cases
    elif isinstance(term1, Variable):
        return _unify_var(term1, term2, bindings)
    elif isinstance(term2, Variable): 
        return _unify_var(term2, term1, bindings)
    elif isinstance(term1, Functor) and isinstance(term2, Functor):
        P, P_terms = term1.name, term1.args
        F, F_terms = term2.name, term2.args
        if P == F:
            return _unify(P_terms, F_terms, bindings) 
    elif isinstance(term1, list) and isinstance(term2, list) and len(term1) == len(term2):
        new_bindings = _unify(term1[0], term2[0], bindings)
        if new_bindings:
            return _unify(apply_bindings_seq(term1[1:], new_bindings), apply_bindings_seq(term2[1:], new_bindings), new_bindings)
    else:
        return None


def _unify_var(var: Variable, x, bindings: dict):
    if str(var) in bindings.keys():
        return _unify(bindings[var], x, bindings)

    try:
        if x in bindings:
            return _unify(var, bindings[x], bindings)
    except TypeError:
        pass
    return compose(bindings, {var : x}, bindings)  


def apply_bindings_seq(seq, bindings):
    l = []
    for x in seq:
        try:
            l.append(x.apply_bindings(bindings))
        except:
            l.append(x)
    return list(l)

def calc_term(kb, term1, operator, term2):
    if isinstance(term1, Functor):
        term1 = kb.query_constant(term1)
    if isinstance(term2, Functor):
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
            if isinstance(rule_body[i], Functor):
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
            if isinstance(test_rule[i], Functor):
                test_rule[i] = test_rule[i].apply_bindings(current_subst)
                if not kb.is_constant(test_rule[i]):
                    return
        if check_semantic(kb, test_rule):
            l = dict(current_subst)
            result.append(l)
        return
    
    for i in range(index, len(rule_body)):
        if i % 2 == 0: # is functor position
            theta = rule_body[i].apply_bindings(current_subst)
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


def fol_fc_ask(kb: KnowledgeBase, query: Functor):
    'Suy dien tien'
    if str(query) in kb._fact.keys():
        for args in kb._fact[str(query)]:
            theta = unify(args, query.args)
            if theta is not None:
                yield theta
        return None
    kb = kb.clone()

    for rule_name in kb._rules.keys():
        rule = kb._rules[rule_name]

        subst_list = []
        for p in rule.body:
            if isinstance(p, Functor):
                p_subst_list = kb.instantiate(p)
                subst_list.append(p_subst_list)
            else:
                subst_list.append(p)
        
        result = []
        current_subst = {}
        tried_subst = []
        find_match(kb, rule.body, subst_list, tried_subst, current_subst, 0, result)

        for match in result:
            args = [match[x] for x in rule.head.args]
            new_fact = Functor(rule.name, args)
            kb.add_fact(new_fact) # TODO: should not add directly
            theta = unify(new_fact, query)
            if theta is not None:
                yield theta

        if str(rule) == str(query):
            break

    return None


def fol_bc_ask(kb: KnowledgeBase, query: Functor):

    if str(query) in kb._fact.keys():
        for args in kb._fact[str(query)]:
            theta = unify(args, query.args)
            if theta is not None:
                return theta
        return None

    kb = kb.clone()

    bindings = unify(query, kb._rules[str(query)].head)
    for key in list(bindings.keys()):
        if isinstance(bindings[key], Variable):
            del bindings[key]
    if bindings is None:
        bindings = {}

    subst_list = []
    for p in kb._rules[str(query)].body:
        if isinstance(p, Functor):
            p = p.apply_bindings(bindings)
            theta = kb.instantiate(p)
            subst_list.append(theta)
        else:
            subst_list.append(p)

    result = []
    current_subst = bindings
    tried_subst = []
    find_match(kb, kb._rules[str(query)].body, subst_list, tried_subst, current_subst, 0, result)

    for i in range(len(result)):
        x = result[i]
        replace_goal = kb._rules[str(query)].head.apply_bindings(x)
        x = unify(replace_goal, query.apply_bindings(x))
        result[i] = x
        
    if result == []:
        return None
    return result