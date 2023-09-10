###############################################
# VARIÁVES
###############################################

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
file_precedencia_por_disciplinas.close()

# Abrir o arquivo txt de precedentes
file_precedencia_por_disciplinas2 = open("./disciplinas_precedentes.txt", "r", encoding="utf-8")

###############################################
# ÚTILS
###############################################

def get_x(inicio_x,semestre, horario, dia):
    return (inicio_x-1) +(dia + (semestre-1) * NUM_DIAS ) + (NUM_DIAS * NUM_MAX_SEMESTRES) * (horario-1)


def add_restricao(indices_para_receber_1, valor_depois_do_igual):
    global NUM_HORARIOS, NUM_MAX_SEMESTRES, NUM_DIAS, num_disciplinas,quantidade_maxima_variaveis, restricoes
    restricao = []

    for i in range(1,1+quantidade_maxima_variaveis):
        if i in indices_para_receber_1:
            restricao.append(1)
        else:
            restricao.append(0)

    restricoes.append([restricao, valor_depois_do_igual])



###############################################
# RETRIÇÕES
###############################################
"""
Disciplina uma vez por semestre
Disciplina em um turno só
"""
def restricao_1():
    global num_disciplinas, quantidade_maxima_variaveis, horario_disciplinas, variaveis, horario_por_disciplinas
    
    X = []
    for disciplina in variaveis.keys():
        horario_disciplina = horario_por_disciplinas[disciplina]
        valores_de_x = variaveis[disciplina]
        dia = int(horario_disciplina[0]) - 1 #seg =1, ter=2, qua=3...
        
        for semestre in range(1,NUM_MAX_SEMESTRES+1):
            for aula in horario_disciplina[2:]:
                x = get_x(inicio_x=valores_de_x[0],dia=dia,semestre=semestre,horario=int(aula))
                X.append(x)
        add_restricao(X,4)

"""
Restrição de não alocar disciplinas em horários de indisponibilidade do usuário.
"""
def restricao_2(disciplina):
    # Extrai os dados da disciplina
    codigo_disc, nome_disc, turma_disc, horario_disc = disciplina.replace("\n", "").split(",")
    # Separa o dia e as horas do horário da disciplina
    dia_disc = horario_disc[:2]
    horas_disc = list(horario_disc[2:])
    
    # Percorre os horários indisponíveis
    for horario_indisponivel in horarios_indisponiveis:
        # Separa o dia e as horas do horário indisponível
        dia_indisponivel = horario_indisponivel[:2]
        horas_indisponivel = horario_indisponivel[2:]
        # Verifica se o dia da disciplina coincide com o dia indisponível
        if dia_disc == dia_indisponivel:
            # Verifica se alguma hora da disciplina coincide com alguma hora indisponível
            for hora_disc in horas_disc:
                if hora_disc in horas_indisponivel:
                    # Retorna True se houver coincidência, indicando que há restrição
                    return True   
    # Retorna False se não houver coincidência, indicando que não há restrição
    return False


"""
Elimina as disciplinas que o usuário já concluiu.
"""
def restricao_3(diciplina):

    if diciplina.split(',')[0] in disciplinas_concluidas: 
        return True
    return False

def restricao_4():
  for disciplina in precedencia_por_disciplinas.keys():
    # Obter as cadeiras que precedem a disciplina dependente
    precedentes = precedencia_por_disciplinas[disciplina]
    for precedente in precedentes: #cada uma das cadeiras anteriores da dependente
      # Obter horario da disciplina dependente
      horario_disciplina = horario_por_disciplinas[disciplina]
      # Obter o range de x para a disciplina dependente
      valores_de_x = variaveis[disciplina]
      # Obter dia da disciplina dependente
      dia = int(horario_disciplina[0]) - 1 #seg =1, ter=2, qua=3...
      # Obter horario da disciplina precedente
      horario_precedente = horario_por_disciplinas[precedente]
      # Obter range de x da disciplina precedente
      valores_de_x_precedente = variaveis[precedente]
      # Obter dia da disciplina precedente
      dia_precedente = int(horario_precedente[0]) - 1 #seg =1, ter=2, qua=3...
      for semestre_precedente in range(1,NUM_MAX_SEMESTRES): #shift
        # Inicializa lista de somas de X
        X = []
        for aula in horario_precedente[2:]:
          x = get_x(inicio_x=valores_de_x_precedente[0],dia=dia_precedente,semestre=semestre_precedente,horario=int(aula))
          X.append(x)
        for semestre_dependente in range(semestre_precedente+1,NUM_MAX_SEMESTRES+1): # Adiciona todas seguintes da disciplina dependente
          for aula in horario_precedente[2:]:
            x = get_x(inicio_x=valores_de_x[0],dia=dia,semestre=semestre_dependente,horario=int(aula))
            X.append(x)
        add_restricao(X,4)

#def restricao_5(disciplina, lista):
    if disciplina[3] in lista:
        return False
    else:
        lista.append(disciplina[3])

"""
Disciplinas que tem precedência não podem ficar no primeiro semestre.
"""
def restricao_6():
    precedencia_disciplinas = file_precedencia_por_disciplinas2.readlines()
    for disciplinas in precedencia_disciplinas:
        if disciplinas[0] == "#": 
            continue
            
        # Verifica se a que ela depende já foi conluída
        disciplina_dependente, disciplina_requesito = disciplinas.replace('\n','').split(',')
        disciplinas_concluidas = [d.split(',')[0] for d in file_disciplinas_concluidas]
        if disciplina_requesito in disciplinas_concluidas:
            continue

        horario_disciplina = horario_por_disciplinas[disciplina_dependente]
        valores_de_x = variaveis[disciplina_dependente]
        dia = int(horario_disciplina[0]) - 1 #seg =1, ter=2, qua=3...
        
        X = []
        for aula in horario_disciplina[2:]:
            x = get_x(inicio_x=valores_de_x[0],dia=dia,semestre=1,horario=int(aula))
            X.append(x)
        
        add_restricao(X,0)
        
###############################################
# MAIN
###############################################
"""Cria a função objetivo"""
def funcao_objetivo(func_objetivo):
    
    global variaveis

    for _ in variaveis:
        func_objetivo.extend([1]*NUM_HORARIOS * NUM_MAX_SEMESTRES * NUM_DIAS)



"""Monta o dicinário de horários"""
def get_horarios_discipinas( lines) :

    global num_disciplinas, quantidade_maxima_variaveis, horario_disciplinas, variaveis, horario_por_disciplinas
    
    x = 1
    num_disciplinas = 0
    for disc in lines:
      
        if disc[0] == "#" or restricao_2(disc) or restricao_3(disc):
            continue

        disc = disc[0:-1].split(",")

        #if restricao_5(disc, listarestricao5) == False:
            #continue
            
        # Monta o dicionários de horários
        if disc[3] in horario_disciplinas.keys():
            horario_disciplinas[f"{disc[3]}"].append([f"{disc[0]}", num_disciplinas])
        else:
            horario_disciplinas[f"{disc[3]}"] = [[f"{disc[0]}", num_disciplinas]]
        num_disciplinas+=1

        #Atribui a quantidade dos E[i,j] dessa disciplina
        x_aux = x + (NUM_HORARIOS * NUM_MAX_SEMESTRES * NUM_DIAS)
        variaveis[disc[0]] = [x, x_aux-1]
        x = x_aux
        horario_por_disciplinas[disc[0]] = f"{disc[3]}"

    quantidade_maxima_variaveis = NUM_HORARIOS * NUM_MAX_SEMESTRES * NUM_DIAS * num_disciplinas



def main():

    file_disciplinas = open("./disciplinas.txt", "r", encoding="utf-8")
    lines = file_disciplinas.readlines()

    get_horarios_discipinas(lines=lines)

    funcao_objetivo(func_objetivo=func_objetivo)
    restricao_1()
    restricao_4()
    restricao_6()

    # print(horario_disciplinas)
    print(func_objetivo)
    print(restricoes)


if __name__ == "__main__":
    main()