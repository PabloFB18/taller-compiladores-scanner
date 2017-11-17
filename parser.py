import ply.yacc as yacc

# Obtener tokens del scanner
from __builtin__ import raw_input

import nodos
from scanner import tokens
from visitor import Visitor

precedence = (
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULTI', 'DIVI'),
    ('right', 'ID', 'NUM'),
    ('left', 'DPAREN', 'IPAREN')
)


def p_program(p):
    """program : declaration_list"""
    p[0] = nodos.Program(p[1])


def p_declaration_list1(p):
    """declaration_list : declaration_list declaration"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[2], list):
        p[0].extend(p[2])
    else:
        p[0].extend([p[2]])


def p_declaration_list2(p):
    """declaration_list : declaration"""
    p[0] = [p[1]]


def p_declaration1(p):
    """declaration : var_declaration"""
    p[0] = p[1]


def p_declaration2(p):
    """declaration : fun_declaration"""
    p[0] = p[1]


def p_var_declaration1(p):
    """var_declaration : type_specifier ID PUNTOC"""
    p[0] = nodos.VarDeclaration(p[1], p[2])


def p_var_declaration2(p):
    """var_declaration : type_specifier ID ICORCH NUM DCORCH PUNTOC"""
    p[0] = nodos.VarDeclaration(p[1], p[2], p[4])


def p_type_specifier1(p):
    """type_specifier : INT"""
    p[0] = p[1]


def p_type_specifier2(p):
    """type_specifier : VOID"""
    p[0] = p[1]


def p_fun_declaration(p):
    """fun_declaration : type_specifier ID IPAREN params DPAREN compound_stmt"""
    p[0] = nodos.FunDeclaration(p[1], p[2], p[4], p[6])


def p_params1(p):
    """params : param_list"""
    p[0] = p[1]


def p_params2(p):
    """params : VOID"""
    pass


def p_param_list1(p):
    """param_list : param_list COMA param"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[3], list):
        p[0].extend(p[3])
    else:
        p[0].extend([p[3]])


def p_param_list2(p):
    """param_list : param"""
    p[0] = [p[1]]


def p_param1(p):
    """param : type_specifier ID"""
    p[0] = nodos.Param(p[1], p[2], False)


def p_param2(p):
    """param : type_specifier ID ICORCH DCORCH"""
    p[0] = nodos.Param(p[1], p[2], True)


def p_compound_stmt(p):
    """compound_stmt : ILLAVE local_declarations statement_list DLLAVE"""
    p[0] = nodos.CompoundStmt(p[2], p[3])


def p_local_declarations1(p):
    """local_declarations : local_declarations var_declaration"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[2], list):
        p[0].extend(p[2])
    else:
        p[0].extend([p[2]])


def p_local_declarations_empty(p):
    """local_declarations :  empty"""
    pass


def p_statement_list1(p):
    """statement_list : statement_list statement"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[2], list):
        p[0].extend(p[2])
    else:
        p[0].extend([p[2]])


def p_statement_list_empty(p):
    """statement_list : empty"""
    pass


def p_statement1(p):
    """statement : expression_stmt"""
    p[0] = p[1]


def p_statement2(p):
    """statement : compound_stmt"""
    p[0] = p[1]


def p_statement3(p):
    """statement : selection_stmt"""
    p[0] = p[1]


def p_statement4(p):
    """statement : iteration_stmt"""
    p[0] = p[1]


def p_statement5(p):
    """statement : return_stmt"""
    p[0] = p[1]


def p_expression_stmt1(p):
    """expression_stmt : expression PUNTOC"""
    p[0] = p[1]
    # p[0] = nodos.ExpressionStmt(p[1])


def p_expression_stmt2(p):
    """expression_stmt : PUNTOC"""
    pass


def p_selection_stmt1(p):
    """selection_stmt : IF IPAREN expression DPAREN statement"""
    p[0] = nodos.SelectionStmt(p[1], p[3], p[5])


def p_selection_stmt2(p):
    """selection_stmt : IF IPAREN expression DPAREN statement ELSE statement"""
    p[0] = nodos.SelectionStmt(p[1], p[3], p[5], p[6], p[7])


def p_iteration_stmt(p):
    """iteration_stmt :  WHILE IPAREN expression DPAREN statement"""
    p[0] = nodos.IterationStmt(p[1], p[3], p[5])


def p_return_stmt1(p):
    """return_stmt :  RETURN PUNTOC"""
    p[0] = nodos.ReturnStmt(p[1])


def p_return_stmt2(p):
    """return_stmt :  RETURN expression PUNTOC"""
    p[0] = nodos.ReturnStmt(p[1], p[2])


def p_expression1(p):
    """expression :  var ASIGN expression"""
    p[0] = nodos.Expression(p[1], p[2], p[3])


def p_expression2(p):
    """expression :  simple_expression"""
    p[0] = p[1]


def p_var1(p):
    """var :  ID"""
    p[0] = nodos.Var(p[1])


def p_var2(p):
    """var :  ID ICORCH expression DCORCH"""
    p[0] = nodos.Var(p[1], p[3])


def p_simple_expression1(p):
    """simple_expression :  additive_expression relop additive_expression"""
    p[0] = nodos.SimpleExpression(p[1], p[2], p[3])


def p_simple_expression2(p):
    """simple_expression :  additive_expression"""
    p[0] = p[1]


def p_relop1(p):
    """relop : MENORI"""
    p[0] = p[1]


def p_relop2(p):
    """relop : MENOR"""
    p[0] = p[1]


def p_relop3(p):
    """relop : MAYOR"""
    p[0] = p[1]


def p_relop4(p):
    """relop : MAYORI"""
    p[0] = p[1]


def p_relop5(p):
    """relop : IGUAL"""
    p[0] = p[1]


def p_relop6(p):
    """relop : DIST"""
    p[0] = p[1]


def p_additive_expression1(p):
    """additive_expression : additive_expression addop term"""
    p[0] = nodos.AdditiveExpression(p[1], p[2], p[3])


def p_additive_expression2(p):
    """additive_expression : term"""
    p[0] = p[1]


def p_addop1(p):
    """addop : SUMA"""
    p[0] = p[1]


def p_addop2(p):
    """addop : RESTA"""
    p[0] = p[1]


def p_term1(p):
    """term : term mulop factor"""
    p[0] = nodos.Term(p[1], p[2], p[3])


def p_term2(p):
    """term : factor"""
    p[0] = p[1]


def p_mulop1(p):
    """mulop : MULTI"""
    p[0] = p[1]


def p_mulop2(p):
    """mulop : DIVI"""
    p[0] = p[1]


def p_factor1(p):
    """factor : IPAREN expression DPAREN"""
    p[0] = p[1]


def p_factor2(p):
    """factor : var"""
    p[0] = p[1]


def p_factor3(p):
    """factor : call"""
    p[0] = p[1]


def p_factor4(p):
    """factor : NUM"""
    p[0] = nodos.Num(p[1])


def p_call(p):
    """call : ID IPAREN args DPAREN"""
    p[0] = nodos.Call(p[1], p[3])


def p_args1(p):
    """args : arg_list"""
    p[0] = p[1]


def p_args_empty(p):
    """args : empty"""
    pass


def p_arg_list1(p):
    """arg_list : arg_list COMA expression"""
    if isinstance(p[1], list):
        p[0] = p[1]
    else:
        p[0] = [p[1]]

    if isinstance(p[3], list):
        p[0].extend(p[3])
    else:
        p[0].extend([p[3]])


def p_arg_list2(p):
    """arg_list : expression"""
    p[0] = [p[1]]


def p_empty(p):
    """empty :"""
    pass


# Error rule for syntax errors
def p_error(p):
    print ('Syntax error in input!')
    print ('Error en el ' + str(p.type))


# Build the parser
parser = yacc.yacc()

with open('sample.txt', 'r') as arch1:
    contents = arch1.read()
    result = parser.parse(contents)
    visitor = Visitor()
    nodos.Program.accept(result, visitor)
    print(visitor.ast)

# out1 = open('parser-examples/out1.txt', 'w')
# with open('parser-examples/sample1.txt', 'r') as arch1:
#     contents = arch1.read()
#     result = parser.parse(contents)
#     print('\n sample1')
#     visitor = Visitor()
#     nodos.Program.accept(result, visitor)
#     out1.write(visitor.ast)

