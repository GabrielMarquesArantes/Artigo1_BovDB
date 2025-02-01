import csv
import os
import random
from tabulate import tabulate

# Funções de análise para os diferentes métodos de média móvel e RSI
def calculate_sma(velas, n):
    sma = []
    for i in range(n, len(velas)):
        close_prices = [float(vela[4]) for vela in velas[i - n:i]]  # Índice 4 para 'Bar CLOSE Bid Quote'
        sma_value = sum(close_prices) / n
        sma.append(sma_value)
    return sma

def calculate_rsi(velas, n):
    rsi = []
    for i in range(n, len(velas)):
        gains = []
        losses = []
        close_prices = [float(vela[4]) for vela in velas[i - n:i + 1]]
        for j in range(1, len(close_prices)):
            change = close_prices[j] - close_prices[j - 1]
            if change > 0:
                gains.append(change)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(change))
        
        avg_gain = sum(gains) / n
        avg_loss = sum(losses) / n
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        rsi_value = 100 - (100 / (1 + rs))
        rsi.append(rsi_value)
    return rsi

def calculate_wma(velas, n):
    wma = []
    weights = list(range(1, n + 1))
    for i in range(n, len(velas)):
        close_prices = [float(vela[4]) for vela in velas[i - n:i]]
        wma_value = sum(w * close for w, close in zip(weights, close_prices)) / sum(weights)
        wma.append(wma_value)
    return wma

def calculate_ema(velas, n):
    ema = []
    alpha = 2 / (n + 1)
    ema_value = sum(float(vela[4]) for vela in velas[:n]) / n
    for i in range(n, len(velas)):
        ema_value = alpha * float(velas[i][4]) + (1 - alpha) * ema_value
        ema.append(ema_value)
    return ema

def calculate_pma(velas, n):
    pma = []
    for i in range(n, len(velas)):
        close_prices = [float(vela[4]) for vela in velas[i - n:i]]
        pma_value = sum(p * close for p, close in zip(range(1, n + 1), close_prices)) / sum(range(1, n + 1))
        pma.append(pma_value)
    return pma

def calculate_hma(velas, n):
    hma = []
    weights = [2 / i for i in range(1, n + 1)]
    weights_sum = sum(weights)
    for i in range(n, len(velas)):
        close_prices = [float(vela[4]) for vela in velas[i - n:i]]
        hma_value = weights_sum / sum(w / close for w, close in zip(weights, close_prices))
        hma.append(hma_value)
    return hma

def calculate_random(velas, n):
    random_trends = []
    for _ in range(n, len(velas)):
        random_trend = random.choice(['CALL', 'PUT'])
        random_trends.append(random_trend)
    return random_trends

# Função para realizar a análise com base no arquivo CSV
def analyze_csv_file(file_path, ma_function, ma_period):
    print(f"Analisando o arquivo: {file_path}")
    with open(file_path, mode='r') as file:
        reader = csv.reader(file, delimiter=';')  # Atualizado para separador ponto e vírgula
        velas = list(reader)

    if len(velas) < ma_period:
        print("Dados insuficientes para análise.")
        return None

    ma_values = ma_function(velas, ma_period)
    win, loss = 0, 0

    for i in range(len(ma_values) - 1):
        current_close = float(velas[i + len(velas) - len(ma_values)][4])
        next_close = float(velas[i + len(velas) - len(ma_values) + 1][4])

        if isinstance(ma_values[i], float):
            ma_value = ma_values[i]
            trend = 'CALL' if current_close > ma_value else 'PUT'
        else:
            trend = ma_values[i]

        if (trend == 'CALL' and next_close > current_close) or (trend == 'PUT' and next_close < current_close):
            win += 1
        else:
            loss += 1

    assertividade = round(win / (win + loss) * 100, 2) if win + loss > 0 else 0
    return win, loss, assertividade

# Configurações
DATA_FOLDER = "./data_tests"
ma_type = input("Escolha o tipo de média móvel (SMA, WMA, EMA, PMA, HMA, RSI, RANDOM): ").upper()

if ma_type == "SMA":
    ma_function = calculate_sma
elif ma_type == "WMA":
    ma_function = calculate_wma
elif ma_type == "EMA":
    ma_function = calculate_ema
elif ma_type == "PMA":
    ma_function = calculate_pma
elif ma_type == "HMA":
    ma_function = calculate_hma
elif ma_type == "RSI":
    ma_function = calculate_rsi
elif ma_type == "RANDOM":
    ma_function = calculate_random
else:
    print("Tipo de média móvel inválido. Utilizando SMA por padrão.")
    ma_function = calculate_sma

ma_period = int(input("Informe o período da análise: "))

# Processar todos os arquivos CSV na pasta
all_results = []
for file_name in os.listdir(DATA_FOLDER):
    if file_name.endswith(".csv"):
        file_path = os.path.join(DATA_FOLDER, file_name)
        result = analyze_csv_file(file_path, ma_function, ma_period)
        if result:
            win, loss, assertividade = result
            all_results.append([file_name.replace("_historico.csv", ""), win, loss, assertividade])

# Exibir os resultados
print(tabulate(all_results, headers=['PAR', 'WINS', 'LOSS', 'ASSERTIVIDADE']))
