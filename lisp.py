import sys

class Expression(object):
    def __init__(self, parent = None):
        self.parent = parent

    def run(self, context):
        pass

class Atom(Expression):
    def __init__(self, value = None):
        super(Atom, self).__init__()
        self.value = value

class Integer(Atom):
    def __init__(self, value = None):
        super(Integer, self).__init__()
        self.value = value

    def run(self, context):
        return self.value

class Symbol(Atom):
    def __init__(self, value = None):
        super(Symbol, self).__init__()
        self.value = value

    def run(self, context):
        return context.symbols[self.value].run(context)

class List(Expression):
    def __init__(self):
        super(List, self).__init__()
        self.args = []

    def run(self, context):
        if type(self.args[0]) == List:
            # assume that if the first element in a list is also a list that
            # we are seeing a lambda. Unclear if this always holds true,
            # would require further testing
            lambda_params = self.args[0].args[1].args
            lambda_fn = self.args[0].args[2]
            lambda_args = self.args[1:]
            program = Program()
            program.context.symbols = dict(context.symbols)
            for param, val in zip(lambda_params, lambda_args):
                program.context.symbols[param.value] = val
            program.asts.append(lambda_fn)
            result = program.step()
            return result
        elif self.args[0].value == "define":
            context.symbols[self.args[1].value] = self.args[2]
        elif self.args[0].value == "eq?":
            return self.args[1].run(context) == self.args[2].run(context)
        elif self.args[0].value == "atom?":
            arg_type = type(self.args[1])
            return (arg_type in [Atom, Integer, Symbol])
        elif self.args[0].value == "+":
            return self.args[1].run(context) + self.args[2].run(context)
        elif self.args[0].value == "-":
            return self.args[1].run(context) - self.args[2].run(context)
        elif self.args[0].value == "*":
            return self.args[1].run(context) * self.args[2].run(context)
        elif self.args[0].value == "/":
            return self.args[1].run(context) / self.args[2].run(context)
        elif self.args[0].value in context.symbols:
            temp_list = List()
            temp_list.args.append(
                context.symbols[self.args[0].value])
            temp_list.args.extend(self.args[1:])
            return temp_list.run(context)
        else:
            import pdb; pdb.set_trace()
            print "unknown form"

class Context(object):
    def __init__(self):
        self.symbols = {}

class Program(object):
    def __init__(self):
        self.asts = []
        self.cur_pos = 0 # the expression that's about to be run
        self.context = Context()

    def step(self):
        result = self.asts[self.cur_pos].run(self.context)
        self.cur_pos += 1
        return result

    def hasFinished(self):
        return self.cur_pos >= len(self.asts)

    def parse(self, raw):
        program = self

        cur_list = None
        atom_so_far = ""

        def isInteger(atom):
            try:
                int(atom)
                return True
            except ValueError:
                return False

        for ch in (raw + " "):
            should_end_atom = (ch in ["(", ")", " ", "\t", "\n"])
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
                cur_list = cur_list.parent
            elif ch != " " and ch != "\n" and ch != "\t":
                atom_so_far += ch
        return program

def run(program):
    while not program.hasFinished():
        result = program.step()
        if result != None:
            print result

if __name__ == "__main__":
    if len(sys.argv) == 1:
        program = Program()
        try:
            while True:
                line = raw_input("> ")
                program.parse(line)
                run(program)
        except EOFError:
            pass
    elif len(sys.argv) >= 2 and sys.argv[1] == 'test':
        program = Program()
        def check(input_string, expected):
            program.parse(input_string)
            result = str(program.step())
            if result == expected:
                print "PASS: {}: {}".format(input_string, expected)
            else:
                print "FAIL: input: {}, expected: {}, but got: {}".format(input_string, expected, result)

        check("5", "5")
        check("(+ 1 1)", "2")
        check("(define a 1)", "None")
        check("(+ a 1)", "2")
        check("(+ (- 1 2) (* 1 1))", "0")
        check("(eq? -1 (- 0 1))", "True")
        check("((lambda (x) x) 5)", "5")
        check("((lambda (x y) (* x y)) 5 6)", "30")
        check("(define a 5)", "None")
        check("((lambda (x y) (* x y)) a 6)", "30")
        check("(define square (lambda (x) (* x x)))", "None")
        check("(square 5)", "25")
