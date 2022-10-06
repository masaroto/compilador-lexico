import re
import os

path = "exemplos/maior.ilp"

if os.path.isfile(path):
    file = open(path, "r")
    txt = str(file.read())
    file.close()



coment = re.compile(r'//.*[\n]') #ER pra achar comentario
pro = re.compile(r'^PROGRAM')
wri = re.compile(r'^WRITE')
end = re.compile(r'^END')
beg = re.compile(r'^BEGIN')
pv = re.compile(r'^;')
doisp = re.compile(r'^:')
vir = re.compile(r'^,')
var = re.compile(r'^VAR')
se = re.compile(r'^IF')
ent = re.compile(r'^ELSE')
the = re.compile(r'^THEN')
num = re.compile(r'^[\d]+[,\d+]?')
ident = re.compile(r'^[a-zA-Z][a-zA-Z0-9]*')
op_arit = re.compile(r'^\*|^\/|^\+|^\-')
op_rel = re.compile(r'^\=|^\<\>|^\<|^\<\=|^\>\=|^\>')
tipo = re.compile(r'^INTEGER|^REAL|^STRING')
abre_paren = re.compile(r'^\(')
fecha_parent = re.compile(r'^\)')

nome_regra = ["pro", "wri", "end", "beg",
              "pv", "doisp", "vir",
              "var", "num", "se", "ent", "the",
              "ident", "op_arit", "op_rel",  
              "abre_paren", "fecha_parent", "tipo"]

              
regras = [pro, wri, end, beg, 
          pv,doisp, vir, 
          var, tipo, se, ent, the,
          ident, op_arit, op_rel, 
          abre_paren, fecha_parent, tipo]

txt = re.sub(coment, "", txt)
print(txt)
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
