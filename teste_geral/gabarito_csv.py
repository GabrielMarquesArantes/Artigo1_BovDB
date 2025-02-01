import csv
import os

# Função para criar a pasta de saída
def ensure_output_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

# Função para criar os CSVs de gabarito
def create_gabarito_csvs(input_folder, output_folder):
    # Garantir que a pasta de saída exista
    ensure_output_folder(output_folder)

    # Processar cada arquivo CSV na pasta de entrada
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".csv"):
            input_file_path = os.path.join(input_folder, file_name)

            # Gerar o nome do arquivo de saída
            base_name = file_name.replace("DAT_ASCII_", "").replace(".csv", "")
            output_file_name = f"{base_name.split('_')[0]}_GAB_{base_name.split('_')[2]}.csv"
            output_file_path = os.path.join(output_folder, output_file_name)

            with open(input_file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile:
                reader = csv.reader(infile, delimiter=';')
                writer = csv.writer(outfile, delimiter=';')

                # Preparar a lista de velas
                velas = list(reader)

                # Gerar o gabarito
                for i in range(len(velas) - 1):
                    current = velas[i]
                    next_ = velas[i + 1]

                    # Extrair valores relevantes
                    datetime_stamp = current[0]
                    current_close = float(current[4])
                    next_close = float(next_[4])

                    # Determinar a previsão correta
                    trend = 'CALL' if next_close > current_close else 'PUT'

                    # Escrever no novo arquivo CSV
                    writer.writerow([datetime_stamp, trend])

            print(f"Gabarito criado: {output_file_path}")

# Configuração das pastas
input_folder = "./data_tests"
output_folder = "./gabaritos"

# Criar os gabaritos
create_gabarito_csvs(input_folder, output_folder)
