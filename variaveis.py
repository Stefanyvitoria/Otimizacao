#CONSTANTES
NUM_MAX_SEMESTRES = 5
NUM_HORARIOS = 12
NUM_DIAS = 5
turnos = {"M": 1, "T": 5, "N": 9}

# VARIÁVEIS
global num_disciplinas, quantidade_maxima_variaveis
num_disciplinas = 1
quantidade_maxima_variaveis = 1

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

# Abrir o arquivo txt de precedentes
file_precedencia_por_disciplinas = open("./disciplinas_precedentes.txt", "r", encoding="utf-8")

#lista de disciplinas concluídas
file_disciplinas_concluidas = open("./disciplinas_concluidas.txt", "r", encoding="utf-8").readlines()
disciplinas_concluidas = [d.split(',')[0] for d in file_disciplinas_concluidas]

# Criar um dicionário vazio para armazenar os precedentes por disciplina
precedencia_por_disciplinas = {}
# lista com os horários indisponíveis 
horarios_indisponiveis = open("./horarios_indisponiveis.txt", "r", encoding="utf-8").readlines()
# Para cada linha do arquivo, separar os códigos das disciplinas por vírgula
for linha in file_precedencia_por_disciplinas.readlines():
  if linha[0] == '#':
    continue
  disciplinas = linha.split(",")
  # A primeira disciplina da linha é a que depende das outras
  dependente = disciplinas[0]
  # As demais disciplinas da linha são as que precedem a primeira
  precedentes = disciplinas[1:]
  # Remover os espaços em branco e as quebras de linha dos códigos das disciplinas
  dependente = dependente.strip()
  # reune os precedentes em uma lista, verificando se eles não estão na lista de concluidas
  precedentes = [p.strip() for p in precedentes if p.strip() not in disciplinas_concluidas]
  # Adicionar a chave e o valor ao dicionário de precedentes
  precedencia_por_disciplinas[dependente] = precedentes
  # Fechar o arquivo txt de precedentes
# file_precedencia_por_disciplinas.close()

