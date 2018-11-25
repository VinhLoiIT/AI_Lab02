import interpreter as ip

class KnowledgeBase(object):

    def __init__(self):
        self._fact = {}
        self._rules = []
        self._unify_temp = {}

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

    def add_fact(self, fact): # or atom
        if isinstance(fact, ip.Atom):
            self._fact[str(fact)] = True
        elif isinstance(fact, ip.Functor):
            if str(fact) not in self._fact.keys():
                self._fact[str(fact)] = [fact.args]
            else:
                self._fact[str(fact)].append(fact.args)
        else:
            raise KBError("Invalid fact")

    def add_rule(self, rule):
        self._rules.append(rule)

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

        # TODO: unify rule

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
        


    # def _unify_fact_kb(self, fact: ip.Functor):
    #     pass


class KBError(ValueError):
    pass

class SyntaxError(KBError):
    pass


