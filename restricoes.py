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

"""
Disciplinas que tem precedência não podem ficar no primeiro semestre.
"""
def restricao_6():
    
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
        
