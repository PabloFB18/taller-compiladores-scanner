# coding=utf-8
from string import lower

from tabla_simbolos.nodo_funcion import NodoFuncion
from tabla_simbolos.nodo_tabla_simbolos import NodoTablaSimbolos
from tabla_simbolos.nodo_variable import NodoVariable
from tabla_simbolos.tabla_simbolos import TablaSimbolos


class BuildTablaSimbolosVisitor(object):
    def __init__(self):
        # La tabla de simbolos.
        self.tabla_simbolos = TablaSimbolos()
        # Lista de las funciones.
        self.funciones = []
        # Nodo que se encuentra siendo modificado, se va cambiando cuando se crea otro.
        self.nodo = NodoTablaSimbolos()

    def visit_program(self, program):
        # Crear el nodo raiz y agregarlo.
        self.nodo = NodoTablaSimbolos()
        self.tabla_simbolos.root = self.nodo
        # Expanir el arbol para seguir el analisis.
        for declaration in program.declarations_p:
            declaration.accept(self)
        # Asociar a nodo AST.
        program.simbolos = self.nodo

    def visit_var_declaration(self, var_declaration):
        # Revisar si ya esta declarada la variable.
        error_var = self.nodo.check_repetido(var_declaration.id_t)
        if error_var is None:
            # Añadir la declaracion al nodo de la tabla de simbolos.
            self.nodo.new_entry(var_declaration.id_t, var_declaration.type_specifier_t, var_declaration.numero_si_no)
        else:
            # Indicar el error.
            print 'error en declaracion de variable: ' + error_var

    def visit_fun_declaration(self, fun_declaration):
        # Revisar si ya esta declarada la funcion.
        error_fun = None
        for funcion in self.funciones:
            if funcion.nombre == fun_declaration.id_t and funcion.tipo == fun_declaration.type_specifier_t:
                error_fun = funcion
                break
        # Crear la nueva funcion
        fun = NodoFuncion(fun_declaration.id_t, fun_declaration.type_specifier_t)
        # Crear nuevo nodo de la tabla de simbolos.
        new_nodo = NodoTablaSimbolos()
        # Agregar el nuevo nodo al nodo padre.
        self.nodo.hijos.append(new_nodo)
        # Guardar el nodo padre por si hay mas declaraciones de variables despues de la funcion.
        nodo_padre = self.nodo
        # cambiar el nodo sobre el cual se esta trabajando.
        self.nodo = new_nodo
        # Yo soy tu padre
        self.nodo.padre = nodo_padre
        # Se agrega la funcion a la lista de funciones.
        self.funciones.append(fun)
        # Visitar los nodos que contienen los parametros.
        if fun_declaration.params_p is not None:
            for param in fun_declaration.params_p:
                param.accept(self)
        # TODO: que hacer si es sobrecarga
        if error_fun is not None:
            print 'error en funcion: ' + error_fun
        # Visitar el contenido de la funcion.
        if fun_declaration.compound_stmt_p.local_declarations_p is not None or fun_declaration.compound_stmt_p\
                .stmt_list_p is not None:
            fun_declaration.compound_stmt_p.accept(self)
        # Asociar a nodo AST.
        fun_declaration.simbolos = self.nodo
        # Asociar lista funciones a nodo AST.
        fun_declaration.funcion = self.nodo
        # Volver al nodo padre.
        self.nodo = nodo_padre

    def visit_param(self, param):
        error_param = self.nodo.check_repetido(param.id_t)
        if error_param is None:
            self.nodo.new_entry(param.id_t, param.type_specifier_t, param.arreglo_si_no)
            self.funciones[len(self.funciones)-1].parametros.append(NodoVariable(param.id_t, param.type_specifier_t,
                                                                                 param.arreglo_si_no))
        else:
            print 'error en parametro: ' + error_param

    def visit_compound_stmt(self, compound_stmt):
        # Crear nuevo nodo de la tabla de simbolos.
        new_nodo = NodoTablaSimbolos()
        # Agregar el nuevo nodo al nodo padre.
        self.nodo.hijos.append(new_nodo)
        # Guardar el nodo padre por si hay mas declaraciones de variables despues de la funcion.
        nodo_padre = self.nodo
        # cambiar el nodo sobre el cual se esta trabajando.
        self.nodo = new_nodo
        # Yo soy tu padre
        self.nodo.padre = nodo_padre
        # Visitar los nodos que contienen los parametros.
        if compound_stmt.local_declarations_p is not None:
            for local_declaration in compound_stmt.local_declarations_p:
                if local_declaration is not None:
                    local_declaration.accept(self)
        if compound_stmt.stmt_list_p is not None:
            for stmt in compound_stmt.stmt_list_p:
                if stmt is not None:
                    stmt.accept(self)
        # Asociar a nodo AST.
        compound_stmt.simbolos = self.nodo
        # Volver al nodo padre.
        self.nodo = nodo_padre

    def visit_selection_stmt(self, selection_stmt):
        # Crear nuevo nodo de la tabla de simbolos.
        new_nodo = NodoTablaSimbolos()
        # Agregar el nuevo nodo al nodo padre.
        self.nodo.hijos.append(new_nodo)
        # Guardar el nodo padre por si hay mas declaraciones de variables despues de la funcion.
        nodo_padre = self.nodo
        # cambiar el nodo sobre el cual se esta trabajando.
        self.nodo = new_nodo
        # Yo soy tu padre
        self.nodo.padre = nodo_padre
        # Visitar los nodos.
        if not selection_stmt.else_si_no:
            selection_stmt.expression_p.accept(self)
            if selection_stmt.stmt_p is not None:
                selection_stmt.stmt_p.accept(self)
        else:
            selection_stmt.expression_p.accept(self)
            if selection_stmt.stmt_p is not None:
                selection_stmt.stmt_p.accept(self)
            if selection_stmt.stmt2_p is not None:
                # Crear nuevo nodo de la tabla de simbolos.
                new_nodo = NodoTablaSimbolos()
                # Agregar el nuevo nodo al nodo padre.
                self.nodo.hijos.append(new_nodo)
                # Guardar el nodo padre por si hay mas declaraciones de variables despues de la funcion.
                nodo_padre = self.nodo
                # cambiar el nodo sobre el cual se esta trabajando.
                self.nodo = new_nodo
                # Yo soy tu padre
                self.nodo.padre = nodo_padre
                # Visitar los nodos.
                selection_stmt.stmt2_p.accept(self)
                # Asociar a nodo AST.
                selection_stmt.simbolos = self.nodo
                # Volver al nodo padre.
                self.nodo = nodo_padre
        # Asociar a nodo AST.
        selection_stmt.simbolos = self.nodo
        # Volver al nodo padre.
        self.nodo = nodo_padre

    def visit_iteration_stmt(self, iteration_stmt):
        # Crear nuevo nodo de la tabla de simbolos.
        new_nodo = NodoTablaSimbolos()
        # Agregar el nuevo nodo al nodo padre.
        self.nodo.hijos.append(new_nodo)
        # Guardar el nodo padre por si hay mas declaraciones de variables despues de la funcion.
        nodo_padre = self.nodo
        # cambiar el nodo sobre el cual se esta trabajando.
        self.nodo = new_nodo
        # Yo soy tu padre
        self.nodo.padre = nodo_padre
        # Visitar los nodos.
        iteration_stmt.expression_p.accept(self)
        if iteration_stmt.stmt_p is not None:
            iteration_stmt.stmt_p.accept(self)
        # Asociar a nodo AST.
        iteration_stmt.simbolos = self.nodo
        # Volver al nodo padre.
        self.nodo = nodo_padre

    def visit_return_stmt(self, return_stmt):
        if return_stmt.expression_si_no:
            if lower(self.funciones[len(self.funciones) - 1].tipo) == 'void':
                print 'Error funcion ' + self.funciones[len(self.funciones)-1].nombre + \
                  ' declarada void no debe retornar un valor'
            return_stmt.expression_p.accept(self)
        else:
            if lower(self.funciones[len(self.funciones)-1].tipo) == 'int':
                print 'Error funcion ' + self.funciones[len(self.funciones)-1].nombre + \
                      ' declarada int debe retornar un valor'

    def visit_expression(self, expression):
        expression.var_p.accept(self)
        expression.expression_p.accept(self)

    # TODO: revisar si se declaro
    def visit_var(self, var):
        if not self.nodo.check_declarado(var.id_t):
            print 'Error variable ' + var.id_t + ' no declarada'
        if var.expression_si_no:
            var.expression_p.accept(self)

    def visit_simple_expression(self, simple_expresion):
        simple_expresion.additive_expression1_p.accept(self)
        simple_expresion.additive_expression2_p.accept(self)

    def visit_additive_expression(self, additive_expresion):
        additive_expresion.additive_expression_p.accept(self)
        additive_expresion.term_p.accept(self)

    def visit_term(self, term):
        term.term_p.accept(self)
        if term.factor_p is not None:
            term.factor_p.accept(self)

    def visit_num(self, num):
        pass

    def visit_call(self, call):
        if call.args_p is not None:
            for arg in call.args_p:
                arg.accept(self)
