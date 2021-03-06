from tabla_simbolos.nodo_funcion import NodoFuncion
from tabla_simbolos.nodo_tabla_simbolos import NodoTablaSimbolos
from tabla_simbolos.nodo_variable import NodoVariable


class Nodo():
    pass


# class Null(Nodo):
#     def __init__(self):
#         self.type = 'empty'


class Program(Nodo):
    def __init__(self, declarations_p):
        self.declarations_p = declarations_p
        self.simbolos = NodoTablaSimbolos()

    def accept(self, visitor):
        visitor.visit_program(self)


class VarDeclaration(Nodo):
    def __init__(self, type_specifier_t, id_t, num_t=None):
        self.type_specifier_t = type_specifier_t
        self.id_t = id_t
        self.numero_si_no = False
        self.tipo = None
        self.variable = None

        if num_t is not None:
            self.num_t = num_t
            self.numero_si_no = True

    def accept(self, visitor):
        visitor.visit_var_declaration(self)


class FunDeclaration(Nodo):
    def __init__(self, type_specifier_t, id_t, params_p, compound_stmt_p):
        self.type_specifier_t = type_specifier_t
        self.id_t = id_t
        self.params_p = params_p
        self.compound_stmt_p = compound_stmt_p
        self.simbolos = NodoTablaSimbolos()
        self.funcion = None
        self.tipo = None

    def accept(self, visitor):
        visitor.visit_fun_declaration(self)


class Param(Nodo):
    def __init__(self, type_specifier_t, id_t, arreglo_si_no):
        self.type_specifier_t = type_specifier_t
        self.id_t = id_t
        self.arreglo_si_no = arreglo_si_no
        self.tipo = None
        self.variable = None

    def accept(self, visitor):
        visitor.visit_param(self)


class CompoundStmt(Nodo):
    def __init__(self, local_declarations_p, stmt_list_p):
        self.local_declarations_p = local_declarations_p
        self.stmt_list_p = stmt_list_p
        self.simbolos = NodoTablaSimbolos()

    def accept(self, visitor):
        visitor.visit_compound_stmt(self)


# class ExpressionStmt(Nodo):
#     def __init__(self, expresion_p):
#         self.expresion_p = expresion_p
#
#     def accept(self, visitor):
#         visitor.visit_expression_stmt(self)


class SelectionStmt(Nodo):
    def __init__(self, if_t, expression_p, stmt_p, else_t=None, stmt2_p=None):
        self.if_t = if_t
        self.expression_p = expression_p
        self.stmt_p = stmt_p
        self.else_si_no = False
        self.simbolos_if = NodoTablaSimbolos()

        if else_t is not None:
            self.else_t = else_t
            self.stmt2_p = stmt2_p
            self.else_si_no = True
            self.simbolos_else = NodoTablaSimbolos()

    def accept(self, visitor):
        visitor.visit_selection_stmt(self)


class IterationStmt(Nodo):
    def __init__(self, while_t, expression_p, stmt_p):
        self.while_t = while_t
        self.expression_p = expression_p
        self.stmt_p = stmt_p
        self.simbolos_else = NodoTablaSimbolos()

    def accept(self, visitor):
        visitor.visit_iteration_stmt(self)


class ReturnStmt(Nodo):
    def __init__(self, return_t, expression_p=None):
        self.return_t = return_t
        self.expression_si_no = False
        self.tipo = None

        if expression_p is not None:
            self.expression_p = expression_p
            self.expression_si_no = True

    def accept(self, visitor):
        visitor.visit_return_stmt(self)


class Expression(Nodo):
    def __init__(self, var_p, asign_t, expression_p):
        self.var_p = var_p
        self.asign_t = asign_t
        self.expression_p = expression_p
        self.tipo = None

    def accept(self, visitor):
        visitor.visit_expression(self)


class Var(Nodo):
    def __init__(self, id_t, expression_p=None):
        self.id_t = id_t
        self.expression_si_no = False
        self.tipo = None
        self.variable = None

        if expression_p is not None:
            self.expression_p = expression_p
            self.expression_si_no = True

    def accept(self, visitor):
        visitor.visit_var(self)


class SimpleExpression(Nodo):
    def __init__(self, additive_expression1_p, relop_t, additive_expression2_p):
        self.additive_expression1_p = additive_expression1_p
        self.relop_t = relop_t
        self.additive_expression2_p = additive_expression2_p
        self.tipo = None

    def accept(self, visitor):
        visitor.visit_simple_expression(self)


class AdditiveExpression(Nodo):
    def __init__(self, additive_expression_p, addop_t, term_p):
        self.additive_expression_p = additive_expression_p
        self.addop_t = addop_t
        self.term_p = term_p
        self.tipo = None

    def accept(self, visitor):
        visitor.visit_additive_expression(self)


class Term(Nodo):
    def __init__(self, term_p, mulop_t, factor_p):
        self.term_p = term_p
        self.mulop_t = mulop_t
        self.factor_p = factor_p
        self.tipo = None

    def accept(self, visitor):
        visitor.visit_term(self)


class Num(Nodo):
    def __init__(self, num_t):
        self.num_t = num_t

    def accept(self, visitor):
        visitor.visit_num(self)


class Call(Nodo):
    def __init__(self, id_t, args_p):
        self.id_t = id_t
        self.args_p = args_p
        self.funcion = None
        self.tipo = None

    def accept(self, visitor):
        visitor.visit_call(self)






