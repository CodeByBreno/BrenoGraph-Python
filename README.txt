# Projeto desenvolvido para Disciplina de Computação Gráfica (2022.2)
# Aluno: Breno Gabriel de Souza Coelho
# 
# Gerador de Gráficos com base num arquivo Excel
# (última modificação: 18.05.2023)
#

=================================== Explicando o que eu fiz:

Eu criei um script em Python que constroí o gráfico em SVG ao escrever
num arquivo alvo uma linha que tem a estrutura/formato do SVG. Por exemplo,

def desenhaCirculo(self, x, y, radius, color=None, border_color = "black", border_width=1):
   self.file.write('<circle cx="' + str(x) + '" cy="' + str(y) + '"r="' + str(radius) + '"style="fill:'
                  + color + '; stroke:' + border_color + '; stroke-width:' + str(border_width) + 'px"/>\n')

O método acima, da classe JanelaGraficoSVG, escreve no arquivo informado
no construtor da classe uma linha "<circle cx=5 cy=6 ..." por exemplo,
que compõe um circulo no SVG. A classe informada possui uma série de
métodos que escrevem no arquivo alvo linhas em SVG, no final, eu utilizo
esses métodos para construir o gráfico a partir de um conjunto de dados

Esse script automatizado, portanto, permite compor um gráfico a partir
de uma base de dados extraída do excel ou informada por parâmetro. 

No arquivo BrenoGraph.py, eu uso a função "graphExcel(arquivo_excel, arquivo_saida)"
para formar o gráfico a partir de um arquivo excel informado. No arquivo
"buildGraph.py" eu faço alguns exemplos de criação de gráfico passando uma lista
de dados, como abaixo:

buildGraph('teste3.html', [(0, 5), (2, 12), (6, -4), (12, -10)]);

Ambos os códigos criam um arquivo .html de saida com o gráfico dos dados passados.
Em particular, coloquei dois arquivos Excel com as informações do censo de 
petrolina e juazeiro, e cada um gera um .html com seu respectivo gráfico.

================================ Para executar, basta fazer:

"python BrenoGraph.py"

no prompt de comandos.
Lá eu já coloquei as linhas 

graphExcel("censo_petrolina.xlsx", "grafico_petrolina.html");
graphExcel("censo_juazeiro.xlsx", "grafico_juazeiro.html");

Que criam os arquivos html com os gráficos. Ao fazer isso, também serão criados
3 arquivos de teste com gráficos criados a partir de outros dados


================================ Observações:

Infelizmente, devido à algum bug inesperado, o gráfico de petrolina ficou um pouco
mais baixo do que o esperado. 
Além disso, foi necessário criar um ponto extra em ambos os gráficos das populações,
(0,1), para que ele fosse gerado de maneira adequada. Não tenho certeza do porque isso
ocorreu, mas acredito que o projeto já realiza o solicitado
