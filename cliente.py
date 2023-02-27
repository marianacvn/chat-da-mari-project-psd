from configuracao import *
from cadastro_usuario import*
from cadastro_grupo import*
import threading
import socket


class Cliente():

    def __init__(self, usuario, servidor, porta, sinal):

        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ADDR = (servidor, int(porta))
        self.cliente.connect(ADDR)
        self.ativo = True

        if (sinal):
            cadastrar_usuario(usuario)

        self.name = usuario
        self.enviarMensagem(self.name)

        self.thread_recv = threading.Thread(target=self.receberMensagem, args=())
        self.thread_recv.start()

        self.main_loop()


    def main_loop(self):
        while (self.ativo):
            try:
                msg = str(input())

                if (msg != "" and msg != DISCONNECT_MESSAGE):
                    self.enviarMensagem(msg)
                    msg = ""
                else:
                    self.desconectado()
                    self.ativo = False
            except:
                self.desconectado()

    def escolher_comando(self):
        pass

    def enviarMensagem(self, msg):
            try:
                mensagem, enviar_tamanho = codificarMensagem(msg)
                self.cliente.send(enviar_tamanho)
                self.cliente.send(mensagem)

                if (msg == DISCONNECT_MESSAGE):
                    self.desconectado()

            except:
                print("Falha na conexão")
                self.ativo = False


    def receberMensagem(self):

        while self.ativo:
            try:
                msg_tamanho = self.cliente.recv(HEADER).decode(FORMAT)
                if msg_tamanho:
                    msg_tamanho = int(msg_tamanho)
                    msg = self.cliente.recv(msg_tamanho).decode(FORMAT)

                    if ("-msg" in msg): #-msg U ou G NICK/GRUPO
                        message = msg.split(" ")
                        op = message[5]
                        if (op == 'U'):
                            user = message[6]
                            if(user == self.name):
                                text = ''
                                message.pop(4)
                                message.pop(4)
                                message.pop(4)
                                for txt in message:
                                    text += txt + ' '
                                print(text)
                        elif (op == 'G'):
                            grupo = message[6]
                            grupos = buscar_grupos(ler_grupo())
                            for g in grupos:
                                if grupo == g.nome:
                                    for u in g.usuarios:
                                        if u == self.name:
                                            text = ''
                                            message.pop(4)
                                            message.pop(4)
                                            message.pop(4)
                                            for txt in message:
                                                text += txt + ' '
                                            print(text)
                    else:
                        print(msg)
            except:
                self.ativo = False


    def desconectado(self):

        print("Tchau...")
        self.cliente.close()
        self.ativo = False
        print("[Conexão Finalizada]")


def codificarMensagem(msg):
    mensagem = str(msg).encode(FORMAT)
    msg_tamanho = len(mensagem)
    enviar_tamanho = str(msg_tamanho).encode(FORMAT)
    enviar_tamanho += b' ' * (HEADER - len(enviar_tamanho))
    return mensagem, enviar_tamanho




if(__name__ == "__main__"):
    print("#############  Chat da Mari #############\n")

    usuario = input("Insira seu apelido: ")

    usuarios = ler_usuario()

    if valida_usuario(usuarios, usuario) :
        c = Cliente(usuario, SERVER, PORT, True)
    else:
        print(f'Usuário {usuario} já existe, deseja entrar no chat-da-mari? [S - Sim/ N - Não]:')
        resposta = input(">")
        if (resposta == 'S'):
            c = Cliente(usuario, SERVER, PORT, False)
        else:
            print(f'Tchau!')