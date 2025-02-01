import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import LabelEncoder

# Caminho da pasta onde estão os arquivos consolidados
PASTA_CONSOLIDADOS = "teste_geral/consolidados"

# Arquivos de dados e gabaritos
arquivo_dados = os.path.join(PASTA_CONSOLIDADOS, "consolidado_2021_2022.csv")
arquivo_gabarito = os.path.join(PASTA_CONSOLIDADOS, "consolidado_gabarito_2021_2022.csv")

# Carregar os dados
df_dados = pd.read_csv(arquivo_dados)
df_gabarito = pd.read_csv(arquivo_gabarito)

# Garantir que a coluna DateTime Stamp seja usada para alinhamento dos datasets
df_dados.set_index("DateTime Stamp", inplace=True)
df_gabarito.set_index("DateTime Stamp", inplace=True)

# Unir os datasets usando o índice (DateTime Stamp)
df = df_dados.join(df_gabarito, how="inner")

# Separar features (indicadores técnicos) e rótulo (CALL/PUT)
X = df.drop(columns=["template"])  # Remover a coluna de saída
y = df["template"]

# Converter CALL/PUT para valores numéricos
encoder = LabelEncoder()
y = encoder.fit_transform(y)  # CALL -> 0, PUT -> 1

# Criar o modelo Random Forest
modelo = RandomForestClassifier(n_estimators=100, random_state=42)

# Aplicar Cross-Validation (StratifiedKFold para manter equilíbrio entre classes)
kf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = cross_val_score(modelo, X, y, cv=kf, scoring="accuracy")

# Exibir os resultados
print(f"Acurácia média da validação cruzada: {np.mean(scores):.4f}")
print(f"Desvio padrão: {np.std(scores):.4f}")
