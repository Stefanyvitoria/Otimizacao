from variaveis import *
from restricoes import *

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
    listarestricao5 = []
    
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

    print(horario_disciplinas)
    #print(func_objetivo)
    #print(restricoes)
    


if __name__ == "__main__":
    main()

