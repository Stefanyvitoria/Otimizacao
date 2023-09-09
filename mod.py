# num_semestre = 5
# turno = 3
# hora = 12
# dias  = 5

# # qual o x da célula E[12,24]

# celula_inicial = 1
# celula_final = 300

# celula_qualquer = 10

# linha = celula_final/(num_semestre*dias)
# # print(linha) 
# seg = 1
# ter = 2
# qua = 3
# qui = 4
# sex = 5

# # print(celula_qualquer%(hora))
# # print(10%(15))

quant_dias = 5
num_semestre = 5
d = 1 #seg, ter
s = 1 #semestre
h = 1 # horário


print( (d + (s-1) * quant_dias ) + (quant_dias * num_semestre) * (h-1) )