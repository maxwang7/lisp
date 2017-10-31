import re


class Expression(object):
    def __init__(self):
        self.args = []
        self.parent = None

    def addArg(self, expression_or_atom):
        self.args.append(expression_or_atom)

    def setParent(self, parent_expression):
        self.parent = parent_expression

class Atom(object):
    def __init__(self, atom):
        self.atom = atom

class Context(object):
    def _init__(self):
        self.bindings = {}

def parser(raw):
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

def run(ast):
    import pdb; pdb.set_trace()

    bindings = {}
    stack = list(ast.args)

    def valueOf(atom):
        try:
            return int(atom.atom)
        except ValueError:
            try:
                return int(bindings[atom.atom])
            except ValueError:
                return bindings[atom.atom]

    def evaluate(expression):
        # TODO expression may have sub expressions that are already pre-evaluated
        # deal with that
        args = expression.args
        if args[0].atom == 'define':
            bindings[args[1].atom] = args[2].atom
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

input_str = "(define a 1) (define a 2) (define b 2) (+ a b)"
ast = parser(input_str)
run(ast)
