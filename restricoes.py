from variaveis import * 
from utils import * 


"""
Disciplina uma vez por semestre
Disciplina em um turno só
"""
def restricao_1():
    
    global variaveis,horario_por_disciplinas, restricoes

    X = []
    for disciplina in variaveis.keys():
        horario_disciplina = horario_por_disciplinas[disciplina]
        valores_de_x = variaveis[disciplina]
        dia = int(horario_disciplina[0]) - 1 #seg =1, ter=2, qua=3...
        
        for semestre in range(1,NUM_MAX_SEMESTRES+1):
            for aula in horario_disciplina[2:]:
                x = get_x(inicio_x=valores_de_x[0],dia=dia,semestre=semestre,horario=int(aula))
                X.append(x)
        
        add_restricao(indices_x=X,menor_que=4)
