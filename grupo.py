class Grupo():

    def __init__(self, nome, usuario):
        self.nome = nome
        self.usuario = usuario
        self.usuarios = []

    def __str__(self):

        texto = ''
        for txt in self.usuarios:
            texto += txt + ','
        texto = texto.removesuffix(',')
        return f'{self.nome}${self.usuario}${texto}'

    def inserir_usuario(self, usuario):
        for usr in self.usuarios:
            if usuario == usr:
                return False
        self.usuarios.append(usuario)
        return True

    def remover_usuario(self, usuario):
        for usr in self.usuarios:
            if usuario == usr:
                self.usuarios.remove(usr)
                return True
        return False