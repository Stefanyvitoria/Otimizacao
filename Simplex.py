import numpy as np

class Simplex:
    def __init__(self, objetivo):
        self.objetivo = [1] + objetivo
        self.linhas = []
        self.const = []

    def restricao(self, equacao, limite):
        self.linhas.append([0] + equacao)
        self.const.append(limite)

    def coluna_pivo(self):
        menor_indice = -1
        pos = 0
        for i in range(1, len(self.objetivo) - 1):
            if self.objetivo[i] < self.objetivo[menor_indice]:
                menor_indice = i
        if self.objetivo[menor_indice] >= 0:
            return -1
        return menor_indice

    def linha_pivo(self, coluna):
        col_const = [i[-1] for i in self.linhas]
        col_pivo = [i[coluna] for i in self.linhas]

        fracoes = []
        for i in range(len(col_const)):
            if col_pivo[i] <= 0:
                fracoes.append(np.inf)
            else:
                fracoes.append(col_const[i] / col_pivo[i])
        return np.argmin(fracoes)

    def imprime(self):
        print('\n', np.matrix([self.objetivo] + self.linhas))
        print('\n', 'O valor de Z até agora é', self.objetivo[-1])

    def pivo(self, linha, coluna):
        elemento_pivo = self.linhas[linha][coluna]
        self.linhas[linha] = [x / elemento_pivo for x in self.linhas[linha]]
        for cada_linha in range(len(self.linhas)):
            if cada_linha != linha:
                multiplicador = self.linhas[cada_linha][coluna]
                self.linhas[cada_linha] = [x - multiplicador * self.linhas[linha][idx] for idx, x in enumerate(self.linhas[cada_linha])]
        self.objetivo = [x - self.objetivo[coluna] * self.linhas[linha][idx] for idx, x in enumerate(self.objetivo)]


    def verifica_maximizacao(self):
        return min(self.objetivo) >= 0

    def solucao(self):
        for i in range(len(self.linhas)):
            self.objetivo += [0]
            variaveis_basicas = [0 for _ in range(len(self.linhas))]
            variaveis_basicas[i] = 1
            self.linhas[i] += variaveis_basicas + [self.const[i]]
            self.linhas[i] = np.array(self.linhas[i])
        self.objetivo = np.array(self.objetivo + [0])

        self.imprime()
        while True:
            c = self.coluna_pivo()
            if c == -1:
                print('\n', 'Solução ótima encontrada.')
                self.imprime_variaveis()
                break
            r = self.linha_pivo(c)
            self.pivo(r, c)
            self.imprime()

    def imprime_variaveis(self):
        variaveis = [0] * (len(self.linhas[0]) - 2)
        for i in range(len(self.linhas)):
            variavel = self.linhas[i][-1]
            for j in range(len(variaveis)):
                variaveis[j] += variavel * self.linhas[i][j + 1]
        print('\n', 'Valores das variáveis de decisão:')
        for i, var in enumerate(variaveis):
            print(f'x{i+1}: {var}')



if __name__ == '__main__':
    """
    max Z = x1 + x2 + x3
    x1 + x2 <= 4
    x1 - x2 <= 2
    x1,x2 >= 0
    """

    t = Simplex([-3, -2])
    t.restricao([1, 1], 4)
    t.restricao([1, -1], 2)
    t.solucao()
