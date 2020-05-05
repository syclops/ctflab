"""
Check that a function only uses certain operators and that it uses less than a
given maximum number of these operators.

Author: Steve Matsumoto <stephanos.matsumoto@sporic.me>
"""
import argparse
from pycparser import c_parser, c_ast
from queue import Queue
import sys


DISALLOWED_OPS = (
    c_ast.Break,
    c_ast.Case,
    c_ast.Continue,
    c_ast.Default,
    c_ast.DoWhile,
    c_ast.For,
    c_ast.FuncCall,
    c_ast.If,
    c_ast.Switch,
    c_ast.TernaryOp,
    c_ast.While,
)
OP_NODES = {
    c_ast.ArrayDecl: lambda x: [x.type, x.dim],
    c_ast.ArrayRef: lambda x: [x.name, x.subscript],
    c_ast.Assignment: lambda x: [x.lvalue, x.rvalue],
    c_ast.BinaryOp: lambda x: [x.left, x.right],
    c_ast.Cast: lambda x: [x.to_type, x.expr],
    c_ast.Compound: lambda x: x.block_items,
    c_ast.CompoundLiteral: lambda x: [x.type, x.init],
    c_ast.Constant: lambda _: [],
    c_ast.Decl: lambda x: [x.type, x.init, x.bitsize],
    c_ast.DeclList: lambda x: x.decls,
    c_ast.EllipsisParam: lambda _: [],
    c_ast.EmptyStatement: lambda _: [],
    c_ast.Enum: lambda x: [x.values],
    c_ast.Enumerator: lambda x: [x.value],
    c_ast.EnumeratorList: lambda x: x.enumerators,
    c_ast.ExprList: lambda x: x.exprs,
    # c_ast.FileAST should not appear in the body of a function.
    c_ast.FuncDecl: lambda x: [x.args, x.type],
    c_ast.FuncDef: lambda x: [x.decl, x.body] + x.param_decls,
    c_ast.Goto: lambda _: [],
    c_ast.ID: lambda _: [],
    c_ast.IdentifierType: lambda _: [],
    c_ast.InitList: lambda x: x.initlist,
    c_ast.Label: lambda x: [x.stmt],
    c_ast.NamedInitializer: lambda x: x.name + [x.expr],
    c_ast.ParamList: lambda x: x.params,
    c_ast.PtrDecl: lambda x: [x.type],
    c_ast.Return: lambda x: [x.expr],
    c_ast.Struct: lambda x: x.decls,
    c_ast.StructRef: lambda x: [x.name, x.field],
    c_ast.TypeDecl: lambda x: [x.type],
    c_ast.Typedef: lambda x: [x.type],
    c_ast.Typename: lambda x: [x.type],
    c_ast.UnaryOp: lambda x: [x.expr],
    c_ast.Union: lambda x: x.decls,
    c_ast.Pragma: lambda _: [],
}


def check_function(function, allowed_ops, max_ops):
    """
    Check that a function meets the allowed operators and maximum operators
    limits.

    Args:
        function: the name of the function to check.
        allowed_ops: a list of strings representing allowed operators.
        max_ops: the maximum number of operators allowed.

    Returns:
        A message explaining why the check fails, or None if it succeeds.
    """
    source_code = sys.stdin.read()
    ast = c_parser.CParser().parse(source_code)
    # Scan the parse tree for the target function definition.
    for declaration in ast.ext:
        if not isinstance(declaration, c_ast.FuncDef):
            continue
        if declaration.decl.name == function:
            # Set up a breadth-first search through the parse tree of the
            # function body.
            queue = Queue()
            for statement in declaration.body.block_items:
                queue.put(statement)
            num_ops = 0
            while not queue.empty():
                statement = queue.get()
                if isinstance(statement, DISALLOWED_OPS):
                    return 'Loops and conditionals are prohibited'
                # Constants and unary/binary operators have additional failure
                # conditions, so check them.
                if isinstance(statement, c_ast.Constant):
                    if statement.type != 'int':
                        return 'Only integer constants allowed'
                    value = int(statement.value, 0)
                    if value < 0 or value > 255:
                        return f'Integer constant {value} out of allowed range'
                elif isinstance(statement, (c_ast.BinaryOp, c_ast.UnaryOp)):
                    if statement.op not in allowed_ops:
                        return f'Using operator {statement.op} is forbidden'
                    num_ops += 1
                    if num_ops > max_ops:
                        return f'Maximum allowed operators ({max_ops}) exceeded'
                # Add relevant child nodes in the parse tree to the queue.
                for child_node in OP_NODES[type(statement)](statement):
                    queue.put(child_node)
    return None


def get_parser(name):
    parser = argparse.ArgumentParser(name)
    parser.add_argument('function',
                        help='name of function to check')
    parser.add_argument('allowed_ops',
                        help='comma-separated list of allowed operations')
    parser.add_argument('max_ops', type=int,
                        help='maximum number of allowed operations')
    return parser


def main(args=sys.argv):
    parser = get_parser(args[0])
    parsed_args = parser.parse_args(args[1:])
    allowed_ops = parsed_args.allowed_ops.split(',')
    error_msg = check_function(parsed_args.function, allowed_ops,
                               parsed_args.max_ops)
    if error_msg is not None:
        print(error_msg, file=sys.stderr)
        sys.exit(1)
    print('Syntax check succeeded', file=sys.stderr)
    sys.exit(0)


if __name__ == '__main__':
    main()
