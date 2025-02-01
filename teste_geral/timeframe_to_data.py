from datetime import datetime, timedelta

def timeframe_to_date(timeframe, epoch_start="1970-01-01"):
    """
    Converte um timeframe (segundos ou milissegundos desde uma época específica) em uma data real.
    
    Parâmetros:
        - timeframe (int ou float): O valor do timeframe a ser convertido.
        - epoch_start (str): Data inicial no formato "YYYY-MM-DD" (padrão: "1970-01-01").
        
    Retorna:
        - Uma string formatada como "dia/mês/ano, hora:minuto:segundo".
    """
    try:
        # Garantir que timeframe seja interpretado como segundos (divida por 1000 se for milissegundos)
        if timeframe > 10**10:  # Provável que seja em milissegundos
            timeframe = timeframe / 1000
        
        # Converter a data inicial da época em um objeto datetime
        epoch = datetime.strptime(epoch_start, "%Y-%m-%d")
        
        # Adicionar o timeframe à época para obter a data real
        real_date = epoch + timedelta(seconds=timeframe)
        
        # Formatar a data como "dia/mês/ano, hora:minuto:segundo"
        return real_date.strftime("%d/%m/%Y, %H:%M:%S")
    
    except Exception as e:
        return f"Erro ao converter timeframe: {e}"

# Exemplo de uso
timeframe = 1659918000  # Exemplo em segundos desde 1970-01-01
print(timeframe_to_date(timeframe))

# 1732192800 ultimo começo 1732 21/11/2024, 12:40:00
# 1730110800 último começo 1730 28/10/2024, 10:20:00
# 1729698000 primeiro começo 1729 23/10/2024, 15:40:00
# 1670299200 ultimo começo 1670 06/12/2022, 04:00:00
# 1669886400 primeiro começo 1669 01/12/2022, 09:20:00
# 1659918000 ultimo começo 1659 08/08/2022, 00:20:00
# 1659625200 primeiro começo 1659 04/08/2022, 15:00:00

# 1659625200 primeiro começo 1659 04/08/2022, 15:00:00
# 1732312800 último começo 1732 23/11/2024, 12:40:00