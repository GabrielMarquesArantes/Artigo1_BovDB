from iqoptionapi.stable_api import IQ_Option
import time
import csv
import os

def connect_to_iq_option(email, senha):
    """
    Conecta à IQ Option usando as credenciais fornecidas.

    Args:
        email: O email da conta na IQ Option.
        senha: A senha da conta na IQ Option.

    Returns:
        API: Objeto conectado à API da IQ Option.
    """
    print("Conectando à IQ Option...")
    API = IQ_Option(email, senha)
    API.connect()

    if API.check_connect():
        print("Conexão bem-sucedida!")
        return API
    else:
        print("Erro ao conectar. Verifique suas credenciais.")
        exit()

def save_historical_data(API, par, timeframe, total_candles, output_dir):
    """
    Salva dados históricos de velas em um arquivo CSV.

    Args:
        API: Instância conectada da IQ Option API.
        par: Par de ativos, ex.: 'EURUSD'.
        timeframe: Tempo das velas em segundos (1m = 60, 5m = 300, etc.).
        total_candles: Total de velas desejadas.
        output_dir: Diretório onde os arquivos CSV serão salvos.
    """
    batch_size = 1000  # Máximo permitido pela IQ Option API
    data = []  # Lista para armazenar todas as velas
    endtime = time.time()  # Começa pelo horário atual

    print(f"Coletando dados históricos para {par}...")

    for i in range(0, total_candles, batch_size):
        try:
            velas = API.get_candles(par, timeframe, batch_size, endtime=endtime)
            if not velas:
                break  # Se não houver mais velas disponíveis, interrompe
            data.extend(velas)  # Adiciona as velas à lista
            endtime = velas[0]['from'] - 1  # Define o próximo fim como o início da última vela coletada
        except Exception as e:
            print(f"Erro ao coletar dados para {par}: {e}")
            break

    # Ordena os dados por timestamp
    data.sort(key=lambda x: x['from'])

    # Salva os dados em um arquivo CSV
    file_name = f"{output_dir}/{par}_historico.csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Cabeçalhos do CSV
        writer.writerow(['from', 'to', 'open', 'close', 'min', 'max', 'volume'])
        for vela in data:
            writer.writerow([
                vela['from'], vela['to'], vela['open'],
                vela['close'], vela['min'], vela['max'], vela['volume']
            ])

    print(f"Dados salvos para {par} em {file_name}")

# Credenciais
EMAIL = "3gma26062004@gmail.com"  # Substitua pelo seu email
SENHA = "teste123"              # Substitua pela sua senha

# Conectar à IQ Option
API = connect_to_iq_option(EMAIL, SENHA)

# Configurações para a coleta de dados
TIMEFRAME = 120  # Timeframe das velas (em segundos, 60 = 1 minuto)
TOTAL_CANDLES = 43200  # Número total de velas desejadas
OUTPUT_DIR = "./dados_historicos_60"  # Diretório onde os arquivos CSV serão salvos

# Criar o diretório se ele não existir
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

# Lista de pares de moedas para coletar (especificados manualmente)
pares_selecionados = [
    "AUDCAD", "AUDUSD", "AUDJPY", "EURUSD", "EURJPY", "GBPJPY", "GBPUSD", "USDCHF", "USDCAD", "EURGBP"
]  # Adicione os pares desejados aqui

print(f"Pares selecionados para coleta: {pares_selecionados}")

# Coletar e salvar dados para cada par
for par in pares_selecionados:
    save_historical_data(API, par, TIMEFRAME, TOTAL_CANDLES, OUTPUT_DIR)