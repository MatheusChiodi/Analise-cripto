from flask import Flask, render_template, request, redirect, url_for
from pycoingecko import CoinGeckoAPI
import time
import threading

app = Flask(__name__)

# Configuração inicial
moedas = ['bitcoin', 'dogecoin', 'ethereum', 'binance-coin-wormhole', 'ripple', 'thena']
moedas_sugestoes = {
    'bitcoin': {'preco_compra': 0, 'descricao': 'Principal criptomoeda do mercado.'},
    'ethereum': {'preco_compra': 0, 'descricao': 'Plataforma líder para contratos inteligentes.'},
    'dogecoin': {'preco_compra': 0, 'descricao': 'Moeda meme com alto potencial especulativo.'},
    'binance-coin-wormhole': {'preco_compra': 0, 'descricao': 'Moeda da exchange Binance (BNB).'},
    'ripple': {'preco_compra': 0, 'descricao': 'Moeda para transações bancárias. (XRP)'},
    'thena': {'preco_compra': 0, 'descricao': 'Moeda de cripto-fiat com alto valor.'},
}

# Dados de compras (adicionados manualmente no código)
compras_moedas = {
    'bitcoin': {'quantidade': 0.00011367, 'preco_compra': 98582.94},
    'ethereum': {'quantidade': 0, 'preco_compra': 0},
    'dogecoin': {'quantidade': 51.14961121, 'preco_compra': 0.42},
    'binance-coin-wormhole': {'quantidade': 0.01551858, 'preco_compra': 652.61},
    'ripple': {'quantidade': 7.23655381, 'preco_compra': 1.38},
    'thena': {'quantidade': 4.66683051, 'preco_compra': 3.40},
}

monitorando = False


def obter_precos(moedas):
    """
    Obtém os preços atuais das moedas.
    """
    cg = CoinGeckoAPI()
    precos = cg.get_price(ids=moedas, vs_currencies='usd', include_24hr_change=True)
    return precos


def calcular_preco_ideal(preco_atual, variacao_24h):
    """
    Calcula um preço de compra ideal com base no preço atual e na variação de 24 horas.
    """
    margem = abs(variacao_24h) * 0.01  # Ajusta a margem com base na volatilidade
    preco_ideal = preco_atual * (1 - margem)
    return round(preco_ideal, 2)


def calcular_preco_medio_lucro(moeda, preco_atual):
    """
    Calcula o preço médio e o lucro com base nos dados de compra.
    """
    dados_compra = compras_moedas.get(moeda, {'quantidade': 0, 'preco_compra': 0})
    quantidade = dados_compra['quantidade']
    preco_medio = dados_compra['preco_compra']

    # Calcula lucro/prejuízo
    lucro = (preco_atual - preco_medio) * quantidade
    return {'preco_medio': preco_medio, 'lucro': round(lucro, 2)}


def calcular_totais(precos):
    """
    Calcula o gasto total e o valor atual de todas as moedas.
    """
    gasto_total = 0
    valor_atual = 0

    for moeda, dados_compra in compras_moedas.items():
        quantidade = dados_compra['quantidade']
        preco_compra = dados_compra['preco_compra']
        preco_atual = precos[moeda]['usd']

        gasto_total += quantidade * preco_compra
        valor_atual += quantidade * preco_atual

    return round(gasto_total, 2), round(valor_atual, 2)


def recomendacao_investimento(moedas_sugestoes, precos, start_index=10):
    """
    Gera recomendações de investimento com base nos preços atuais e variações.
    Incrementa os índices em múltiplos de 10.
    """
    recomendacoes = []
    current_index = start_index

    for moeda, dados in moedas_sugestoes.items():
        preco_atual = precos[moeda]['usd']
        variacao_24h = precos[moeda]['usd_24h_change']
        preco_ideal_calculado = calcular_preco_ideal(preco_atual, variacao_24h)

        # Calcula preço médio e lucro
        calculos = calcular_preco_medio_lucro(moeda, preco_atual)

        if preco_atual <= dados['preco_compra']:
            recomendacao = "Comprar"
        else:
            recomendacao = "Esperar"

        recomendacoes.append({
            'index': current_index,
            'moeda': moeda.capitalize(),
            'preco_atual': preco_atual,
            'preco_ideal': preco_ideal_calculado,
            'recomendacao': recomendacao,
            'descricao': dados['descricao'],
            'variacao': variacao_24h,
            'preco_medio': calculos['preco_medio'],
            'lucro': calculos['lucro']
        })
        current_index += 10  # Incrementa o índice em 10

    return recomendacoes


@app.route("/")
def index():
    """
    Página inicial que exibe preços e recomendações.
    """
    precos = obter_precos(moedas)
    recomendacoes = recomendacao_investimento(moedas_sugestoes, precos, start_index=10)
    gasto_total, valor_atual = calcular_totais(precos)
    return render_template("index.html", recomendacoes=recomendacoes, gasto_total=gasto_total, valor_atual=valor_atual)


@app.route("/monitorar", methods=["GET", "POST"])
def monitorar():
    """
    Página para iniciar ou interromper o monitoramento contínuo.
    Exibe os dados de preços monitorados diretamente na página.
    """
    global monitorando
    dados_precos = []

    if request.method == "POST":
        if not monitorando:
            monitorando = True
            threading.Thread(target=monitorar_precos_continuamente).start()
        else:
            monitorando = False

    if monitorando:
        precos = obter_precos(moedas)
        dados_precos = recomendacao_investimento(moedas_sugestoes, precos)

    return render_template("monitorar.html", monitorando=monitorando, dados_precos=dados_precos)


def monitorar_precos_continuamente():
    """
    Função para monitorar preços continuamente em um thread separado.
    """
    global monitorando

    while monitorando:
        precos = obter_precos(moedas)
        recomendacoes = recomendacao_investimento(moedas_sugestoes, precos)
        print("\nMonitorando Preços...")
        for rec in recomendacoes:
            print(f"{rec['moeda']}: {rec['recomendacao']} | Preço Atual: ${rec['preco_atual']:.2f}")
        time.sleep(10)  # Intervalo de 10 segundos entre as verificações


if __name__ == "__main__":
    app.run(debug=True)

