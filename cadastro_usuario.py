import os

fn = 'usuarios.txt'

def valida_usuario(text, usr):

    resultado = True

    for txt in text:
        if usr == txt:
            resultado = False

    return resultado

def inserir_usuario(text, usr):
    resultado = ''
    for txt in text:
        resultado += txt + "|"
    return resultado + usr


def cadastrar_usuario(usr):
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = usr
            file.write(text)
        return True
    else:
        text = text.split("|")
        if valida_usuario(text, usr):
            with open(fn,'w') as file:
                text = inserir_usuario(text, usr)
                file.write(text)
            return True
        else:
            return False

def ler_usuario():
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
            return text.split("|")
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = ''
            file.write(text)
        return text.split("|")
