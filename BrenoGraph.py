#
#
#
# Projeto desenvolvido para Disciplina de Computação Gráfica (2022.2)
# Aluno: Breno Gabriel de Souza Coelho
# 
# Gerador de Gráficos com base num arquivo Excel
# (última modificação: 18.05.2023)
#

import pandas;
from BuildGraph import *;

def values_are_numeric(list):
    for each in list:
        if not isinstance(each[1], int):
            return False;
    return True;

def merge(list1, list2):
    resultado = [];

    #Isso é um improviso. Por algum motivo, se não tiver um dado com x <= 0, o gráfico fica errado
    #if (list1[0][1] > 0) : resultado.append((0,0)) 

    for i in range(0, len(list1)):
        resultado.append((list1[i][1], list2[i][1]));

    return resultado;

def graphExcel(arquivo_excel, arquivo_saida):
    dados_excel = pandas.read_excel(arquivo_excel);
    dict_dados = dados_excel.to_dict();
    dados_entrada = [];

    count = 0;
    for column in dict_dados: 
        dados_entrada.append([]);

        for line_index in dict_dados[column]:
            dados_entrada[count].append((line_index, dict_dados[column][line_index]));

        count += 1;

    if len(dados_entrada[0]) != len(dados_entrada[1]):
        quit(105);

    if (values_are_numeric(dados_entrada[0])):
        dados_entrada = merge(dados_entrada[0], dados_entrada[1])

    print(dados_entrada);
    buildGraph(arquivo_saida, dados_entrada);

graphExcel("censo_petrolina.xlsx", "grafico_petrolina.html");
graphExcel("censo_juazeiro.xlsx", "grafico_juazeiro.html");