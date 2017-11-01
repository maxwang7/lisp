# Design

Try it out! `python lisp.py`

Supports:
- `eq?`
- `atom?`
- `define`
- `lambda`
- `cond`

And has the built-ins: `+`, `-`, `*`, `/`

On the roadmap...
- `quote`
- `cons`, `car`, `cdr`
- `cond`
- And better overall testing...


There are two parts
- parser - implemented in `parse()`. This function takes a raw Lisp
string input and builds an abstract syntax tree (AST).
- execution - implemented in `run()`. This function takes in an AST
and executes the expressions.

Class design:

Context - contains symbol bindings and, in the future, lambdas.

Program - contains a list of ASTs and an index of the current execution position
- `asts`
- `current_pos`

Expression
- properties:
  - `parent`
  - `run(context)` - abstract method, returns an updated Context object
- subclasses:
  - List
      - properties:
        - `args` - a list
  - Atom
    - properties:
    - Integer
      - `val` - an integer value
    - Symbol
      - `symbol` - the symbol string

For example, the string 
`"(define a 1) (define b 2) (+ (+ a b) 1)"`
should produce the following program.asts (`parent` and functions omitted):

[
  List(
    Symbol("define")
    Symbol("a")
    Number(1)),
  List(
    Symbol("define")
    Symbol("b")
    Number(2)),
  List(
    Symbol("+"),
    List(
      Symbol("+"),
      Symbol("a"),
      Symbol("b")),
    Number(1))
]
