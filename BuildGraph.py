def positive(value):
    if value < 0:
        return -1*value;
    else:
        return value;

def calculate_order(value):
    count = 0;

    while(value < 1 and value != 0 and value > 0):
        print(value);
        value *= 10;
        count += 1;
    
    return count;

def min_interval_x(data):
    #Coloca para calcular a menor distancia entre dois 'x' sucessivos e 
    #usa isso como base para determinar bar_width
    N = len(data);
    interval = data[N-1][0] - data[0][0];

    for i in range(1, len(data)):
        if (data[i][0] - data[i-1][0]) < interval:
            interval = data[i][0] - data[i-1][0];
    
    return interval, calculate_order(interval);

class JanelaGraficoSVG():

    def __init__(self, namefile, arguments):
        self.file = open(namefile, "w");
        self.dx = 0;
        self.dy = 0;
        self.x0 = 0;
        self.y0 = 0;
        
        #Gerar file como html ou svg puro?
        if "html" in arguments: self.html = True;
        else: self.html: False;
        if self.html:
            self.initiate_html();
            self.file = open(namefile, "a");

        #Tipo do Gráfico:
        if "graph_type" in arguments: self.graph_type = arguments["graph_type"];
        else: self.graph_type = "line";

        #Dimensionamento padrão
        if "width" in arguments: self.width = arguments["width"];
        else: self.width = 0;
        if "height" in arguments: self.height = arguments["height"];
        else: self.height = 0;
        if "font_size" in arguments: self.font_size = arguments["font_size"];
        else: self.font_size = 20;

        self.safety_margin = self.width//50;

        #Paddings da tela - o traceback fica de fora
        if "padding" in arguments:
            self.padding_left = arguments["padding"];
            self.padding_bottom = arguments["padding"];
            self.padding_top = arguments["padding"];
            self.padding_right = arguments["padding"];
        else:
            if "padding_left" in arguments: self.padding_left = arguments["padding_left"];
            else: self.padding_left = 0;
            if "padding_bottom" in arguments: self.padding_bottom = arguments["padding_bottom"];
            else: self.padding_bottom = 0;
            if "padding_top" in arguments: self.padding_top = arguments["padding_top"];
            else: self.padding_top = 0;
            if "padding_right" in arguments: self.padding_right = arguments["padding_right"];
            else: self.padding_right = 0;

        #Larguras
        if "main_line_width" in arguments: self.main_line_width = arguments["main_line_width"];
        else: self.main_line_width = 2;
        if "point_radius" in arguments: self.point_radius = arguments["point_radius"];
        else: self.point_radius = 10;
        if "point_border_width" in arguments: self.point_border_width = arguments["point_border_width"];
        else: self.point_border_width = 0;

        if "bar_width" in arguments: self.bar_width = arguments["bar_width"];
        else: self.bar_width = None;
        if "bar_border_width" in arguments: self.bar_border_width = arguments["bar_border_width"];
        else: self.bar_border_width = 0;

        #Cores
        if "line_color" in arguments: self.main_line_color = arguments["line_color"];
        else: self.main_line_color = 0;
        if "background_color" in arguments: self.background_color = arguments["background_color"];
        else: self.background_color = "lightgrey";
        if "point_color" in arguments: self.point_color = arguments["point_color"];
        else: self.point_color = "lightblue";
        if "point_border_color" in arguments: self.point_border_color = arguments["point_border_color"];
        else: self.point_border_color = "blue";
        if "graph_line_color" in arguments: self.graph_line_color = arguments["graph_line_color"];
        else: self.graph_line_color = "black";
        if "support_line_color" in arguments: self.support_line_color = arguments["support_line_color"];
        else: self.support_line_color = "lightgray";

        if "bar_color" in arguments: self.bar_color = arguments["bar_color"];
        else: self.bar_color = ["#86c5ff", "green"];
        if "bar_border_color" in arguments: self.bar_border_color = arguments["bar_border_color"];
        else: self.bar_border_color = "None";
    
        #background-color: #68FFEF;padding-top: 10px;padding-left: 10px;padding-bottom:  10px;padding-right: 10px;
        self.file.write('<svg xmls="http://www.w3.org/2000/svg" width="' + str(self.width + self.point_radius) + '" height="' 
                        + str(self.height + self.point_radius) + '" viewBox=" 0 0 ' + str(self.width + self.point_radius) + ' ' + str(self.height + self.point_radius)
                        + '" style="background-color: ' + self.background_color + '; padding-top: ' + str(self.padding_top) + 'px; padding-left: ' + str(self.padding_left) 
                        + 'px; padding-bottom:' + str(self.padding_bottom) + 'px; padding-right:' + str(self.padding_right) + 'px;" >\n');

        if "debug" in arguments: self.debug = arguments["debug"];
        else: self.debug = "True";

        if "titulo" in arguments: self.titulo_principal = arguments["titulo"];
        else: self.titulo_principal = "sem titulo";

    def debbuger(self, data):
        N = len(data);
        big_y, low_y = big_low_y(data);

        print("Dimensoes da Tela: " + str(self.width) + "x" + str(self.height));
        print("Origem do Sistema: [" + str(self.x0) + "," + str(self.y0) + "]");
        print("Escala de x: ", str(self.dx));
        print("Escala de y: ", str(self.dy));
        print("Tamanho total ocupado por x: ", str(self.dx*N));
        print("Tamanho total ocupado por y: ", str(self.dy*N));
        print("Intervalo de variacao de x: [" + str(data[0][0]) + "," + str(data[N-1][0]) + "]");
        print("Intervalo de variacao de y: [" + str(low_y) + "," + str(big_y) + "]");
    
    def desenhaLinha(self, x0, y0, x1, y1, line_stroke = None, line_color = None):
        if line_stroke == None: line_stroke = self.main_line_width;
        if line_color == None: line_color = self.main_line_color;

        self.file.write('<line x1="' + str(x0) + '" y1="' + str(y0) + '" x2="' + str(x1) + '" y2="' + str(y1) + '" style="stroke:' + line_color+ '; stroke-width:' + str(line_stroke) + 'px"/>\n')
    
    def desenhaRetangulo(self, x, y, width, height, args = {}):
        if "color" not in args: args["color"] = 'None';
        if "border" not in args: args["border"] = 'None';
        if "border_width" not in args: args["border_width"] = 0;
        self.file.write('<rect x="' + str(x) + '" y="' + str(y) + '" width="' + str(width) + '" height="' + str(height) + '" style="fill:' + args["color"] + '; stroke:' + args["border"] + '; stroke-width:' + str(args["border_width"]) + 'px"/>\n')

    def desenhaCirculo(self, x, y, radius, color=None, border_color = "black", border_width=1):
        self.file.write('<circle cx="' + str(x) + '" cy="' + str(y) + '"r="' + str(radius) + '"style="fill:'
                        + color + '; stroke:' + border_color + '; stroke-width:' + str(border_width) + 'px"/>\n')

    def escreveTexto(self, x, y, texto, font_family = "Arial", font_size = 24, font_background_color="black"):
        self.file.write('<text x="' + str(x) + '" y="' + str(y) + '" font-family="' + 
                        font_family + '" font-size="' + str(font_size) + '" fill="' + font_background_color + '">' + texto + '</text>')

    def calculaEscala(self, data, N, big_y, low_y):
        y_interval = big_y - low_y;
        self.dy = int((self.height - self.padding_top - self.padding_bottom)/y_interval);

        x_interval = data[N-1][0] - data[0][0];
        self.dx = int((self.width - self.padding_left - self.padding_right)/x_interval);

    def calculaOrigem(self, data, low_y):
        self.x0 = positive(data[0][0]) * self.dx + self.padding_left; 
        self.y0 = self.height - self.padding_top - positive(low_y) * self.dy; 
    
    def desenhaEixos(self, data, N, big_y, low_y):
        extra_extension = self.safety_margin;

        if self.graph_type == "bar":
            #Aumentando um pouco a extensão dos eixos para compensar o tamanho da barra
            extra_extension += self.bar_width; 
        
        if self.graph_type == "line":
            #Compensando o pelo tamanho das bolinhas
            extra_extension += self.point_radius;

        #Desenha o Eixo X
        self.desenhaLinha(x0 = data[0][0]*self.dx + self.x0 - extra_extension,
                          y0 = self.y0,
                          x1 = data[N-1][0]*self.dx + self.x0 + extra_extension,
                          y1 = self.y0);
        
        #Desenha o Eixo Y
        self.desenhaLinha(x0 = self.x0,
                          y0 = self.y0 - big_y*self.dy - extra_extension,
                          x1 = self.x0,
                          y1 = self.y0 - low_y*self.dy + extra_extension);
    
    def drawGraphic(self, data):
        N = len(data);
        big_y, low_y = big_low_y(data);
        
        #Isso aqui é pra calcular um tamanho apropriado para as barras caso 
        #não tenha sido informado um default. 
        print("MENOR DISTANCIA EM X: " + str(min_interval_x(data)));
        if self.bar_width == None:
            self.bar_width = float(10*min_interval_x(data)[0]/0.323);
            
        self.calculaEscala(data, N, big_y, low_y);
        self.calculaOrigem(data, low_y);
    
        if self.graph_type == "line":
            for i in range(0, N):
                xi = data[i][0]*self.dx + self.x0;
                yi = self.y0 - data[i][1]*self.dy;

                print("Dado " + str(i) + "° : " + str(xi));
                print(xi);

                #Desenha uma reta de suporte, partindo da altura do ponto até o eixo das abcissas
                self.desenhaLinha(
                                x0 = xi,
                                y0 = self.y0,
                                x1 = xi,
                                y1 = yi,
                                line_color = self.support_line_color);

            self.desenhaEixos(data, N, big_y, low_y);

            for i in range(0, N):
                xi = data[i][0]*self.dx + self.x0;
                yi = self.y0 - data[i][1]*self.dy;

                if i > 0:
                    x0_anterior = data[i-1][0]*self.dx + self.x0;
                    y0_anterior = self.y0 - data[i-1][1]*self.dy;

                    #Desenha uma linha conectando o ponto atual ao anterior
                    self.desenhaLinha(x0 = x0_anterior,
                                    y0 = y0_anterior,
                                    x1 = xi,
                                    y1 = yi,
                                    line_color = self.graph_line_color);

                    #Desenha a bolinha referente ao ponto
                    self.desenhaCirculo(x = x0_anterior,
                                        y = y0_anterior,
                                        radius = self.point_radius,
                                        color = self.point_color,
                                        border_color= self.point_border_color,
                                        border_width = self.point_border_width);
        
                    self.escreveTexto(x = x0_anterior, 
                                      y = y0_anterior, 
                                      texto = str(data[i-1][1]), 
                                      font_size= self.font_size);

            #Última bolinha (para garantir que ela seja sempre desenhada por cima da linha)
            self.desenhaCirculo(x = xi,
                                y = yi,
                                radius = self.point_radius,
                                color = self.point_color,
                                border_color= self.point_border_color,
                                border_width = self.point_border_width);

            self.escreveTexto(  x = xi, 
                                y = yi, 
                                texto = str(data[i][1]), 
                                font_size= self.font_size);

            if self.debug == True:
                #Desenhando a origem (por motivos de debug mesmo)
                self.desenhaCirculo(x = self.x0,
                                    y = self.y0,
                                    radius = self.point_radius,
                                    color = "#ff0f0f",
                                    border_color= self.point_border_color,
                                    border_width = self.point_border_width);

        if self.graph_type == "bar":
            N = len(data);

            for i in range(0, N):
                xi = data[i][0]*self.dx + self.x0;
                yi = self.y0 - data[i][1]*self.dy;
                qtd_colors = len(self.bar_color);
                text_y = str(data[i][1]);
                text_size = 4*len(text_y);
                
                if data[i][1] > 0:
                    self.desenhaRetangulo(
                        x = int(xi),
                        y = int(yi),
                        width = self.bar_width,
                        height = data[i][1]*self.dy,
                        args = {
                        "color": self.bar_color[i%qtd_colors],
                        "border" : self.bar_border_color,
                        "border_width" : self.bar_border_width 
                        },
                    )
                    
                    self.escreveTexto(x = xi + text_size//2, 
                                      y = yi - 10, 
                                      texto = text_y, 
                                      font_size= self.font_size);
                    
                else:
                    self.desenhaRetangulo(
                        x = int(xi),
                        y = self.y0,
                        width = self.bar_width,
                        height = -1*data[i][1]*self.dy,
                        args = {
                        "color": self.bar_color[i%qtd_colors],
                        "border" : self.bar_border_color,
                        "border_width" : self.bar_border_width 
                        },
                    )    
                    self.escreveTexto(x = xi + text_size//2, 
                                      y = self.y0 -1*data[i][1]*self.dy + 25, 
                                      texto = text_y, 
                                      font_size = self.font_size);

            self.desenhaEixos(data, N, big_y, low_y);                

        #Contorno do gráfico
        self.desenhaRetangulo(
                            x = 2, 
                            y = 2, 
                            width=self.width, 
                            height=self.height,
                            args=
                            {"color": "None",
                            "border" : "#BBBBBB",
                            "border_width" : 2});

        self.debbuger(data);
        
    def initiate_html(self):
        self.file.write('<html>\n<head>\n<title>BrenoGraph</title>\n</head>\n<body>');

    def endFile(self):
        self.file.write('</svg>');

        if (self.html):
            self.file.write("\n</body>\n</html>\n");

def big_low_y(data):
    if len(data) > 0:
        big_y = data[0][1];
        low_y = data[0][1];
    else:
        return (0,0);

    for each in data:
        if each[1] > big_y:
            big_y = each[1];
        if each[1] < low_y:
            low_y = each[1];

    return (big_y, low_y);

def buildGraph(namefile, data):

    window_width = 1200;
    window_height = 800;

    args = {
        "width" : window_width,
        "height" : window_height,
        "padding" : 50,
        "line_color": "#86c5ff",
        "background_color": "white",
        "point_color": "#38caf8",
        "main_line_width": 5,
        "graph_type": "line",
        "graph_line_color": "#86c5ff",
        "bar_color": ["#25d8ff", "#9cb5f6", "#c1a0ff", "#b2ffdc"],
        "html": True,
        "debug": True,
        "font_size": 20,
    }

    janela = JanelaGraficoSVG(namefile, args);

    janela.drawGraphic(data);

    janela.endFile();
        

buildGraph('teste1.html', [(0, 12), (1.5, 3), (4, -5), (5.87, -4), (9, 10), (10.45, 5), (11, 8), (13, -2), 
                               (16, -4), (17, -3), (19.23, 6), (22, 7), (24.67, 3), (26, -1), (27, 2), (28, 8), 
                               (29, 20), (34.67, -6), (35, 5), (38, -8), (41, 10), (42, 16), (43, -6), (46, -5), 
                               (48, 12), (49, 8), (52, 9), (55, 32), (56, -16), (57, -19), (58, -20), 
                               (62, 12)]);


buildGraph('teste2.html', [(-8,-20), (-7, -10),(-6, 10), (-5,2),(-4,-4),(-3,10),(-2,5),(-1,-8),(0,-2), 
                                (1,12), (2,-5), (3, -15), (4, -32), (5, -42)]);

buildGraph('teste3.html', [(0, 5), (2, 12), (6, -4), (12, -10)]);