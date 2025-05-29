import yfinance as yf
import pandas as pd
import sys
from datetime import datetime
import pytz

# Parâmetros
ticker = "PETR4.SA"
period = "10d"
interval = "1d"

# Coleta dos dados
data = yf.download(ticker, period=period, interval=interval)

# Verificações iniciais
if data.empty or len(data) < 5:
    print("Não há dados suficientes para análise.")
    sys.exit()

# Garantir datetime no índice
data.index = pd.to_datetime(data.index)

# Cálculo de médias móveis para tendência
data["EMA9"] = data["Close"].ewm(span=9).mean()
data["EMA21"] = data["Close"].ewm(span=21).mean()

# Verificar tendência com base nas médias móveis
if data["EMA9"].iloc[-1] > data["EMA21"].iloc[-1]:
    tendencia = "alta"
else:
    tendencia = "baixa"

print(f"\nTendência detectada com EMA: {tendencia.upper()}")

# Ajustar para fuso horário de Brasília
fuso_brasilia = pytz.timezone('America/Sao_Paulo')
agora_brasilia = datetime.now(fuso_brasilia)
hora_formatada = agora_brasilia.strftime("%Y-%m-%d %H:%M:%S")
data_formatada = agora_brasilia.strftime("%d/%m/%Y")

# Obter o preço atual do ativo via yfinance Ticker
ticker_info = yf.Ticker(ticker)
preco_atual = ticker_info.info.get('regularMarketPrice', None)

if preco_atual is not None:
    print(f"\nPreço atual do ativo {ticker}: {preco_atual}")
else:
    preco_atual = data['Close'].iloc[-1]
    print(f"\nPreço atual do ativo {ticker} (último fechamento): {preco_atual}")

print(f"Hoje é dia {data_formatada}")

# Seleção dos candles (fechados)
candle_2_dias_atras = data.iloc[-2]  # 2 dias atrás
candle_1_dia_atras = data.iloc[-1]   # 1 dia atrás

# Usar preços de fechamento dos candles fechados
preco_1 = float(candle_2_dias_atras['Close'])  # fechamento 2 dias atrás
preco_0 = float(candle_1_dia_atras['Close'])   # fechamento 1 dia atrás

# Calcular intervalo da Fibonacci
fib_range = preco_0 - preco_1

# Níveis ajustados conforme pedido
nivel_1 = preco_1                    # fechamento 2 dias atrás
nivel_0382 = preco_0                 # fechamento 1 dia atrás
nivel_0 = preco_1 - (fib_range * 0.382)  # projeção do preço para o próximo dia

# Exibição dos resultados
print(f"\n>>> RESULTADOS <<<")
print(f"Nível 1 (fechamento 2 dias atrás): {round(nivel_1, 2)}")
print(f"Nível 0.382 (fechamento 1 dia atrás): {round(nivel_0382, 2)}\n")
print(f"Nível 0.0 (projeção preço próximo dia): {round(nivel_0, 2)}\n\n")