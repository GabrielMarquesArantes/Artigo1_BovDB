import csv
import os
from tabulate import tabulate

# Funções de análise para os diferentes métodos de média móvel
def calculate_sma(velas, n):
    sma = []
    for i in range(n, len(velas)):
        close_prices = [float(vela[4]) for vela in velas[i - n:i]]
        sma_value = sum(close_prices) / n
        sma.append(sma_value)
    return sma

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

# Função RSI ajustada
def calculate_rsi(velas, n):
    rsi = []
    gains = [0]
    losses = [0]
    for i in range(1, len(velas)):
        change = float(velas[i][4]) - float(velas[i - 1][4])
        gains.append(max(0, change))
        losses.append(abs(min(0, change)))
    avg_gain = sum(gains[:n]) / n
    avg_loss = sum(losses[:n]) / n
    rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
    rsi.append(100 - (100 / (1 + rs)))

    for i in range(n, len(velas)):
        avg_gain = (avg_gain * (n - 1) + gains[i]) / n
        avg_loss = (avg_loss * (n - 1) + losses[i]) / n
        rs = avg_gain / avg_loss if avg_loss != 0 else float('inf')
        rsi_value = 100 - (100 / (1 + rs))
        rsi.append(rsi_value)
    return rsi

# Função para gerar os CSVs com os valores de ma_value
def generate_ma_csv(file_path, ma_function, ma_period, output_folder):
    with open(file_path, mode='r') as file:
        reader = csv.reader(file, delimiter=';')
        velas = list(reader)

    if len(velas) < ma_period:
        print(f"Dados insuficientes para análise no arquivo {file_path}.")
        return

    ma_values = ma_function(velas, ma_period)
    output_file_name = f"{os.path.splitext(os.path.basename(file_path))[0]}_{ma_function.__name__}_{ma_period}.csv"
    output_file_path = os.path.join(output_folder, output_file_name)

    os.makedirs(output_folder, exist_ok=True)
    with open(output_file_path, mode='w', newline='') as output_file:
        writer = csv.writer(output_file, delimiter=';')
        writer.writerow(["DateTime Stamp", "MA Value"])

        last_valid_value = None  # Para armazenar o último valor válido de ma_value

        for i in range(len(velas)):
            try:
                ma_value = ma_values[i - ma_period] if i >= ma_period else ""
                last_valid_value = ma_value if ma_value != "" else last_valid_value
                writer.writerow([velas[i][0], ma_value])
            except IndexError:
                # Caso aconteça um erro, use o último valor válido ou deixe em branco
                writer.writerow([velas[i][0], last_valid_value if last_valid_value is not None else ""])

    print(f"Arquivo gerado: {output_file_path}")

# Configurações
DATA_FOLDER = "./data_tests"
OUTPUT_FOLDER = "./dad_apr_maq"
ma_type = input("Escolha o tipo de média móvel (SMA, WMA, EMA, RSI): ").upper()

if ma_type == "SMA":
    ma_function = calculate_sma
elif ma_type == "WMA":
    ma_function = calculate_wma
elif ma_type == "EMA":
    ma_function = calculate_ema
elif ma_type == "RSI":
    ma_function = calculate_rsi
else:
    print("Tipo de média móvel inválido. Utilizando SMA por padrão.")
    ma_function = calculate_sma

ma_period = int(input("Informe o período da média móvel: "))

# Processar todos os arquivos CSV na pasta
for file_name in os.listdir(DATA_FOLDER):
    if file_name.endswith(".csv"):
        file_path = os.path.join(DATA_FOLDER, file_name)
        generate_ma_csv(file_path, ma_function, ma_period, OUTPUT_FOLDER)