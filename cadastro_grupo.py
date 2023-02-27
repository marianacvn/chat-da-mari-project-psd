import os
from grupo import*

fn = 'grupos.txt'

def valida_grupo(grupos, grupo):

    resultado = True

    for group in grupos:
        if grupo.nome == group.nome:
            resultado = False

    return resultado

def inserir_grupo(grupos, grupo):
    resultado = ''
    for g in grupos:
        resultado += str(g) + "|"
    if (grupo == None):
        resultado = resultado.removesuffix('|')
    else:
        resultado = resultado + str(grupo)
    return resultado

def cadastrar_grupo(grupo):
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = str(grupo)
            file.write(text)
        return True
    else:
        grupos =buscar_grupos(text)

        if valida_grupo(grupos, grupo):
            with open(fn,'w') as file:
                text = inserir_grupo(grupos, grupo)
                file.write(text)
            return True
        else:
            return False

def atualizar_grupos(grupos):
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = inserir_grupo(grupos, None)
            file.write(text)
        return True
    else:
        with open(fn,'w') as file:
            text = inserir_grupo(grupos, None)
            file.write(text)
            return True

def ler_grupo():
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
            return text
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = ''
            file.write(text)
        return text

def buscar_grupos(text):

        grupos = []

        if len(text) > 0:
            for txt in text.split("|"):
                gru = txt.split('$')
                g = Grupo(gru[0], gru[1])
                usu = gru[2].split(',')
                for usr in usu:
                    g.inserir_usuario(usr)
                grupos.append(g)
        return grupos


# g = Grupo('JASES', 'davi')
# g.inserir_usuario('davi')
# g.inserir_usuario('jose')
# cadastrar_grupo(g)


# g = buscar_grupos(ler_grupo())

# gru = Grupo('JOSES', 'davi')
# gru.inserir_usuario('davi')

# g[0] = gru

# atualizar_grupos(g)

# for g in buscar_grupos(ler_grupo()):
#     print(g.nome + ' - ' + g.usuario + ' - ' + str(g.usuarios))