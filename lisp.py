import re

class Expression(object):
    def __init__(self, parent = None):
        self.parent = parent

    def run(self, context):
        pass

class List(Expression):
    def __init__(self):
        super(List, self).__init__()
        self.args = []

class Atom(Expression):
    def __init__(self, value = None):
        super(Atom, self).__init__()
        self.value = value

class Integer(Atom):
    def __init__(self, value = None):
        super(Integer, self).__init__()
        self.value = value

class Symbol(Atom):
    def __init__(self, value = None):
        super(Symbol, self).__init__()
        self.value = value

class Context(object):
    def __init__(self):
        self.symbols = {}

class Program(object):
    def __init__(self):
        self.asts = []
        self.cur_pos = 0 # the expression that's about to be run
        self.context = Context()

    def step(self):
        return self.asts[self.cur_pos].run(self.context)

    def hasFinished(self):
        return self.cur_pos >= len(self.asts)

def parse(raw):
    program = Program()

    cur_list = None
    atom_so_far = ""

    def isInteger(atom):
        try:
            int(atom)
            return True
        except ValueError:
            return False

    for ch in raw:
        should_end_atom = (ch in ["(", ")", " "])
        if should_end_atom and atom_so_far != "":
            new_atom = None
            if isInteger(atom_so_far):
                new_atom = Integer(value = int(atom_so_far))
            else:
                new_atom = Symbol(value = atom_so_far)

            if cur_list:
                cur_list.args.append(new_atom)
            else:
                program.asts.append(new_atom)

            atom_so_far = ""

        if ch == "(":
            new_list = List()
            if cur_list:
                cur_list.args.append(new_list)
                new_list.parent = cur_list
            else:
                program.asts.append(new_list)
            cur_list = new_list
        elif ch == ")":
            import pdb; pdb.set_trace()
            cur_list = cur_list.parent
        elif ch != " " and ch != "\n" and ch != "\t":
            atom_so_far += ch
    return program
    """
    result = Expression()
    cur_expression = result
    cur_atom = ""

    for ch in raw:
        should_end_atom = (ch in ["(", ")", " "])

        if should_end_atom and cur_atom != "":
            cur_expression.addArg(Atom(cur_atom))
            cur_atom = ""

        if ch == "(":
            new_expression = Expression()
            cur_expression.addArg(new_expression)
            new_expression.setParent(cur_expression)
            cur_expression = new_expression
        elif ch == ")":
            cur_expression = cur_expression.parent
        elif ch != " ":
            cur_atom += ch

    return result
"""

def run(program):
    import pdb; pdb.set_trace()

    bindings = {}
    stack = list(ast.args)

    def valueOfAtom(atom):
        try:
            return int(atom.atom)
        except ValueError:
            try:
                return int(bindings[atom.atom])
            except ValueError:
                return bindings[atom.atom]

    def valueOf(expression_or_atom):
        if type(expression_or_atom) == Expression:
            return expression_or_atom.val
        elif type(expression_or_atom) == Atom:
            return valueOfAtom(expression_or_atom)
        else:
            print "invalid"

    def evaluate(expression):
        # TODO expression may have sub expressions that are already pre-evaluated
        # deal with that
        args = expression.args
        if args[0].atom == 'define':
            bindings[valueOf(args[1].atom)] = valueOf(args[2].atom)
            return
        elif args[0].atom == '+':
            return valueOf(args[1]) + valueOf(args[2])
        else:
            print "unknown function: '{}'".format(expression.args[0].atom)

    while len(stack) > 0:
        head = stack.pop(0)
        if type(head) == Expression:
            has_sub_expression = False
            for arg in head.args:
                if type(arg) == Expression and not arg.val:
                    stack.insert(0, head)
                    stack.insert(0, arg)
                    has_sub_expression = True
                    break
            if has_sub_expression:
                continue
            val = evaluate(head)
            print "{}: {}".format(head, val)
            head.val = val
        elif type(head) == Atom:
            print "it's an atom!"
    import pdb; pdb.set_trace()

if __name__ == "__main__":
    input_str = "(define a 1) (define a 2) (+ (+ a b) 1)" # => 4
    program = parse(input_str)
    run(program)
