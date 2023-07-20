import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build

def buscar_dados_da_planilha():
    try:
        # Substitua as informações abaixo pelas suas credenciais e ID da planilha
        # Você precisa criar um projeto no Console de Desenvolvedor do Google e ativar a API do Google Sheets
        # Depois, crie um arquivo de credenciais e defina o caminho para esse arquivo abaixo
        credenciais = service_account.Credentials.from_service_account_file('client_secret.json')

        spreadsheet_id = '1z14zZrinju-GVJVnCjjhTr0B9mHhtN_oBhXMjZ0uvoQ'
        range_name = 'FRETE!A:M'

        service = build('sheets', 'v4', credentials=credenciais)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('Não foram encontrados dados na planilha.')
            return []

        # Aqui você pode manipular os dados retornados na lista 'values'
        print(values)

    except Exception as e:
        print('Erro ao buscar os dados da planilha:', str(e))
        raise e

buscar_dados_da_planilha()

# def atualizar_rastreamento_pedido(pedido_id, rastreamento):
#     try:
#         url = f'https://{{url-loja}}/ws/wspedidos/{pedido_id}.json'
#         headers = {
#             'Content-Type': 'application/json',
#             'appKey': '{{appKey}}'
#         }
#         data = {
#             'Wspedido': {
#                 'Entrega': {
#                     'rastreamento': rastreamento
#                 }
#             }
#         }

#         response = requests.put(url, headers=headers, json=data)

#         if response.status_code == 200:
#             print(f'Rastreamento do pedido {pedido_id} atualizado com sucesso!')
#         else:
#             print(f'Erro ao atualizar o rastreamento do pedido {pedido_id}. Status code: {response.status_code}')
#             print(response.text)

#     except Exception as e:
#         print(f'Erro ao atualizar o rastreamento do pedido {pedido_id}:', str(e))

# # Função principal para executar a automação
# def main():
#     # Buscar os dados da planilha do Google Sheets
#     dados_da_planilha = buscar_dados_da_planilha()

#     # Iterar pelos dados e atualizar os pedidos na Simplo7
#     for row in dados_da_planilha:
#         pedido_id = row[0]             # Número do pedido
#         nota_numero = row[1]           # Número da nota fiscal
#         nota_serie = row[2]            # Série da nota fiscal
#         nota_chave = row[3]            # Chave da nota fiscal
#         nota_data = row[4]             # Data da nota fiscal
#         rastreamento = row[5]          # Número de rastreamento

#         pedido = {
#             'id': pedido_id,
#             'nota_numero': nota_numero,
#             'nota_serie': nota_serie,
#             'nota_chave': nota_chave,
#             'nota_data': nota_data,
#             'rastreamento': rastreamento
#         }

#         atualizar_rastreamento_pedido(pedido_id, rastreamento)

# # Executar a função principal
# if __name__ == "__main__":
#     main()
