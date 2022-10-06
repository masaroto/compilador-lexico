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
    filenames = next(os.walk(os.path.dirname(__file__) + path_dir), (None, None, []))[2]
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

    path_file = os.path.dirname(__file__) + path_dir + files[int(index)]

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
    
    ("op_arit"   ,'\*|\/|\+|\-'),
    ("op_rel"    ,'\:\=|\<\>|\<|\<\=|\>\=|\>'),
    
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
            m = re.compile('\S').search(buffer, position)
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
            raise SyntaxError("Caractere " + buffer[position] +
            " na posição %s não é permitido." % (position))

    return tokens
        

def main():
    src_code = select_arq()
    print("==================== Código Fonte =====================\n")
    print(src_code)

    floxo_tokens = Lexer(src_code)

    print("================== Fluxo de Tokens ===================\n")
    print("(<NomeToken>, <Lexema>)\n")
    for token in floxo_tokens:
        print(token.__str__())


if __name__ == "__main__":
    main()



