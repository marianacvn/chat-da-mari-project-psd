import threading
import socket
from datetime import datetime

from cadastro_usuario import*
from cadastro_grupo import*
from cadastro_mensagens import*
from configuracao import *
from grupo import*
from usuario import*


class Servidor():

    def __init__(self):

        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.servidor.bind(ADDR)

        self.usuario = []
        self.listaUsuarios = []
        self.grupos = buscar_grupos(ler_grupo())

        self.ativo = True

        print("#############  Chat da Mari #############\n")
        print("Inicializando servidor...")

        self.servidor.listen()
        print(f"[LISTENING] Server is listening on {SERVER} port {PORT}")

        self.usuario = ler_usuario()

        for usr in self.usuario:
            u = Usuario(usr, None, False)
            self.listaUsuarios.append(u)

        self.assinar()

    def assinar(self):
        while self.ativo:
            try:
                conexao, addr = self.servidor.accept()

                usuario = ''
                tamanho_usuario = int(conexao.recv(HEADER).decode(FORMAT))
                usuario = conexao.recv(tamanho_usuario).decode(FORMAT)

                for usr in self.listaUsuarios:
                    if usr.login == usuario:
                        usr.conexao = conexao
                        usr.online = True
                    else:
                        if valida_usuario(self.usuario, usuario):
                            u = Usuario(usuario, None, False)
                            u.conexao = conexao
                            u.online = True
                            self.listaUsuarios.append(u)
                            self.usuario.append(usuario)

                thread = threading.Thread(target=self.atualizar, args=(conexao, usuario))
                thread.start()

                conectados = 0

                for u in self.listaUsuarios:
                    if u.online == True:
                        conectados +=1

                msg = f"{usuario} entrou no chat. Quantidade de Usuários {conectados}."
                self.mensagemServidor(msg)

            except:
                print("[CLOSING] Server is closing.")
                self.servidor.close()
                self.ativo = False
                return


    def cancelarAssinatura(self, conexao, usuario):
        for u in self.listaUsuarios:
            if u.conexao == conexao:
                usr = Usuario(u.login, None, False)
                self.listaUsuarios.append(usr)
                self.listaUsuarios.remove(u)

        conexao.close()

        _data_atual = data_atual()
        msg = (f"{usuario} saiu *-* ({_data_atual}).")
        self.mensagemServidor(msg)


    def atualizar(self, conexao, usuario):
        cliente_ativo = True
        while cliente_ativo:
            try:
                tamanho_mensagem = conexao.recv(HEADER).decode(FORMAT)
                if tamanho_mensagem:
                    tamanho_mensagem = int(tamanho_mensagem)
                    msg = conexao.recv(tamanho_mensagem).decode(FORMAT)

                    if msg == DISCONNECT_MESSAGE:
                        self.cancelarAssinatura(conexao, usuario)
                        cliente_ativo = False
                        return

                    self.comandos(msg, conexao, usuario)


            except:
                self.cancelarAssinatura(conexao, usuario)
                cliente_ativo = False
                return

    def comandos(self, msg, conexao, usuario):

        if ("-listarusuarios" in msg):

            message = '\n-> Lista de usuários cadastrados:\n'
            message += '-> Login  | Online:\n'
            for txt in self.listaUsuarios:
                status = 'Não'
                if (txt.online == True):
                    status = 'Sim'
                message += '- ' + txt.login + ' - ' + status + '\n'

            self.mensagemPublica(message, conexao, usuario, True)

        elif ("-criargrupo" in msg):

            message = msg.split(" ")
            g = Grupo(message[1], usuario)

            if len(self.grupos) == 0:
                cadastrar_grupo(g)
                self.grupos.append(g)
                self.mensagemPublica(f'O grupo {g.nome} foi criado com sucesso!', conexao, usuario, True)
            else:
                resultado = True
                for group in self.grupos:
                    if g.nome != group.nome:
                        if cadastrar_grupo(g)  :
                            self.grupos.append(g)
                            self.mensagemPublica(f'O grupo {g.nome} foi criado com sucesso!', conexao, usuario, True)
                            resultado = False
                if resultado:
                    self.mensagemPublica(f'O grupo {g.nome} já está cadastrado!', conexao, usuario, True)

        elif ("-listargrupos" in msg):

            message = '\n-> Lista de Grupos criados:\n'
            for grupo in self.grupos:
                message += ' - ' + grupo.nome + '\n'

            self.mensagemPublica(message, conexao, usuario, True)

        elif ("-listausrgrupo" in msg):

            message = msg.split(" ")
            g = Grupo(message[1], usuario)

            if len(self.grupos) == 0:
                self.mensagemPublica('Nenhum grupo foi criado!', conexao, usuario, True)
            else:
                resultado = True
                for group in self.grupos:
                    if g.nome == group.nome:
                        message = f'\n-> Lista de Usuários do Grupo [{g.nome}]:\n'
                        for usr in group.usuarios:
                            message += ' - ' + usr + '\n'
                        self.mensagemPublica(message, conexao, usuario, True)
                        resultado = False
                if resultado:
                    self.mensagemPublica(f'Nenhum grupo encontrado com o nome {g.nome}', conexao, usuario, True)

        elif ("-entrargrupo " in msg):

            message = msg.split(" ")
            g = Grupo(message[1], usuario)

            if len(self.grupos) == 0:
                self.mensagemPublica('Nenhum grupo foi criado!', conexao, usuario, True)
            else:
                resultado = True
                for group in self.grupos:
                    if g.nome == group.nome:
                        if group.inserir_usuario(usuario):
                            self.grupos[self.grupos.index(group)] = group
                            atualizar_grupos(self.grupos)
                            self.mensagemPublica(f'O usuário {usuario} entrou no grupo {g.nome}!', conexao, usuario, True)
                            resultado = False
                        else:
                            self.mensagemPublica(f'O usuário {usuario} já está no grupo {g.nome}!', conexao, usuario, True)
                            resultado = False
                if resultado:
                    self.mensagemPublica(f'O grupo {g.nome} não existe!', conexao, usuario, True)

        elif ("-sairgrupo" in msg):

            message = msg.split(" ")
            g = Grupo(message[1], usuario)

            if len(self.grupos) == 0:
                self.mensagemPublica('Nenhum grupo foi criado!', conexao, usuario, True)
            else:
                resultado = True
                for group in self.grupos:
                    if g.nome == group.nome:
                        if group.remover_usuario(usuario):
                            self.grupos[self.grupos.index(group)] = group
                            atualizar_grupos(self.grupos)
                            self.mensagemPublica(f'O usuário {usuario} saiu do grupo {g.nome}!', conexao, usuario, True)
                            resultado = False
                        else:
                            self.mensagemPublica(f'O usuário {usuario} não está no grupo {g.nome}!', conexao, usuario, True)
                            resultado = False
                if resultado:
                    self.mensagemPublica(f'O grupo {g.nome} não existe!', conexao, usuario, True)

        elif ("-msgt" in msg):
            message = msg.split(" ")

            op = message[1]
            if (op == 'C'):
                for u in self.listaUsuarios:
                    if u.online == True and u.conexao != conexao:
                        self.mensagemPublica(msg, conexao, usuario, False)
            elif (op == 'D'):
                listaUsuOffline = []
                for u in self.listaUsuarios:
                    if u.online == False:
                        listaUsuOffline.append(u)
                self.mensagemOffline(msg, conexao, usuario, listaUsuOffline)
            elif (op == 'T'):
                for u in self.listaUsuarios:
                    if u.online == True and u.conexao != conexao:
                        self.mensagemPublica(msg, conexao, usuario, False)

                listaUsuOffline = []
                for u in self.listaUsuarios:
                    if u.online == False:
                        listaUsuOffline.append(u)
                self.mensagemOffline(msg, conexao, usuario, listaUsuOffline)
            else:
                self.mensagemPublica(f'Comando não encontrado', conexao, usuario, True)

        elif ("-msg" in msg): #-msg U ou G NICK/GRUPO
            message = msg.split(" ")

            op = message[1]
            if (op == 'U'):
                user = message[2]
                resultado  = True
                for u in self.usuario:
                    if u == user:
                        self.mensagemPublica(msg, conexao, usuario, False)
                        resultado = False
                if resultado:
                    self.mensagemPublica(f'O usuário {user} não está cadastrado!', conexao, usuario, True)

            if (op == 'G'):
                gru = message[2]
                resultado  = True
                for g in self.grupos:
                    if g.nome == gru:
                        self.mensagemPublica(msg, conexao, usuario, False)
                        resultado = False
                if resultado:
                    self.mensagemPublica(f'O grupo {gru} não existe!', conexao, usuario, True)

        else:
            self.mensagemPublica(msg, conexao, usuario, False)
            msg = ''

    def mensagemServidor(self, msg):

        print(msg)

        mensagem, enviar_tamanho = codificarMensagem(msg)

        for cliente in self.listaUsuarios:
            if cliente.conexao != None:
                cliente.conexao.send(enviar_tamanho)
                cliente.conexao.send(mensagem)

    def mensagemPublica(self, msg, conexao, usuario, comando):

        _data_atual = data_atual()

        msgTodos = (f"{usuario} ({_data_atual}): {msg}")
        msgMinha = (f"Eu ({_data_atual}): {msg}")
        print(msgTodos)

        mensagem, enviar_tamanho = codificarMensagem(msgTodos)
        mensagemMinha, enviar_tamanhoMinha = codificarMensagem(msgMinha)


        if (comando):
            conexao.send(enviar_tamanhoMinha)
            conexao.send(mensagemMinha)
        else:
            for cliente in self.listaUsuarios:
                if cliente.conexao != None:
                    if(cliente.conexao != conexao):
                        cliente.conexao.send(enviar_tamanho)
                        cliente.conexao.send(mensagem)
                    else:
                        cliente.conexao.send(enviar_tamanhoMinha)
                        cliente.conexao.send(mensagemMinha)

    def mensagemOffline(self, msg, conexao, usuario, usuarios):

        _data_atual = data_atual()

        msgTodos = (f"{usuario} ({_data_atual}): {msg}")
        msgMinha = (f"Eu ({_data_atual}): {msg}")
        print(msgTodos)

        mensagemMinha, enviar_tamanhoMinha = codificarMensagem(msgMinha)

        for cliente in usuarios:
            if(cliente.conexao != conexao):
                message = msgTodos.split(" ")
                text = ''
                message.pop(4)
                message.pop(4)
                for txt in message:
                    text += txt + ' '
                cadastrar_mensagem(Mensagem(cliente.login, text))

        conexao.send(enviar_tamanhoMinha)
        conexao.send(mensagemMinha)


def data_atual():
    data_atual = datetime.now()
    hora_atual = data_atual.strftime("%H:%M:%S")
    return(f"{data_atual.day}/{data_atual.month}/{data_atual.year} - {hora_atual}")

def codificarMensagem(msg):
    mensagem = str(msg).encode(FORMAT)
    tamanho_mensagem = len(mensagem)
    enviar_tamanho = str(tamanho_mensagem).encode(FORMAT)
    enviar_tamanho += b' ' * (HEADER - len(enviar_tamanho))
    return mensagem, enviar_tamanho

if ("__main__" == __name__):
    s = Servidor()
