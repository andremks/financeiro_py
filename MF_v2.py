import yfinance as yf
import pandas as pd
import numpy as np
import pytz

TICKER = "PETR4.SA"
INTERVAL = "60m"
PERIOD = "30d"
LOTE = 100

df = yf.download(TICKER, interval=INTERVAL, period=PERIOD)
df.reset_index(inplace=True)
df = df.sort_values('Datetime').reset_index(drop=True)

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).fillna(0)
    loss = -delta.clip(upper=0).fillna(0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

df['RSI'] = compute_rsi(df['Close'], period=14)

N = 50
df_recent = df.tail(N)
topo = float(df_recent['High'].max())
fundo = float(df_recent['Low'].min())

fibo_levels = [0, 0.236, 0.382, 0.5, 0.618, 0.786, 1]
fibo_prices = [topo - (topo-fundo)*level for level in fibo_levels]
fibo_niveis = {f'{level:.3f}': round(price, 2) for level, price in zip(fibo_levels, fibo_prices)}

volume_atual = int(df['Volume'].iloc[-1])
media_volume_5 = int(df['Volume'].tail(5).mean())
media_volume_20 = int(df['Volume'].tail(20).mean())

closes = df['Close'].tail(20).values
if len(closes) < 2:
    trend_curta = "indefinida"
else:
    trend_curta = "alta" if closes[-1] > closes[0] else "baixa"

rsi_atual = float(df['RSI'].iloc[-1])

# COMPRA: (reversão/pullback)
preco_entrada_compra = fibo_niveis['0.618']
alvos_compra = {
    'Conservador': fibo_niveis['0.500'],
    'Moderado': fibo_niveis['0.382'],
    'Agressivo': fibo_niveis['0.236'],
}
stop_loss_compra = fibo_niveis['1.000']

# VENDA: seguindo tendência de baixa
preco_entrada_venda = fibo_niveis['0.382']  # venda no pullback
alvos_venda = {
    'Conservador': fibo_niveis['0.618'],
    'Moderado': fibo_niveis['0.786'],
    'Agressivo': fibo_niveis['1.000'],
}
stop_loss_venda = fibo_niveis['0.236']

def calcula_lucro(entrada, saida, lote=100, tipo="compra"):
    if tipo == "compra":
        return round((saida - entrada) * lote, 2)
    else:  # venda/short
        return round((entrada - saida) * lote, 2)

lucros_compra = {alvo: calcula_lucro(preco_entrada_compra, preco_alvo, LOTE, "compra") for alvo, preco_alvo in alvos_compra.items()}
lucros_venda = {alvo: calcula_lucro(preco_entrada_venda, preco_alvo, LOTE, "venda") for alvo, preco_alvo in alvos_venda.items()}

# Dia/hora de Brasília e preço atual
ultimo_dt_utc = df['Datetime'].iloc[-1]
if ultimo_dt_utc.tzinfo is None:
    ultimo_dt_utc = ultimo_dt_utc.tz_localize('UTC')
fuso_brasilia = pytz.timezone('America/Sao_Paulo')
ultimo_dt_brasil = ultimo_dt_utc.astimezone(fuso_brasilia)
dia_hora_brasilia = ultimo_dt_brasil.strftime('%d/%m/%Y %H:%M')
preco_atual = float(df['Close'].iloc[-1])

print(f"\nTendência curta: {trend_curta.upper()}")
print(f"RSI atual: {rsi_atual:.2f}")
print(f"Volume atual: {volume_atual:,} | Média (5): {media_volume_5:,} | Média (20): {media_volume_20:,}\n")
print(f"Níveis de Fibonacci (topo: {topo:.2f}, fundo: {fundo:.2f}):")
for level, price in fibo_niveis.items():
    print(f"  Fibo {level}: {price:.2f}")

print("\n-----------------------------")
print("ALVOS PARA OPERAÇÃO COMPRADA (reversão/pullback):")
print(f"Sugestão de entrada: {preco_entrada_compra:.2f}")
print(f"Stop loss: {stop_loss_compra:.2f}")
for nome, preco_alvo in alvos_compra.items():
    print(f"  {nome:10}: {preco_alvo:.2f} | Lucro: R$ {lucros_compra[nome]:.2f}")

print("\nALVOS PARA OPERAÇÃO VENDIDA (seguindo tendência de baixa):")
print(f"Sugestão de entrada: {preco_entrada_venda:.2f}")
print(f"Stop loss: {stop_loss_venda:.2f}")
for nome, preco_alvo in alvos_venda.items():
    print(f"  {nome:10}: {preco_alvo:.2f} | Lucro: R$ {lucros_venda[nome]:.2f}")

print("\n-----------------------------")
print(f"Data/hora (Brasília): {dia_hora_brasilia}")
print(f"Preço atual: R$ {preco_atual:.2f}")
print("-----------------------------")