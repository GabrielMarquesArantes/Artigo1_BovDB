import os
import csv

# Definição das pastas e arquivos de saída
GABARITO_DIR = "gabaritos"
OUTPUT_DIR = "consolidados"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Dicionários para armazenar os dados
dados_2021_2022 = {}
dados_2023 = {}

# Percorre os arquivos dentro da pasta "gabarito"
for filename in os.listdir(GABARITO_DIR):
    if not filename.endswith(".csv"):
        continue  # Ignora arquivos que não sejam CSV

    file_path = os.path.join(GABARITO_DIR, filename)

    # Determina para qual dicionário os dados devem ir
    if "2021" in filename or "2022" in filename:
        target_dict = dados_2021_2022
    elif "2023" in filename:
        target_dict = dados_2023
    else:
        continue  # Ignora arquivos fora do período desejado

    # Lê o arquivo CSV e adiciona ao dicionário correspondente
    with open(file_path, mode="r", newline="") as file:
        reader = csv.reader(file, delimiter=";")
        for row in reader:
            if len(row) < 2:
                continue  # Ignora linhas inválidas

            timestamp, template = row[0], row[1].strip()
            target_dict[timestamp] = template  # Adiciona ao dicionário

# Função para salvar os arquivos consolidados
def salvar_csv(dados, output_file):
    sorted_keys = sorted(dados.keys())  # Ordena os timestamps
    with open(output_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["DateTime Stamp", "Template"])  # Escreve o cabeçalho

        for timestamp in sorted_keys:
            writer.writerow([timestamp, dados[timestamp]])

# Salvar os arquivos finais
salvar_csv(dados_2021_2022, os.path.join(OUTPUT_DIR, "gabarito_2021_2022.csv"))
salvar_csv(dados_2023, os.path.join(OUTPUT_DIR, "gabarito_2023.csv"))

print("Arquivos de gabarito consolidados salvos em 'consolidados/'")
