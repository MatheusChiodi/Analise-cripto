from pycoingecko import CoinGeckoAPI
import pandas as pd

# Obter lista completa de moedas
cg = CoinGeckoAPI()
moedas = cg.get_coins_list()

# Criar DataFrame a partir da lista de moedas
df_moedas = pd.DataFrame(moedas)

# Salvar o DataFrame em um arquivo Excel
file_path = "lista_moedas_coingecko.xlsx"
df_moedas.to_excel(file_path, index=False)

print(f"Arquivo Excel salvo em: {file_path}")
