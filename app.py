import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json
from datetime import date
import pandas as pd

# Os filtros são definidos nessas duas listas
filtros_orgs = {"PET Sistemas de Informação", "PET Sistemas de Informação - Monte Carmelo", "PETSIMC"}
filtros_tipos = {"Programa PET", "Estágio UFU", "Mest./Dout./Especializ.", "Monitoria"}

# Obtém o ano atual para comparar com a data dos editais e transforma em String
data_atual = date.today()
ano_atual = '{}'.format(data_atual.year)

# Inicializa variáveis de controle
id_pag = 0  # Página inicial
QTD_MAX = 20  # Última página
continuar = True  # Variável que indica se devemos continuar a busca

# Lista que vai armazenar todos os dados de editais coletados
editais_data = []

# Laço que percorre as páginas de editais enquanto a quantidade de páginas for menor que QTD_MAX e devemos continuar
while (id_pag < QTD_MAX and continuar):
    # Formata a URL da página de editais com o número da página atual
    url = f"http://www.editais.ufu.br/discente?page={id_pag}"
    
    # Faz uma requisição HTTP para obter o conteúdo da página
    response = requests.get(url)
    
    # Verifica se a requisição foi bem-sucedida (status 200)
    if response.status_code == 200:
        # Analisa o conteúdo da página HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra todos os blocos de editais (linhas da tabela de editais)
        edital_blocks = soup.find_all('tr')

        # Itera sobre cada edital encontrado na página
        for edital in edital_blocks:
            numero_edital = edital.find('td', class_='views-field-field-nro-value')
            numero_edital = numero_edital.get_text(strip=True) if numero_edital else 'N/A'

            orgao_responsavel = edital.find('td', class_='views-field-field-setor-responsavel-value')
            orgao_responsavel = orgao_responsavel.get_text(strip=True) if orgao_responsavel else 'N/A'
            
            titulo = edital.find('td', class_='views-field-title')
            titulo_text = titulo.get_text(strip=True) if titulo else 'N/A'

            link_edital = None
            if titulo:
                a_tag = titulo.find('a', href=True)  # Encontra a tag que contém o link
                if a_tag:
                    # Cria a URL completa do edital usando urljoin
                    link_edital = urljoin(url, a_tag['href'])
            
            tipo = edital.find('td', class_='views-field-field-tipo-value')
            tipo = tipo.get_text(strip=True) if tipo else 'N/A'
            
            data_publicacao = edital.find('td', class_='views-field-field-data-publicacao-value')
            data_publicacao = data_publicacao.get_text(strip=True) if data_publicacao else 'N/A'
            
            # Extrai o ano da data de publicação
            ano_edital = '{}'.format(data_publicacao[4:9].strip())

            # Se qualquer uma dessas informações estiver disponível, cria um dicionário com os dados do edital
            if numero_edital != 'N/A' or orgao_responsavel != 'N/A' or titulo_text != 'N/A' or tipo != 'N/A' or data_publicacao != 'N/A' or link_edital:
                edital_info = {
                    'numero_edital': numero_edital,
                    'orgao_responsavel': orgao_responsavel,
                    'titulo': titulo_text,
                    'tipo': tipo,
                    'data_publicacao': data_publicacao,
                    'link': link_edital
                }

                # Adiciona o edital à lista se ele passar pelos filtros de órgão, tipo e ano.
                if (orgao_responsavel in filtros_orgs) and (tipo in filtros_tipos) and ano_edital == ano_atual:
                    editais_data.append(edital_info)

        # Se o ano do edital não for o ano atual, interrompe a busca
        if(ano_edital != ano_atual):
            continuar = False
                 
    else:
        # Exibe uma mensagem de erro se a página não for acessada com sucesso
        print(f"Erro ao acessar a página. Status code: {response.status_code}")
        break
    
    # Incrementa o número da página para acessar a próxima
    id_pag += 1

# Converte a lista de editais em um arquivo JSON e salva no disco
editais_json = json.dumps(editais_data, ensure_ascii=False, indent=4)
json_filename = "editais.json"
with open(json_filename, 'w', encoding='utf-8') as json_file:
    json_file.write(editais_json)

# Converte os dados dos editais em um DataFrame do pandas e salva em um arquivo Excel
xlsx_filename = 'editais.xlsx'
df = pd.DataFrame(editais_data)
df.to_excel(xlsx_filename, index=False)

# Exibe uma mensagem informando que os dados foram salvos
print(f"Dados salvos em {xlsx_filename} e {json_filename}")
