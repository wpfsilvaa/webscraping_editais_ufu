Este projeto é um **scraper web** que coleta informações de editais publicados no site da UFU, filtrando com base em critérios predefinidos. Os dados coletados são exportados em formatos **JSON** e **Excel** para facilitar o uso e análise.

---

## **Como Funciona o Script**

### 1. **Filtros Definidos**
- **Órgãos responsáveis** (`filtros_orgs`): Apenas editais de órgãos específicos serão incluídos.
- **Tipos de edital** (`filtros_tipos`): Somente editais de tipos selecionados serão processados.

### 2. **Coleta e Processamento**
- O script acessa páginas do site iterativamente, começando da página 0 até o limite configurado em `QTD_MAX`.
- Cada página é analisada usando **BeautifulSoup**, e os dados relevantes dos editais são extraídos.
- O processamento é interrompido antecipadamente se for encontrado um edital de ano diferente do ano atual.

### 3. **Dados Extraídos**
Para cada edital, o script coleta:
- Número do edital (`numero_edital`)
- Órgão responsável (`orgao_responsavel`)
- Título (`titulo`)
- Tipo de edital (`tipo`)
- Data de publicação (`data_publicacao`)
- Link para mais informações (`link`)

### 4. **Armazenamento**
Os dados são salvos em dois formatos:
- **JSON**: Estruturado para integração com outras ferramentas ou APIs.
- **Excel**: Formato tabular para análise manual ou relatórios.

---

## **Como Usar**

1. **Instale as Dependências**
   Certifique-se de que as bibliotecas necessárias estão instaladas:
   ```bash
   pip install requests beautifulsoup4 pandas openpyxl
   ```

2. **Execute o Script**
   Execute o script em seu ambiente Python:
   ```bash
   python script.py
   ```

3. **Verifique os Arquivos Gerados**
   - O JSON será salvo como `editais.json`.
   - O Excel será salvo como `editais.xlsx`.

---

## **Estrutura do Código**

1. **Configuração de Filtros e Variáveis**  
   Define filtros para órgãos, tipos de edital e controla a navegação nas páginas.

2. **Coleta de Dados**  
   - Faz requisições HTTP para acessar cada página de editais.
   - Analisa o conteúdo HTML e extrai as informações relevantes.

3. **Filtragem e Armazenamento**  
   - Apenas editais que atendem aos filtros são incluídos.
   - Os dados são exportados para JSON e Excel.

---

## **Exemplo de Filtros**

### Filtros de Órgãos
```python
filtros_orgs = {"PET Sistemas de Informação", "PET Sistemas de Informação - Monte Carmelo", "PETSIMC"}
```

### Filtros de Tipos
```python
filtros_tipos = {"Programa PET", "Estágio UFU", "Mest./Dout./Especializ.", "Monitoria"}
```

Se quiser incluir mais órgãos ou tipos, basta adicionar os novos valores às listas.

---

## **Exemplo de Saída JSON**

```json
[
    {
        "numero_edital": "001/2024",
        "orgao_responsavel": "PET Sistemas de Informação",
        "titulo": "Seleção para bolsistas do PET",
        "tipo": "Programa PET",
        "data_publicacao": "2024-01-15",
        "link": "http://www.editais.ufu.br/discente/001-2024"
    }
]
```

---

## **Melhorias Futuras**
1. **Paralelização**  
   - Utilizar bibliotecas como `asyncio` ou `concurrent.futures` para acelerar o scraping.

2. **Tratamento de Erros**  
   - Lidar com exceções durante as requisições HTTP ou parsing de HTML.

3. **Interface Configurável**  
   - Permitir que o usuário defina os filtros e outros parâmetros via interface ou arquivo de configuração.

4. **Detecção Automática do Ano Atual no HTML**  
   - Extrair o ano diretamente do conteúdo HTML, em vez de usar o sistema local.

5. **Logs Detalhados**  
   - Salvar logs de execução para depuração e auditoria.

---
