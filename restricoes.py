from variaveis import * 
from utils import * 

global variaveis,horario_por_disciplinas, restricoes

"""
Disciplina uma vez por semestre
Disciplina em um turno só
"""
def restricao_1():

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

    disciplinas_concluidas = [d.split(',')[0] for d in file_disciplinas_concluidas]
    if diciplina.split(',')[0] in disciplinas_concluidas: 
        return True
    return False
