import re
import os
import sys 

path_dir = "/exemplos/"


class Token(object):
    # Objeto token
    
    def __init__(self, type, val, pos):
        self.type = type # Token name
        self.val = val # Token valor (lexema)
        self.pos = pos # Posição em que o lexema foi encontrado no arq.

    def __str__(self):
        return '(%s, %s)' % (self.type, self.val)

def select_arq():
    
    # Seleção de arquivo para leitura

    print("===========================================")
    print("Digite o número correspondente ao arquivo que deseja carregar:\n")
    filenames = next(os.walk(os.getcwd() + path_dir), (None, None, []))[2]
    files = [ file for file in filenames if file.endswith((".ilp", ".ILP")) ]

    if len(files) == 0:
        print("Não existe arquivo .ilp no diretório exemplos.")
        sys.exit()

    for i in range(0, len(files)):
        print('[{}] {}'.format(i, files[i]))
    index = input("\n")

    while not index.isdigit() or int(index) >= len(files) or int(index) < 0:
        print("\nEsta opção não existe, digite novamente.")
        index = input("\n")

    path_file = os.getcwd() + path_dir + files[int(index)]

    if os.path.isfile(path_file):
        file = open(path_file, "r")
        txt = str(file.read())
        file.close()
    
    return txt


rules = [
    
    # Palavras-reservadas


    ("pro"       ,'PROGRAM'), #(token_name, regex)
    ("wri"       ,'WRITE'),
    ("read"      ,'READ'),
    ("end"       ,'END'),
    ("beg"       ,'BEGIN'),
    ("var"       ,'VAR'),
    ("se"        ,'IF'),
    ("ent"       ,'ELSE'),
    ("the"       ,'THEN'),
    ("for"       ,'FOR'),
    ("to"        ,'TO'),
    ("do"        ,'DO'),
    ("tipo"      ,'INTEGER|REAL|STRING'),
    ("typ"      ,'TYPE'),
    

    # Operadores
    
<<<<<<< HEAD
    ("op_arit"   ,'\*|\/'),
    ("MaiorMenor", '\+|\-'),
    ("op_rel"    ,'\:\=|\<\>|\<|\<\=|\>\=|\>'),
=======
    ("op_arit"   ,'\*|\/|\+|\-'),
    ("op_rel"    ,'\=|\<\>|\<\=|\<|\>\=|\>'),
    ("atrib"     ,':\='),
>>>>>>> 5a499bccac9c6dec9c3bfb390e90cf7371b199f7
    
    # Identificador 
    
    ("ident"     ,'[a-zA-Z][a-zA-Z0-9]*'),

    # Separadores

    ("pv"        ,';'),
    ("doisp"     ,':'),
    ("vir"       ,','),
    ("AP"        ,'\('),
    ("FP"        ,'\)'),
    ("AC"        ,'\{'),
    ("FC"        ,'\}'),
    ("ACO"       ,'\['),
    ("FCO"       ,'\]'),
    
    # Literal

    ("num"       ,'[\d]+[,\d+]?')
]

def Lexer(src_code):
    aux = 1
    regex_parts = []
    group_type = {}
    buffer = src_code
    position = 0
    tokens = []

    # Removendo comentário
    buffer = re.sub("//.*[\n]", "", buffer)
        
    # Dividindo regex em grupos
 
    for type, regex in rules:
        groupname = 'GROUP%s' % aux
        regex_parts.append('(?P<%s>%s)' % (groupname, regex))
        group_type[groupname] = type
        aux += 1

    # Juntando regex em um só
    regex = re.compile('|'.join(regex_parts))

    while True:    
        
        if position >= len(buffer):
            break
        else:
            # Ignorando espaços em branco
            m = re.compile('\S').search(buffer, position);
            if m:
                position = m.start()
            else:
                break
                
        m = regex.match(buffer, position)

        if m:
            groupname = m.lastgroup
            tok_type = group_type[groupname]
            tok = Token(tok_type, m.group(groupname), position)
            position = m.end()
            tokens.append(tok)
        else:
            print("==================================================\n")
            print("ERRO: Caractere " + buffer[position] +
            " na posição %s não é permitido.\n" % (position))
            sys.exit()

    return tokens

# ======= PARSER =======


class nao_terminal():
    def __init__(self, data, childs):
        self.childs = childs
        self.data = data

class terminal():    
    def __init__(self, data):
        self.childs = None
        self.data = data
    
class Parser():
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_idx = 0
        self.current_token = self.tokens[self.token_idx]
        self.terminais = ["num", "ident", "op_arit", "MaiorMenor", "op_rel", "AP", "FP"]
        
    def advance(self):
        self.token_idx += 1
        if self.token_idx < len(self.tokens):
            self.current_token = self.tokens[self.token_idx]
            return self.current_token
        else:
            self.current_token = None
    
    
    def EX (self):
        childs = []
        left = self.EXS()
        if (left):
            childs.append(left)
            if(self.current_token != None):
                if self.current_token.type == "op_rel":
                    relation = self.relacao()
                    if (relation):
                        right = self.EXS()
                        if (right):
                            childs.append(relation)
                            childs.append(right)
                        else:
                            return None
                    else:
                        return None
        else:
            return None
        
        return nao_terminal("Expressao", childs)
    
    
    def EXS (self):
        childs = []
        while True:
            
            if self.current_token.type == "MaiorMenor":
                left = self.MaiorMenor()
                if (left):
                    childs.append(left)
            
            aux = self.T()
            
            if (aux):
                childs.append(aux)
            else:
                return None
            
            if (self.current_token == None):
                break

            if (self.current_token.type == "op_rel" or self.current_token.type == "FP"):
                break
        
        return nao_terminal("Expressao_Simples", childs)
            
    
    
    def T (self):
        left = self.F()
        childs = []
        count = 0
        if (left):
            while True:
                op = self.OP()
                if(op):
                    
                    aux = self.F()

                    if (aux):
                        if (count == 0):
                            childs.append(left)
                        count += 1
                        childs.append(op)
                        childs.append(aux)
                    else:
                        return None
                else:
                    if (count == 0):
                        childs.append(left)
                    break
            return nao_terminal("termo", childs)
        else:
            return None
    
    def F (self):
        childs = []
        left = self.V()
        if (left):
            childs.append(left)
            return nao_terminal("Fator", childs)
        left =  self.N()
        if (left):
            childs.append(left)
            return nao_terminal("Fator", childs)
        left = self.Abre()
        if (left):
            
            mid = self.EX()
            
            if (mid):
                right = self.Fecha()
                if (right):
                    childs.append(left)
                    childs.append(mid)
                    childs.append(right)
                    return nao_terminal("Fator", childs)
            else:
                None
        return None
    
    
    def V (self):
        childs = []
        identificador = self.ID()
        if (identificador):
            childs.append(identificador)
            node = nao_terminal("variavel", childs)
            return node
        else:
            return None
            
    
    
    def ID (self):
        childs = []
    
        left = self.L()
        
        if(left):
            childs.append(left)
            if(self.current_token != None):
                while self.current_token.type == "num" or self.current_token.type == "ident" :
                    if self.current_token.type == "num":
                        childs.append(self.D())
                    else:
                        childs.append(self.L())
                    
                if (self.current_token.type not in self.terminais and self.current_token != None):
                    return None
            node = nao_terminal("identificador", childs)
            return node
            
        else:
            
            return None
    
    
    def N (self):
        childs = []
        left = self.D()
        if(left):
            childs.append(left)
            if(self.current_token != None):
                while self.current_token.type == "num":
                    childs.append(self.D())
                if(self.current_token.type not in self.terminais and self.current_token != None):
                    return None
            
                if(self.current_token.type == "ident"):
                    return None
            return nao_terminal("Numero", childs) 
        else:       
            return None
    
    
    def D (self):
        token = self.current_token
        if (token):
            if token.type == "num":
                self.advance()
                return terminal(token)
            else:
                return None
    
    def L (self):
        token = self.current_token
        if (token):
            if token.type == "ident":
                self.advance()
                return terminal(token)
            else:
                return None
    
    def OP (self):
        token = self.current_token
        if (token):
            if token.type == "op_arit":
                self.advance()
                return terminal(token)
            else:
                return None
    
    def MaiorMenor (self):
        token = self.current_token
        if (token):
            if token.type == "MaiorMenor":
                self.advance()
                return terminal(token)
            else:
                return None
    
    def relacao (self):
        token = self.current_token
        if (token):
            if token.type == "op_rel":
                self.advance()
                return terminal(token)
            else:
                return None
    
    def Abre (self):
        token = self.current_token
        if (token):
            if token.type == "AP":
                self.advance()
                return terminal(token)
            else:
                return None
    
    def Fecha (self):
        token = self.current_token
        if (token):
            if token.type == "FP":
                self.advance()
                return terminal(token)
            else:
                return None

# Printa a AST

def print_arvore (Node):
    lista = []
    if Node.childs == None:
        return 0
    else:
        for i in Node.childs:
            if isinstance(i, terminal):
                lista.append(i.data.val)
            else:
                lista.append(i.data)
            print('{0} : Filhos {1}'.format(Node.data, lista))
            print_arvore(i)
    


def main():
    src_code = select_arq()
    print("==================== Código Fonte =====================\n")
    print(src_code)

    fluxo_tokens = Lexer(src_code)

    print("================== Fluxo de Tokens ===================\n")
    print("(<NomeToken>, <Lexema>)\n")
    for token in fluxo_tokens:
        print(token.__str__())

    print("\n================== Análise Sintática ===================\n")

    Parser_result = Parser(fluxo_tokens)

    Tree = Parser_result.EX()
    
    if (Tree):
        print("Entrada valida\n")
        print("=== Abstract Syntax Tree ===\n")
        print_arvore(Tree)
        print("\n")
    
    else:
        print("Erro Sintático: ENTRADA INVALIDA\n")
        print("Obs: Certifique-se que a entrada é reconhecida pelas regras da gramatica\n")


if __name__ == "__main__":
    main()



