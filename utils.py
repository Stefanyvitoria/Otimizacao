from variaveis import * 

def get_x(inicio_x,semestre, horario, dia):
    return (inicio_x-1) +(dia + (semestre-1) * NUM_DIAS ) + (NUM_DIAS * NUM_MAX_SEMESTRES) * (horario-1)


def add_restricao(indices_para_receber_1, valor_depois_do_igual):
    
    restricao = []

    for i in range(1,1+quantidade_maxima_variaveis):
        if i in indices_para_receber_1:
            restricao.append(1)
        else:
            restricao.append(0)

    restricoes.append([restricao, valor_depois_do_igual])

