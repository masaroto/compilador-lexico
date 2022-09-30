import re

txt = "x = 12 * 3\nb = a * 2\n//teste aaifbisbfgioafbgiabsdfpibsdfisbdnfipbpibpibpii sabvdoB !@#% ¨& * ()-+=§\n" 

coment = re.compile(r'//.*[\n]$') #ER pra achar comentario
num = re.compile(r'^[\d]+[,\d+]?')
ident = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*')
op_arit = re.compile(r'^[\*|\/|\+|\-]')
op_rel = re.compile(r'^[\=|\<\>|\<|\<\=|\>\=|\>]')
tipo = re.compile(r'^[INTEGER|REAL|STRING]')
abre_paren = re.compile(r'^\(')
fecha_parent = re.compile(r'^\)')

nome_regra = ["tipo", "num", "ident", "op_arit", "op_rel"]
regras = [tipo, num, ident, op_arit, op_rel]

txt = re.sub(coment, "", txt)
# print(txt)

while txt!="":    
    txt = re.sub(r"^\s+", "", txt, 1)
    for x in range (0, len(regras)):
        regra = regras[x]
        lexema = regra.search(txt)
        if lexema: 
            print("token:",lexema.group(), "| regra:", nome_regra[x])
            txt = txt[lexema.end():]
            break
    if (not lexema):
        if txt != "":
            print("Erro: ", txt[0], "<- esse simbolo não pertence a linguagem")
            break
