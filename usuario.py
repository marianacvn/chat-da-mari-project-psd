class Usuario:
    def __init__(self, login, conexao, online) :
        self.login = login
        self.conexao = conexao
        self.online =  online
        self.mensagens = []


    def __str__(self) -> str:
        return f'[Login: {self.login}, Conexão: {self.conexao}, Online: {self.online}, Mensagens: {self.mensagens}]'