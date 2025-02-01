import os
import csv

# Definição das pastas e arquivos de saída
DADOS_DIR = "dad_apr_maq"
OUTPUT_DIR = "consolidados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cabeçalho do CSV final
header = ["DateTime Stamp", "sma2", "sma3", "sma4", "sma5", "rsi2", "rsi3", "rsi4", "rsi5"]

# Dicionários para armazenar os dados
dados_2021_2022 = {}  # Para consolidar os anos de 2021 e 2022
dados_2023 = {}        # Para consolidar o ano de 2023

# Percorre as pastas "sma" e "rsi" dentro de "dad_apr_maq"
for main_folder in os.listdir(DADOS_DIR):
    main_folder_path = os.path.join(DADOS_DIR, main_folder)

    if not os.path.isdir(main_folder_path):
        continue  # Ignora arquivos que não são pastas

    # Percorre as subpastas dentro de "sma" e "rsi" (ex: "sma_2", "rsi_3", etc.)
    for subfolder in os.listdir(main_folder_path):
        subfolder_path = os.path.join(main_folder_path, subfolder)

        if not os.path.isdir(subfolder_path):
            continue  # Ignora arquivos que não são pastas

        # Verifica se o nome da subpasta está no formato correto
        parts = subfolder.split("_")
        if len(parts) < 2:
            print(f"Ignorando pasta com nome inesperado: {subfolder}")
            continue

        indicador, periodo = parts[0], parts[1]  # Exemplo: "sma_2" -> indicador="sma", periodo="2"
        coluna_nome = f"{indicador}{periodo}"  # Exemplo: "sma2"

        # Percorre os arquivos dentro da subpasta
        for filename in os.listdir(subfolder_path):
            if not filename.endswith(".csv"):
                continue

            file_path = os.path.join(subfolder_path, filename)

            # Determina para qual dicionário os dados devem ir
            if "2021" in filename or "2022" in filename:
                target_dict = dados_2021_2022
            elif "2023" in filename:
                target_dict = dados_2023
            else:
                continue  # Ignora arquivos que não pertencem a esses anos

            # Lê o arquivo CSV
            with open(file_path, mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=";")
                for row in reader:
                    if len(row) < 2:
                        continue  # Ignora linhas inválidas

                    timestamp, ma_value = row[0], row[1].strip()
                    if ma_value == "":
                        ma_value = None  # Mantém vazio se não houver valor

                    # Adiciona ao dicionário correspondente
                    if timestamp not in target_dict:
                        target_dict[timestamp] = {col: "" for col in header[1:]}  # Inicializa com valores vazios

                    target_dict[timestamp][coluna_nome] = ma_value

# Função para salvar os dados consolidados
def salvar_csv(dados, output_file):
    sorted_keys = sorted(dados.keys())  # Ordena os timestamps
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Escreve o cabeçalho

        for timestamp in sorted_keys:
            row = [timestamp] + [dados[timestamp][col] for col in header[1:]]
            writer.writerow(row)

# Salvar os arquivos finais
salvar_csv(dados_2021_2022, os.path.join(OUTPUT_DIR, "2021_2022.csv"))
salvar_csv(dados_2023, os.path.join(OUTPUT_DIR, "2023.csv"))

print("Arquivos consolidados salvos em 'consolidados/'")
