def calculate_order(value):
    count = 0;
    
    while(value < 1 and value != 0):
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

data = [(0, 12), (1.5, 3), (4, -5), (5.87, -4), (9, 10), (10.45, 5), (11, 8), (13, -2), 
    (16, -4), (17, -3), (19.23, 6), (22, 7), (24.67, 3), (26, -1), (27, 2), (28, 8), 
    (29, 20), (34.67, -6), (35, 5), (38, -8), (41, 10), (42, 16), (43, -6), (46, -5), 
    (48, 12), (49, 8), (52, 9), (55, 32), (56, -16), (57, -19), (58, -20), 
    (62, 12)]

print(min_interval_x(data));