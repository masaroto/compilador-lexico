import re

# num_real = re.compile(rf'{num.pattern},[\d]+')
# lista_ident = re.compile(rf'{ident.pattern}[,{ident.pattern}]*')
# fator = re.compile(rf'{ident.pattern}|{num.pattern}')
txt = "x = 12 * 3\n b = a * 2" 

num = re.compile(r'^[\d]+[,\d+]?')
ident = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*')
op_arit = re.compile(r'^[\*|\/|\+|\-]')
op_rel = re.compile(r'^[\=|\<\>|\<|\<\=|\>\=|\>]')
tipo = re.compile(r'^[INTEGER|REAL|STRING]')
coment = re.compile(r'^[\/\/].') #fazer depois pra ignorar comentario
abre_paren = re.compile(r'^\(')
fecha_parent = re.compile(r'^\)')

nome_regra = ["tipo", "num", "ident", "op_arit", "op_rel"]
regras = [tipo, num, ident, op_arit, op_rel]

print(txt)

while txt!="":    
    txt = re.sub(r"^\s+", "", txt, 1)
    # print(txt)
    for x in range (0, len(regras)):
        regra = regras[x]
        # print(regra.pattern)
        lexema = regra.search(txt)
        if lexema: 
            print("token:",lexema.group())
            print("regra:", nome_regra[x])
            txt = txt[lexema.end():]
            break
    if (not lexema):
        if txt != "":
            print(txt[0], "<- esse simbolo não pertence a linguagem")
            break
