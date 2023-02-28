lista = ['teste', 'teste2']

sinal = False
index = 0

try:
    index = lista.index('teste2')
    sinal = False
except:
    sinal = True

print(sinal)