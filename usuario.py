class Usuario:
    def __init__(self, login, conexao, online) :
        self.login = login
        self.conexao = conexao
        self.online =  online
        self.mensagens = []