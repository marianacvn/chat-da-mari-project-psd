import os

fn = 'mensagens.txt'

class Mensagem():
    def __init__(self, usuario, mensagem) :
        self.usuario = usuario
        self.mensagem = mensagem

    def __str__(self):
        return f'{self.usuario}${self.mensagem}'

def inserir_mensagem(mensagens, msg):
    resultado = ''
    for m in mensagens:
        resultado += str(m) + "|"
    if (msg == None):
        resultado = resultado.removesuffix('|')
    else:
        resultado = resultado + str(msg)
    return resultado

def cadastrar_mensagem(msg):
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = str(msg)
            file.write(text)
        return True
    else:
        mensagens = buscar_mensagens(text)
        with open(fn,'w') as file:
            text = inserir_mensagem(mensagens, msg)
            file.write(text)
        return True

def atualizar_mensagens(mensagens):
    if os.path.exists(fn):
        with open(fn) as file:
            text = file.read()
    else:
        text = None

    if not text:
        with open(fn,'w') as file:
            text = inserir_mensagem(mensagens, None)
            file.write(text)
        return True
    else:
        with open(fn,'w') as file:
            text = inserir_mensagem(mensagens, None)
            file.write(text)
            return True

def ler_mensagem():
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

def buscar_mensagens(text):
        mensagens = []

        if len(text) > 0:
            for txt in text.split("|"):
                msg = txt.split('$')
                m = Mensagem(msg[0], msg[1])
                mensagens.append(m)
        return mensagens

# cadastrar_mensagem(Mensagem('davi', 'oladavi tudo tranks'))
# buscar_mensag = buscar_mensagens(ler_mensagem())

# for m in buscar_mensag:
#     if m.usuario == 'davi':
#         buscar_mensag.remove(m)

# atualizar_mensagens(buscar_mensag)

# buscar_mensag = buscar_mensagens(ler_mensagem())

# for m in buscar_mensag:
#     print(m)
