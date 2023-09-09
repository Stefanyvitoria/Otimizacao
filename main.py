NUM_MAX_SEMESTRES = 5
NUM_HORARIOS = 12
NUM_DIAS = 5
turnos = {"M": 1, "T": 5, "N": 9}

def funcao_objetivo(func_objetivo, variaveis_disc:dict):
    for _ in variaveis_disc:
        func_objetivo.extend([1]*NUM_HORARIOS * NUM_MAX_SEMESTRES * NUM_DIAS)



"""Monta o dicinário de horários"""
def get_horarios_discipinas( lines, horario_disc:dict,horario_por_disc:dict, variaveis:dict) :
    
    x = 1
    i = 0
    for disc in lines:
        if disc[0] == "#":
            continue

        # Monta o dicionários de horários
        disc = disc[0:-1].split(",")
        if disc[3] in horario_disc.keys():
            horario_disc[f"{disc[3]}"].append([f"{disc[0]}", i])
        else:
            horario_disc[f"{disc[3]}"] = [[f"{disc[0]}", i]]
        i+=1

        #Atribui a quantidade dos E[i,j] dessa disciplina
        x_aux = x + (NUM_HORARIOS * NUM_MAX_SEMESTRES * NUM_DIAS)
        variaveis[disc[0]] = [x, x_aux-1]
        x = x_aux

        horario_por_disc[disc[0]] = f"{disc[3]}"
    global NUM_DISCIPLINAS, QUANTIDADE_MAXIMA_VARIAVEIS
    NUM_DISCIPLINAS = i
    QUANTIDADE_MAXIMA_VARIAVEIS = NUM_HORARIOS * NUM_MAX_SEMESTRES * NUM_DIAS *NUM_DISCIPLINAS

def get_x(inicio_x,semestre, horario, dia):
    return (inicio_x-1) +(dia + (semestre-1) * NUM_DIAS ) + (NUM_DIAS * NUM_MAX_SEMESTRES) * (horario-1)

def add_restricao(indices_x, menor_que, restricoes):
    global NUM_HORARIOS, NUM_MAX_SEMESTRES, NUM_DIAS, NUM_DISCIPLINAS
    restricao = []
    for i in range(1,1+QUANTIDADE_MAXIMA_VARIAVEIS):
        if i in indices_x:
            restricao.append(1)
        else:
            restricao.append(0)

    restricoes.append([restricao, 4])

"""
Disciplina uma vez por semestre
Disciplina em um turno só
"""
def restricao_1(variaveis_disc:dict, horarios, variaveis, restricao:list):
    
    X = []
    for disciplina in variaveis_disc.keys():
        horario_disciplina = horarios[disciplina]
        valores_de_x = variaveis[disciplina]
        dia = int(horario_disciplina[0]) - 1 #seg =1, ter=2, qua=3...
        
        for semestre in range(1,NUM_MAX_SEMESTRES+1):
            for aula in horario_disciplina[2:]:
                x = get_x(inicio_x=valores_de_x[0],dia=dia,semestre=semestre,horario=int(aula))
                X.append(x)
        
        add_restricao(indices_x=X,menor_que=4,restricoes=restricao)




def main():
    file_disicplinas = open("./disciplinas.txt", "r", encoding="utf-8")
    lines = file_disicplinas.readlines()

    #Dicionário onde a chave é o horário e o valor é um array com os códigos das diciplinas
    horario_disciplinas = {} # '2M1234' : ['12345']
    horario_por_disciplinas = {} # '2M1234' : ['12345']
    #Lista que gurada todas as restrições
    restricoes = []
    func_objetivo = []
    # Dicionário onde a chave é E[i,j] e o valor é a disciplina na qual ele pertence
    variaveis = {}

    get_horarios_discipinas(lines=lines, horario_disc=horario_disciplinas,horario_por_disc=horario_por_disciplinas, variaveis=variaveis)


    funcao_objetivo(func_objetivo=func_objetivo,variaveis_disc=variaveis)
    restricao_1(variaveis_disc=variaveis,horarios=horario_por_disciplinas,variaveis=variaveis,restricao=restricoes)

    print(horario_disciplinas)
    print(func_objetivo)
    print(restricoes)


if __name__ == "__main__":
    main()