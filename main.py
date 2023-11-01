import requests
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import time

def atualizar_pedido_simplo7(pedido_data):
    max_attempts = 3
    attempt = 0

    while attempt < max_attempts:
        try:
            url = f"https://www.outletdosquadros.com.br/ws/wspedidos/{pedido_data['id']}.json"

            payload = {
                "Wspedido": {
                    "Entrega": {
                        "rastreamento": pedido_data["rastreamento"],
                        "url_rastreamento": "https://www.jadlog.com.br/jadlog/home",
                    },
                    "Status": pedido_data['status'],
                }
            }

            headers = {
                "Content-Type": "application/json",
                "appKey": "ZjQxYjBkZDE1YjE1MDBlNjI5NjBhOGYzY2Y2MWRlOWU=",
            }

            response = requests.put(url, headers=headers, json=payload)
            response_json = response.json()

            if response.status_code == 200:
                print(f"Pedido {pedido_data['numero_pedido']} atualizado com sucesso.")
                break
            else:
                print(f"Erro ao atualizar pedido {pedido_data['numero_pedido']}: {response_json}")

        except Exception as e:
            print(f"Erro ao atualizar pedido {pedido_data['numero_pedido']}: {str(e)}")

        attempt += 1
        if attempt < max_attempts:
            print(f"Tentando novamente em 60 segundos...")
            time.sleep(60)

    if attempt >= max_attempts:
        print(f"Atingido o número máximo de tentativas para o pedido {pedido_data['numero_pedido']}.")

def calcular_diferenca_de_datas(data1, data2):
    return (data1 - data2).days

def processar_pedido(row_data, data_atual):
    if row_data[2]:
        data_pedido = datetime.datetime.strptime(row_data[2], "%d/%m/%Y").date()
        diferenca_dias = calcular_diferenca_de_datas(data_atual, data_pedido)

        if 0 <= diferenca_dias <= 30:
            if len(row_data) > 14 and row_data[4] != '' and row_data[14] != '' and row_data[15] != '' and row_data[16] == 'Site':
                id = str(int(row_data[4]) - 10)

                if 'EMITIDO' in row_data[15]:
                    status = "24"
                    status_msg = "TRANSPORTE"
                elif 'FINALIZADO' in row_data[15]:
                    status = "3"
                    status_msg = "FINALIZADO"
                
                if 'CANCELADO' in row_data[15]:
                    status = "4"

                if status != '':
                    pedido_data = {
                        "id": id,
                        "numero_pedido": row_data[4],
                        "rastreamento": row_data[14],
                        "status": status
                    }

                # print(f"Pedido {row_data[4]} está {status_msg} e dentro do intervalo de 1 mês e meio.")
                atualizar_pedido_simplo7(pedido_data)

def buscar_dados_da_planilha():
    try:
        credenciais = service_account.Credentials.from_service_account_file("client_secret.json")
        spreadsheet_id = "1z14zZrinju-GVJVnCjjhTr0B9mHhtN_oBhXMjZ0uvoQ"
        range_name = "FRETE!A:Q"

        service = build("sheets", "v4", credentials=credenciais)
        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get("values", [])

        if not values:
            print("Não foram encontrados dados na planilha.")
            return

        data_atual = datetime.date.today()

        for row_data in values[1:]:
            processar_pedido(row_data, data_atual)

    except Exception as e:
        print("Erro ao buscar os dados da planilha:", str(e))
        raise e

if __name__ == "__main__":
    buscar_dados_da_planilha()
