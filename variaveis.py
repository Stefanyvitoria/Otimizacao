#CONSTANTES
NUM_MAX_SEMESTRES = 5
NUM_HORARIOS = 12
NUM_DIAS = 5
turnos = {"M": 1, "T": 5, "N": 9}

# VARIÁVEIS
num_disciplinas = 0

quantidade_maxima_variaveis = 0

#Dicionário onde a chave é o horário e o valor é um array com os códigos das diciplinas
horario_disciplinas = {} # '2M1234' : ['12345','67890' ]

#Dicionário onde a chave é o código da disciplina e o valor é o horário dela
horario_por_disciplinas = {} # '12345' : ['2M1234']

#Lista que gurada todas as restrições
restricoes = []

# lista com os coeficientes da função objetivo
func_objetivo = []

# Dicionário onde a chave é o código da disciplina e o valor é a quantidade inicial e final de x's dela
variaveis = {} # '12345':[1,900]

file_disciplinas_concluidas = open("./disciplinas_concluidas.txt", "r", encoding="utf-8").readlines()