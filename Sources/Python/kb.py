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
            from algorithm import fol_fc_ask
            return fol_fc_ask(self, q)
        else:
            raise KBError()
                
    def query_ask(self, q: ip.Functor):
        assert not self.is_constant(q)
        return self.instantiate(q)


    def is_constant(self, query):
        return isinstance(query, ip.Atom) or (isinstance(query, ip.Functor) and query.is_fact())

    def instantiate(self, functor: ip.Functor):
        if str(functor) in self._fact.keys():
            self.answer = []
            self.instantiate_fact(functor, dict())
            return self.answer

        elif str(functor) in self._rules.keys():
            from algorithm import fol_fc_ask
            return fol_fc_ask(self, functor)
        else:
            return False

        return False

    def _unify_rule(self, rule: ip.Rule):
        raise NotImplementedError()

    def instantiate_fact(self, functor: ip.Functor, theta):
        assert str(functor) in self._fact.keys()
        
        contain_var, pos = functor.get_var_pos()
        if contain_var:
            for fact in self._fact[str(functor)]:
                var = functor.args[pos]
                new_functor = functor.apply_bindings({var: fact[pos]})
                theta[var] = fact[pos]
                self.instantiate_fact(new_functor, theta)
        else:
            if self.query_constant(functor):
                self.answer.append(dict(theta))

    def and_fact(self, fact1, fact2):
        assert self.is_constant(fact1) and self.is_constant(fact2)
        return self.query_constant(fact1) and self.query_constant(fact2)

    def or_fact(self, fact1, fact2):
        assert self.is_constant(fact1) and self.is_constant(fact2)
        return self.query_constant(fact1) or self.query_constant(fact2)

class KBError(ValueError):
    pass

class SyntaxError(KBError):
    pass