# VulnBuilderAI: Ferramenta Multiplataforma para Construção de Datasets de Vulnerabilidades com Categorização por IA

[![Licença](https://img.shields.io/badge/License-GNU%20GPL-blue)](https://opensource.org/licenses/GNU)

**Resumo do Artigo:**

_Este projeto apresenta o VulnBuilderAI, uma ferramenta para construir datasets de vulnerabilidades de software. A ferramenta coleta dados de múltiplas fontes, normaliza, extrai informações relevantes usando PLN (incluindo LLMs) e categoriza as vulnerabilidades. O objetivo é gerar datasets de alta qualidade para pesquisa e prática em segurança de software._

---

## Estrutura do README.md

Este README.md está organizado nas seguintes seções:

1.  **Título e Resumo:** Título do projeto e um resumo conciso (cópia do resumo do artigo).
2.  **Funcionalidades:** Lista as principais funcionalidades da ferramenta.
3.  **Pré-requisitos:** Lista os requisitos de software (Python, APIs).
4.  **Instalação:** Instruções passo a passo para instalar a ferramenta.
5.  **Configuração:** Instruções para configurar as chaves de API.
6.  **Uso:** Descreve como reproduzir os experimentos apresentados no artigo..
7.  **Experimentos:** Explicação dos argumentos de linha de comando e exemplos de uso.
8.  **Docker (Opcional):** Instruções para construir e executar a ferramenta usando Docker.
9.  **Estrutura do Código:** Breve visão geral da organização do código-fonte.
10. **Extensibilidade**: Como adicionar novas fontes e novos exportadores.
11. **Licença:** Informações sobre a licença do projeto.

---

## Selos
- **Artefatos Disponíveis (SeloD)**
  - O repositório disponível no GitHub contém o arquivo README.md, o qual fornece todas as informações necessárias para entender e utilizar o projeto. Nele, você encontrará detalhes sobre o propósito do projeto, requisitos de sistema, instruções de instalação e execução, além de outras informações relevantes.
- **Artefatos Funcionais (SeloF)**
  ## Dependências
  - `requests`
  - `google-generativeai`
  - `openai`
  - `transformers`
  - `psutil`
  - `huggingface_hub`
  - `torch`

  ## Versões das Dependências, Linguagens e Ambiente
  - **Linguagem:** Python 3.10
  - **Bibliotecas e Ferramentas:**
    - `requests`: versão 2.31.0
    - `google-generativeai`: versão 0.1.3
    - `openai`: versão 0.27.2
    - `transformers`: versão 4.27.4
    - `psutil`: versão 5.9.4
    - `huggingface_hub`: versão 0.13.3
    - `torch`: versão 2.0.0
  - **Ambiente:** Sistema operacional Ubuntu 20.04 LTS, arquitetura x86_64.

  ## Descrição do Ambiente de Execução
  Este projeto foi desenvolvido para rodar em ambiente Linux e Windows. É necessário suporte para Python 3.10 e acesso à internet para baixar as dependências. Pode ser configurado localmente ou em contêineres como Docker.

-**Artefatos Sustentáveis (SeloS)**
-**Experimentos Reprodutíveis (SeloR)**
-**Experimentos Reprodutíveis (SeloR)**

## Instruções para Reproduzir as Principais Reivindicações

Este repositório fornece scripts e instruções detalhadas para reproduzir os resultados apresentados no artigo, incluindo gráficos e tabelas.

### Passos para Reproduzir os Resultados

1. **Configuração do Ambiente**  
   Certifique-se de preparar o ambiente conforme especificado na seção de instalação deste README.md. Todas as dependências necessárias podem ser instaladas utilizando o arquivo `requirements.txt`.

2. **Execução dos Experimentos**  
   Utilize o script principal para realizar os experimentos e gerar os resultados:
   ```bash
   python src/main.py --provider '[PROVEDOR_LLM]' --data-source '[FONTE_DADOS]' --search-params '[PARAMETRO_BUSCA]' --export-format [FORMATO_SAIDA] --output-file [ARQUIVO_SAIDA]
## Detalhamento dos Argumentos de Linha de Comando

| Argumento              | Descrição                                                                                             | Exemplo                          |
|------------------------|-----------------------------------------------------------------------------------------------------|----------------------------------|
| `--provider`           | Nome do provedor de LLM (Large Language Model) a ser utilizado.                                      | `--provider 'openai'`           |
| `--data-source`        | Caminho ou identificador para a fonte de dados que será utilizada pela ferramenta.                   | `--data-source 'dados.csv'`     |
| `--search-params`      | Parâmetros de busca que devem ser utilizados durante a execução.                                     | `--search-params '{"query": "AI"}'` |
| `--export-format`      | Formato do arquivo de exportação gerado pela ferramenta (e.g., `csv`, `json`, `txt`).                | `--export-format 'json'`        |
| `--output-file`        | Caminho ou nome do arquivo onde os resultados serão salvos.                                         | `--output-file 'resultado.json'`|

---

Se precisar de mais detalhes ou ajustes, posso incluir mais informações na tabela! 😊

## Instruções de Instalação e Execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuprojeto/seurepositorio.git
   cd seurepositorio

## Funcionalidades

- **Coleta de Dados:** Busca dados de vulnerabilidades em múltiplas fontes:
  - NVD (National Vulnerability Database)
  - Vulners
  - GitHub (através de uma API, _implementação futura_)
- **Processamento de Dados:**
  - Normalização e limpeza dos dados.
  - Remoção de duplicatas.
  - Truncamento de descrições longas.
  - Filtragem de vulnerabilidades por critérios (e.g., fornecedor).
- **Extração de Informações:** Extrai informações relevantes das descrições das vulnerabilidades, como:
  - ID da vulnerabilidade (CVE, etc.)
  - Título
  - Descrição
  - Fornecedor
  - Data de publicação
  - Score CVSS (se disponível)
  - Severidade (se disponível)
  - Fonte da informação
- **Categorização com IA:**
  - Utiliza modelos de linguagem (LLMs) para categorizar as vulnerabilidades:
    - Google Gemini
    - OpenAI ChatGPT
    - Meta Llama 3
  - Extrai as seguintes informações usando os LLMs:
    - Categoria CWE (Common Weakness Enumeration)
    - Explicação da CWE
    - Fornecedor
    - Causa da vulnerabilidade
    - Impacto da vulnerabilidade
  - Sistema de votação ponderada para combinar os resultados dos diferentes LLMs.
- **Exportação de Dados:**
  - Exporta os dados processados e categorizados para arquivos CSV ou JSON.
- **Extensibilidade:**
  - Arquitetura modular que facilita a adição de novas fontes de dados e novos modelos de IA.
- **Linha de Comando:**
  - Interface de linha de comando para facilitar o uso da ferramenta.

## Pré-requisitos

- Python 3.8 ou superior.
- Chaves de API para os seguintes serviços (opcional, dependendo dos módulos e LLMs que você for usar):
  - **Vulners:** Obtenha uma chave em [https://vulners.com/](https://vulners.com/)
  - **Google Gemini:** Obtenha uma chave em [https://ai.google.dev/](https://ai.google.dev/)
  - **OpenAI ChatGPT:** Obtenha uma chave em [https://platform.openai.com/](https://platform.openai.com/)
  - **Llama (Meta):** Obtenha uma chave em [https://llama-api.com/](https://llama-api.com/)

## Instalação

1.  **Clone o repositório:**

    ```bash
    git clone https://github.com/douglasfideles/VulnBuilderAI.git
    cd VulnBuilderAI
    ```

2.  **Crie um ambiente virtual (recomendado):**

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    .venv\Scripts\activate  # Windows
    ```

3.  **Instale as dependências:**

    ```bash
    pip install -r requirements.txt
    ```

    Caso tenha problemas, instale individualmente:

    ```bash
      pip install google-generativeai
      pip install openai
      pip install requests
    ```

## Configuração

Você pode configurar o VulnBuilderAI usando _variáveis de ambiente_ ou _argumentos de linha de comando_. A ordem de prioridade é: argumentos de linha de comando > variáveis de ambiente.

1.  **Arquivo de configuração (opcional):**
    _Não implementado no código fornecido._ Se você quisesse adicionar um arquivo de configuração (e.g., `config.ini` ou `config.yaml`), precisaria modificar o código (`main.py`) para ler as configurações desse arquivo.

## Uso

### Argumentos de Linha de Comando

```bash
python src/main.py --source <ai_provider> --data-source <data_source> --vulners-key <vulners_key> --gemini-key <gemini_key> --chatgpt-key <chatgpt_key> --llama-key <llama_key>  --export-format <format> --output-file <filename>  --search-params <params> --search-file <file_path>
```

- `--source`: **Obrigatório.** Seleciona o provedor de IA para categorização. Opções:
  - `gemini`: Usa o Google Gemini.
  - `chatgpt`: Usa o OpenAI ChatGPT.
  - `llama`: Usa o Meta Llama.
  - `combined`: Usa _todos_ os modelos acima, com um sistema de votação ponderada.
  - `none`: _Não_ usa IA para categorização (útil para coletar e normalizar dados sem categorizar).
- `--data-source`: **Obrigatório.** Seleciona a fonte de dados de vulnerabilidades. Opções:
  - `nvd`: Usa o National Vulnerability Database (NVD).
  - `vulners`: Usa a API do Vulners.
  - `both`: Usa _ambas_ as fontes (NVD e Vulners).
- `--gemini-key`: Chave de API para o Google Gemini (se `--source` for `gemini` ou `combined`).
- `--chatgpt-key`: Chave de API para o OpenAI ChatGPT (se `--source` for `chatgpt` ou `combined`).
- `--llama-key`: Chave de API para o Llama (se `--source` for `llama` ou `combined`).
- `--default-key`: Chave de API Default para LLM
- `--default-url`: Base URL para Default LLM
- `--default-model`: Modelo para Default LLM
- `--vulners-key`: Chave de API para o Vulners (se `--data-source` for `vulners` ou `both`).
- `--export-format`: Formato de exportação dos dados. Opções:
  - `csv`: Arquivo CSV (Comma-Separated Values).
  - `json`: Arquivo JSON.
  - O padrão é `csv`.
- `--output-file`: Nome do arquivo de saída (e caminho, se necessário). O padrão é `dataset/dds_vulnerabilities_AI.csv`.
- `--search-params`: Parâmetros de busca para vulnerabilidades (palavras-chave separadas por espaço). _Exemplo:_ `"OpenDDS" "RTI Connext DDS"`
- `--search-file`: Caminho para um arquivo _de texto_ contendo os parâmetros de busca (uma palavra-chave ou frase por linha). _Exemplo:_ `search_params.txt`

### Exemplos de Comando

1.  **Usando todas as IAs, ambas as fontes e múltiplos termos de busca:**

    ```bash
    python src/main.py --source combined --data-source both --search-params "OpenDDS" "RTI Connext DDS" --gemini-key <SUA_CHAVE_GEMINI> --chatgpt-key <SUA_CHAVE_CHATGPT> --llama-key <SUA_CHAVE_LLAMA>  --vulners-key <SUA_CHAVE_VULNERS> --export-format csv --output-file vulnerabilidades.csv
    ```

    - `--source combined`: Usa Gemini, ChatGPT e Llama, com votação.
    - `--data-source both`: Usa NVD e Vulners.
    - `--search-params`: Busca por vulnerabilidades relacionadas a "OpenDDS" _e_ "RTI Connext DDS".
    - As chaves de API são fornecidas.
    - O resultado é salvo em `vulnerabilidades.csv`.

2.  **Sem IA, usando apenas o NVD:**

    ```bash
    python src/main.py --source none --data-source nvd --search-params "OpenDDS" --export-format csv --output-file vulnerabilidades_nvd.csv
    ```

    - `--source none`: _Não_ usa IA para categorização. Os campos de categoria (CWE, etc.) ficarão como "UNKNOWN".
    - `--data-source nvd`: Usa _apenas_ o NVD.
    - Não precisa de chaves de API de LLMs.

3.  **Usando Gemini, Vulners e um arquivo com termos de busca:**

    Crie um arquivo `search_terms.txt` com o seguinte conteúdo (um termo por linha):

    ```
    OpenDDS
    RTI Connext DDS
    Eclipse Cyclone DDS
    ```

    Execute:

    ```bash
    python src/main.py --source gemini --data-source vulners --search-file search_terms.txt --vulners-key <SUA_CHAVE_VULNERS> --gemini-key <SUA_CHAVE_GEMINI> --output-file vulnerabilidades_gemini.csv
    ```

    - `--source gemini`
    - `--search-file`: Usa o arquivo `search_terms.txt`.

4.  **Usando Default, Vulners (e. g.) e um arquivo com termos de busca:**

    Crie um arquivo `search_terms.txt` com o seguinte conteúdo (um termo por linha):

    ```
    OpenDDS
    RTI Connext DDS
    Eclipse Cyclone DDS
    ```

    Execute:

    ```bash
    python src/main.py --source default --data-source vulners --search-file search_terms.txt --vulners-key <SUA_CHAVE_VULNERS> --default-key <SUA_CHAVE_DEFAULT> --default-model <MODELO_DEFAULT_LLM> --default-url <BASE_URL_DEFAULT> --output-file vulnerabilidades_default.csv
    ```

    - `--source default`
    - `--search-file`: Usa o arquivo `search_terms.txt`.

## Experimentos

Esta seção descreve como reproduzir os experimentos apresentados no artigo.

**Reivindicação #1 (Exemplo: Coleta e Categorização de Vulnerabilidades em DDS)**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas a DDS, pré-processá-los, extrair informações e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente (variáveis de ambiente ou argumentos de linha de comando).
     - Crie um arquivo (ex: `search_params_DDS.txt`) contendo os termos de busca relacionados a DDS (ou utilize o arquivo que está no diretório search_params/search_params_DDS.txt):

       ```
       Data Distribution Service (DDS)
       FastDDS
       RTI Connext DDS
       Open DDS
       Cyclone DDS
       IntercomDDS
       Coredx DDS
       Gurum DDS
       OpenSplice DDS
       MilDDS
       ```

  2. **Execução:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

     ```bash
       python src/main.py --source combined --data-source both --search-file search_params/search_params_DDS.txt --vulners-key <SUA_CHAVE_VULNERS> --gemini-key <SUA_CHAVE_GEMINI> --chatgpt-key <SUA_CHAVE_CHATGPT>  --llama-key <SUA_CHAVE_LLAMA> --export-format csv --output-file dataset/dds_vulnerabilities.csv
     ```

     - `--source combined`: Usa todos os LLMs (Gemini, ChatGPT, Llama) com votação ponderada.
     - `--data-source both`: Usa NVD e Vulners.
     - `--search-file search_params_dds.txt`: Usa o arquivo com os termos de busca.
     - `--output-file dds_vulnerabilities.csv`: Salva os resultados em `dds_vulnerabilities.csv`.

  3. **Verificação:**
     - Verifique se o arquivo `dataset/dds_vulnerabilities.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #2 (Exemplo: Análise de Protocolos de Roteamento em UAVs)**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar e analisar dados _específicos_ de protocolos de roteamento em UAVs.

- **Passos:**

  1. **Configuração:**

     - Crie um arquivo (ex: `search_params_UAV.txt`) contendo os termos de busca relacionados a protocolos de roteamento de UAVs (ou utilize o arquivo que está no diretório search_params/search_params_UAV.txt):

     ```
     AODV
     DSR
     OLSR
     GRP
     ```

  2. **Execução:**

     ```bash
     python src/main.py --source combined --data-source both --search-file search_params/search_params_UAV.txt --vulners-key <SUA_CHAVE_VULNERS> --gemini-key <SUA_CHAVE_GEMINI> --chatgpt-key <SUA_CHAVE_CHATGPT>  --llama-key <SUA_CHAVE_LLAMA> --export-format csv --output-file dataset/uav_vulnerabilities.csv

     ```

  3. **Verificação:**
     - Verifique se o arquivo `dataset/uav_vulnerabilities.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #3 (Estudo de Caso MQTT):**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas ao protocolo MQTT, pré-processá-los, extrair informações relevantes e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente (variáveis de ambiente ou argumentos de linha de comando).
     - Crie um arquivo (ex: `search_params_MQTT.txt`) contendo os termos de busca relacionados a MQTT:

       ```
       Eclipse Mosquitto
       EMQX
       VerneMQ
       RabbitMQ
       HiveMQ
       ```

  2. **Execução:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

     ```bash
     python src/main.py --source combined --data-source both --search-file search_params/search_params_MQTT.txt --vulners-key <SUA_CHAVE_VULNERS> --gemini-key <SUA_CHAVE_GEMINI> --chatgpt-key <SUA_CHAVE_CHATGPT>  --llama-key <SUA_CHAVE_LLAMA> --export-format csv --output-file dataset/mqtt_vulnerabilities.csv
     ```

     - `--source combined`: Usa todos os LLMs (Gemini, ChatGPT, Llama) com votação ponderada.
     - `--source provider`: Define o uso da lista de modelos de LLMs que está definida na configuração.
     - `--provider [providers]`: Lista os modelos de LLMs que usará e está definida na configuração.
     - `--data-source both`: Usa NVD e Vulners.
     - `--search-file search_params_MQTT.txt`: Usa o arquivo com os termos de busca.
     - `--output-file mqtt_vulnerabilities.csv`: Salva os resultados em `mqtt_vulnerabilities.csv`.

  3. **Verificação:**
     - Verifique se o arquivo `dataset/mqtt_vulnerabilities.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #4 (Estudo de Caso Navegadores Web):**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas a navegadores web (browsers), pré-processá-los, extrair informações relevantes e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente.
     - Crie um arquivo (ex: `search_params_BROWSERS.txt`) contendo os termos de busca relacionados a navegadores:

       ```
       Google Chrome Browser
       Microsoft Edge Browser
       Mozilla Firefox Browser
       Apple Safari Browser
       Opera Browser
       ```

  2. **Execução:**

     ```bash
     python src/main.py --source combined --data-source both --search-file search_params/search_params_BROWSERS.txt --vulners-key <SUA_CHAVE_VULNERS> --gemini-key <SUA_CHAVE_GEMINI> --chatgpt-key <SUA_CHAVE_CHATGPT> --llama-key <SUA_CHAVE_LLAMA> --export-format csv --output-file dataset/browsers_vulnerabilities.csv
     ```

     - `--source combined`: Usa todos os LLMs.
     - `--data-source both`: Usa NVD e Vulners.
     - `--search-file search_params_browsers.txt`: Usa o arquivo com os termos de busca.
     - `--output-file browsers_vulnerabilities.csv`: Salva os resultados em `browsers_vulnerabilities.csv`.

     ```bash
     python .\src\main.py --source provider --provider "meta" "google" "deepseek"  --data-source 'nvd' --search-params 'opendds' --export-format csv --output-file vulnerabilities.csv 
     ```

     - `--source provider`: Usa as LLMs definidas no `--provider`  os LLMs.
     - `--data-source 'nvd'`: Usa NVD or Vulners.
     - `--search-file search_params_browsers.txt`: Usa o arquivo com os termos de busca.
     - `--output-file vulnerabilities.csv`: Salva os resultados em `deepseek_vulnerabilities.csv google_vulnerabilities.csv e meta_vulnerabilities.csv`.

  3. **Verificação:**
     - Verifique se o arquivo `dataset/browsers_vulnerabilities.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Observações Gerais (para todos os estudos de caso):**

- **Reprodutibilidade:** Os resultados _exatos_ podem variar um pouco devido a:
  - **Atualizações nas bases de dados:** O NVD e o Vulners são _constantemente atualizados_. Novas vulnerabilidades podem ser adicionadas, e as informações sobre vulnerabilidades existentes podem ser modificadas.
  - **Estocasticidade dos LLMs:** Os LLMs (Gemini, ChatGPT, Llama) _não são completamente determinísticos_. Pequenas variações nas respostas são esperadas, mesmo com o mesmo prompt e os mesmos dados de entrada. O sistema de votação ponderada ajuda a mitigar isso, mas não elimina _completamente_ a variabilidade.
- **Tempo de Execução:** A coleta de dados, especialmente do Vulners, e a categorização com os LLMs _podem levar um tempo considerável_ (dependendo do número de termos de busca, da quantidade de vulnerabilidades encontradas e da velocidade da sua conexão com a internet e das APIs). Seja paciente.
- **Erros/Exceções:**
- O código fornecido tem _algum_ tratamento de erros (e.g., `try...except` para chamadas de API), mas _não é exaustivo_. É _possível_ que ocorram erros durante a execução (e.g., problemas de conexão, limites de taxa de API, etc.).
- Se ocorrerem erros, _leia atentamente as mensagens de erro_. Elas podem fornecer pistas sobre o problema.
- Verifique se as _chaves de API_ estão corretas e se você _não atingiu os limites de uso_ das APIs.
- Verifique sua conexão com a internet\_.
- **Dados de Saída:**
  - Os arquivos CSV gerados terão as colunas especificadas no código (`id`, `title`, `description`, `vendor`, `cwe_category`, etc.).
  - Os valores para `cwe_category`, `explanation`, `vendor`, `cause` e `impact` serão preenchidos pelos LLMs (ou "UNKNOWN" se a categorização falhar).
  - Os valores para `published`, `cvss_score`, `severity` e `source` virão das fontes de dados (NVD ou Vulners).

## Docker

Você também pode executar o script usando Docker.

### Dockerfile

```dockerfile
# Use uma imagem oficial do Python como imagem base
FROM python:3.10-slim

# Defina o diretório de trabalho no contêiner
WORKDIR /app

# Copie o conteúdo do diretório atual para o contêiner em /app
COPY . /app

# Instale os pacotes necessários especificados em requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Defina a variável de ambiente
ENV NAME DDSBuilder

# Execute main.py quando o contêiner for iniciado
CMD ["python", "src/main.py"]
```

### Construir e Executar o Contêiner Docker

1.  **Construir a imagem:**

    ```bash
    docker build -t vbuilder .
    ```

2.  **Executar o container usando IA para categorização:**

    ```bash
    docker run vbuilder python src/main.py --source combined --data-source both --vulners-key <SUA_CHAVE_VULNERS> --gemini-key <SUA_CHAVE_GEMINI> --chatgpt-key <SUA_CHAVE_CHATGPT>  --llama-key <SUA_CHAVE_LLAMA>  --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS" "RTI Connext DDS"
    ```

3.  **Executar o container sem usar IA para categorização:**

    ```bash
    docker run --source none --data-source nvd --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS"
    ```

## Estrutura do Código

O código-fonte está organizado da seguinte forma:

- `categorization/`: Contém os módulos relacionados à categorização de vulnerabilidades com IA.
  - `categorizer.py`: Implementa a classe `Categorizer`, responsável por interagir com as APIs dos LLMs e combinar os resultados.
  - `__init__.py`
  - `voting.py`: Implementa um sistema de votação.
- `data_sources/`: Contém os módulos para extrair dados de diferentes fontes.
  - `nvd_extractor.py`: Funções para acessar a API do NVD.
  - `vulners_extractor.py`: Funções para acessar a API do Vulners.
  - `github_extractor.py`: (Atualmente não utilizado)
  - `__init__.py`
- `output/`: Contém os módulos para exportar os dados processados.
  - `csv_exporter.py`: Funções para exportar dados para CSV.
  - `__init__.py`
  - `json_exporter.py`: Funções para exportar dados para JSON.
- `processing/`: Contém módulos para processamento e normalização dos dados.
  - `filter.py`: Funções para filtrar as vulnerabilidades.
  - `normalizer.py`: Funções para normalizar os dados de diferentes fontes.
  - `load_data_source.py`:Carrega as fontes de dados.
  - `data_preprocessor.py`: Orquestra o pré-processamento dos dados. -`__init__.py`
- `src/`: Contém o script principal.
  - `main.py`: Ponto de entrada principal do programa.
- `requirements.txt`: Lista as dependências do projeto.
- `README.md`: Este arquivo.
- search-params-\*.txt: Arquivos contendo termos para pesquisa.
- config.yaml: Arquivo de configuração.

## Extensibilidade

O VulnBuilderAI foi projetado para ser extensível, permitindo a adição de novas fontes de dados, normalizadores e formatos de saída de forma simples e organizada. A arquitetura modular da ferramenta facilita a integração de novos componentes sem a necessidade de modificar o código principal. A seguir, descrevemos como adicionar novas fontes de dados e novos formatos de saída.

### Adicionando Novas Fontes de Dados

Para adicionar uma nova fonte de dados, siga os seguintes passos:

1.  **Crie um Novo Módulo Extractor:**

    - Dentro do diretório `data_sources/`, crie um novo arquivo Python com um nome descritivo para a nova fonte de dados, seguindo o padrão `nova_fonte_extractor.py`. Por exemplo, se você deseja adicionar uma fonte chamada "MySource", crie o arquivo `data_sources/mysource_extractor.py`.

2.  **Implemente a Classe Extractor:**

    - Dentro do novo arquivo (e.g., `mysource_extractor.py`), crie uma classe que herde da classe base `DataSourceBase` (definida em `data_sources/data_source.py`). Isso garante que a nova fonte de dados siga a interface esperada pela ferramenta.
    - Implemente o método `collect_data(self, search_params)`:

      - Este método é responsável por _coletar_ os dados da nova fonte.
      - Ele recebe uma lista de `search_params` (termos de busca).
      - Ele deve _retornar_ uma lista de _dicionários_, onde cada dicionário representa uma vulnerabilidade (ainda em um formato _bruto_, sem normalização). _Não se preocupe com o formato dos dados neste ponto; a normalização será feita posteriormente._
      - Use a biblioteca `requests` para fazer as requisições HTTP, se necessário. _Lembre-se de tratar erros e exceções (conexão, rate limits, etc.) de forma adequada._
      - Se a nova fonte de dados tiver sua própria API, use essa API. Se for uma página web, você pode usar bibliotecas como `BeautifulSoup` para fazer o parsing do HTML.
      - Exemplo:

        ```python
        # data_sources/mysource_extractor.py
        import requests
        from .data_source import DataSourceBase

        class MySourceExtractor(DataSourceBase):
            async def collect_data(self, search_params):
                vulnerabilities = []
                for param in search_params:
                    try:
                        # Exemplo de chamada de API (substitua pela lógica real)
                        response = requests.get(f"https://api.mysource.com/vulnerabilities?q={param}")
                        response.raise_for_status()  # Lança exceção se erro HTTP
                        data = response.json()
                        # Adapte a lógica de extração para o formato da sua fonte
                        vulnerabilities.extend(data.get('vulnerabilities', [])) #Adiciona no fim
                    except requests.exceptions.RequestException as e:
                        print(f"Erro ao coletar dados da MySource para '{param}': {e}")
                return vulnerabilities

            def normalize_data(self, vulnerability):
              #Esta função é criada na etapa 5.
        ```

3.  **Atualize o Arquivo de Configuração:**

    - Adicione a nova fonte de dados ao arquivo `config.yaml`:

    ```yaml
    data_sources:
      - nvd
      - vulners
      - mysource

      normalizers:
      - basic

      exporters:
      - csv
      - json
    ```

### Adicionando Novos Formatos de Saída

Para adicionar um novo formato de saída, siga os seguintes passos:

1.  **Crie um Novo Módulo Exporter:**

    - Dentro do diretório output/, crie um novo arquivo Python com um nome descritivo para o novo formato de saída, seguindo o padrão novo_formato_exporter.py. Por exemplo, se você deseja adicionar um formato chamado "XML", crie o arquivo `output/xml_exporter.py`. Por exemplo, se você deseja adicionar um formato chamado "XML", crie o arquivo `output/xml_exporter.py`.

2.  **Implemente a Classe Exporter:**

    - Dentro do novo arquivo `(e.g., xml_exporter.py)`, crie uma classe que herde da classe base `DataExporterBase` (definida em `output/data_exporter.py`). Isso garante que o novo formato de saída siga a interface esperada pela ferramenta.
    - Implemente o método `export(self, data, filename)`:

      - Este método é responsável por exportar os dados no novo formato.
      - Ele recebe os dados a serem exportados e o nome do arquivo de saída.
      - Exemplo:

        ```python

        # output/xml_exporter.py

        import xml.etree.ElementTree as ET
        from .data_exporter import DataExporterBase

        class XmlExporter(DataExporterBase):
          def export(self, data, filename):
             root = ET.Element("Vulnerabilities")
            for item in data:
              vuln_elem = ET.SubElement(root, "Vulnerability")
               for key, value in item.items():
                child = ET.SubElement(vuln_elem, key)
                child.text = str(value)
            tree = ET.ElementTree(root)
          tree.write(filename, encoding='utf-8', xml_declaration=True
        ```

3.  **Atualize o Arquivo de Configuração:**

    - Adicione o novo formato de saída ao arquivo `config.yaml`:

    ```yaml
    data_sources:
      - nvd
      - vulners
      - mysource

      normalizers:
      - basic

      exporters:
      - csv
      - json
      - xml
    ```

## Licença

Este projeto está licenciado sob a Licença GNU - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
