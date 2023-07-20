import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

def atualizar_pedido_simplo7(pedido_data):
    try:
        url = f"https://www.outletdosquadros.com.br/ws/wspedidos/{pedido_data['id']}.json"

        payload = json.dumps({
            "Wspedido": {
                "Entrega": {
                    "rastreamento": pedido_data["rastreamento"]
                }
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'appKey': 'ZjQxYjBkZDE1YjE1MDBlNjI5NjBhOGYzY2Y2MWRlOWU='
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        response_json = response.json()

        if response.status_code == 200:
            print(f"Pedido {pedido_data['id']} atualizado com sucesso.")
        else:
            print(f"Erro ao atualizar pedido {pedido_data['id']}: {response_json}")

    except Exception as e:
        print(f"Erro ao atualizar pedido {pedido_data['id']}: {str(e)}")


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

        # Obtendo os valores de todas as colunas
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])

        if not values:
            print('Não foram encontrados dados na planilha.')
            return

        # Aqui você pode manipular os dados retornados na lista 'values'
        # Suponha que os dados das colunas estejam organizados em listas dentro da lista 'values'
        for row_data in values:
            # Suponha que as colunas A, B e K correspondam às colunas 0, 1 e 10 na lista 'row_data'
            pedido_data = {
                "id": row_data[0], # Número do pedido OUTLET   
                "rastreamento": row_data[9] # Código de rastreamento
            }

            # Atualiza o pedido no Simplo7 usando a função definida anteriormente
            atualizar_pedido_simplo7(pedido_data)

    except Exception as e:
        print('Erro ao buscar os dados da planilha:', str(e))
        raise e


if __name__ == "__main__":
    buscar_dados_da_planilha()
