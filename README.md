# VulnSyncAI: PLN e LLMs para Construção e Atualização Contínua de Datasets de Vulnerabilidades

[![Licença](https://img.shields.io/badge/License-GNU%20GPL-blue)](https://opensource.org/licenses/GNU)

**Resumo do Artigo:**

_A construção e manutenção de datasets atualizados de vulnerabilidades enfrentam desafios como falta de padronização e necessidade de automação. Neste trabalho, apresentamos a VulnSyncAI, uma ferramenta modular que utiliza PLN e LLMs para correlacionar informações de múltiplas fontes, garantindo datasets atualizados e relevantes. A VulnSyncAI melhora a eficácia de modelos de IA na detecção de ameaças, automatizando processos e aumentando a eficiência na criação de datasets representativos._

---

## Estrutura do README.md

Este README.md está organizado nas seguintes seções:

1.  **Título e Resumo:** Título do projeto e um resumo conciso (cópia do resumo do artigo).
2.  **Funcionalidades:** Lista as principais funcionalidades da ferramenta.
3.  **Dependências:** Lista os requisitos de software (Python, APIs).
4.  **Preocupações com segurança:** Lista das preocupações com a segurança.
5.  **Instalação:** Instruções passo a passo para instalar a ferramenta.
6.  **Configuração:** Instruções para configurar as chaves de API.
7.  **Uso:** Descreve como reproduzir os experimentos apresentados no artigo..
8.  **Experimentos:** Explicação dos argumentos de linha de comando e exemplos de uso.
9.  **Docker (Opcional):** Instruções para construir e executar a ferramenta usando Docker.
10. **Estrutura do Código:** Breve visão geral da organização do código-fonte.
11. **Extensibilidade**: Como adicionar novas fontes e novos exportadores.
12. **Licença:** Informações sobre a licença do projeto.

---

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

## Dependências

- Python 3.8 ou superior.
- Chaves de API para os seguintes serviços (opcional, dependendo dos módulos e LLMs que você for usar):
  - **Vulners:** Obtenha uma chave em [https://vulners.com/](https://vulners.com/)
  - **HugginFace:** Obtenha uma chave em [https://huggingface.co](https://huggingface.co/)
  - **Google Gemini:** Obtenha uma chave em [https://ai.google.dev/](https://ai.google.dev/)
  - **OpenAI ChatGPT:** Obtenha uma chave em [https://platform.openai.com/](https://platform.openai.com/)
  - **Llama (Meta):** Obtenha uma chave em [https://llama-api.com/](https://llama-api.com/)

## Preocupações com segurança

Caso a execução do artefato ofereça qualquer tipo de risco, esta seção detalha os potenciais perigos e descreve os processos necessários para garantir a segurança dos avaliadores.

**Riscos Potenciais**

1.  **Uso de Recursos Externos:**

- Dependências externas ou APIs podem expor chaves de autenticação ou dados sensíveis, caso não sejam configuradas adequadamente.
- É importante assegurar que qualquer dado enviado a terceiros esteja em conformidade com políticas de privacidade e segura

1. **Execução de Código:**

- O uso de scripts automatizados, especialmente aqueles com permissões elevadas, pode representar riscos se forem configurados incorretamente.
- Erros no código podem levar ao uso indevido de recursos, como consumo excessivo de CPU/GPU ou perda de dados.

3. **Manipulação de Dados Brutos:**

- Dados não sanitizados podem conter informações prejudiciais ou maliciosas, representando um risco para o sistema onde são processados.

**Medidas de Segurança**

1. **Gerenciamento de Chaves de API:**

- Assegura que as chaves de API sejam armazenadas em variáveis de ambiente e nunca diretamente no código, na config.yaml cuidado com o envio da ´api_key´. Essa configuração é estrito para testes.
- Exemplo de configuração:
  ```yaml
  type: "api"
  provider: "llama2"
  site: "https://api.llama-api.com"
  api_key: "api_key"
  ```

2. **Execução em Ambientes Isolados:**

- Utiliza ambientes virtuais ou contêineres (e.g., Docker) para isolar a execução do artefato.
- Recomendação para criar um contêiner:

  ```bash
    docker build -t vuln-builder-ai .
    docker run -p 8000:8000 vuln-builder-ai
  ```

3. **Documentação de Restrições:**

- Informa aos revisores quaisquer restrições ou pré-requisitos para garantir a execução segura do artefato.

**Responsabilidade**

- Todos os scripts fornecidos foram projetados para minimizar riscos à segurança. No entanto, é responsabilidade do usuário garantir que o ambiente de execução seja seguro e que as práticas recomendadas descritas acima sejam seguidas.

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
      pip install transformers
      pip install psutil
      pip install requests
      pip install huggingface_hub
    ```

## Configuração

Você pode configurar o VulnBuilderAI usando _variáveis de ambiente_ ou _argumentos de linha de comando_. A ordem de prioridade é: argumentos de linha de comando > variáveis de ambiente.

1.  **Arquivo de configuração (opcional):**
    _Não implementado no código fornecido._ Se você quisesse adicionar um arquivo de configuração (e.g., `config.ini` ou `config.yaml`), precisaria modificar o código (`main.py`) para ler as configurações desse arquivo.

## Uso

### Argumentos de Linha de Comando

```bash
python src/main.py --provider <ai_provider> --data-source <data_source> --export-format <format> --output-file <filename>  --search-params <params> --search-file <file_path>
```

- `--provider`: **Obrigatório.** Seleciona o provedor de IA para categorização. Opções:
  - `google`: Usa o Google Gemini.
  - `chatgpt`: Usa o OpenAI ChatGPT.
  - `llama`: Usa o Meta Llama.
  - `....`: Como a ferramenta é extensível é possível adicionar vários modelos de IA.
  - `none`: _Não_ usa IA para categorização (útil para coletar e normalizar dados sem categorizar).
- `--data-source`: **Obrigatório.** Seleciona a fonte de dados de vulnerabilidades. Opções:
  - `nvd`: Usa o National Vulnerability Database (NVD).
  - `vulners`: Usa a API do Vulners.
  - `....`: Como a ferramenta é extensível é possível adicionar vários fontes de dados.
  - `both`: Usa _ambas_ as fontes (NVD e Vulners).
- `--export-format`: Formato de exportação dos dados. Opções:
  - `csv`: Arquivo CSV (Comma-Separated Values).
  - `json`: Arquivo JSON.
  - O padrão é `csv`.
- `--output-file`: Nome do arquivo de saída (e caminho, se necessário). O padrão é `dataset/dds_vulnerabilities_AI.csv`.
- `--search-params`: Parâmetros de busca para vulnerabilidades (palavras-chave separadas por espaço). _Exemplo:_ `"OpenDDS" "RTI Connext DDS"`
- `--search-file`: Caminho para um arquivo _de texto_ contendo os parâmetros de busca (uma palavra-chave ou frase por linha). _Exemplo:_ `search_params.txt`

### Exemplos de Comando

1.  **Usando Google Gemini 1.5 Pro para categorização, com a fonte de dados NVD e múltiplos termos de busca:**

    ```bash
    python src/main.py --provider 'google' --data-source 'nvd' --search-params "OpenDDS" "RTI Connext DDS" --export-format csv --output-file vulnerabilidades.csv
    ```

    - `--provider`: Usa Gemini, ChatGPT e Llama, com votação.
    - `--data-source both`: Usa NVD e Vulners.
    - `--search-params`: Busca por vulnerabilidades relacionadas a "OpenDDS" _e_ "RTI Connext DDS".
    - As chaves de API são fornecidas.
    - O resultado é salvo em `vulnerabilidades.csv`.

2.  **Sem IA, usando apenas o NVD:**

    ```bash
    python src/main.py --provider 'none' --data-source 'nvd' --search-params "OpenDDS" --export-format csv --output-file vulnerabilidades_nvd.csv
    ```

3.  **Usando Gemini, Vulners e um arquivo com termos de busca:**

    Crie um arquivo `search_terms.txt` com o seguinte conteúdo (um termo por linha):

    ```
    OpenDDS
    RTI Connext DDS
    Eclipse Cyclone DDS
    ```

    Execute:

    ```bash
    python src/main.py --provider 'gemini' --data-source 'vulners' --search-file search_terms.txt --output-file vulnerabilidades_gemini.csv
    ```

## Experimentos

Esta seção descreve como reproduzir os experimentos apresentados no artigo.

**Reivindicação #1 (Coleta e Categorização de Vulnerabilidades em DDS)**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas a DDS, pré-processá-los, extrair informações e categorizá-los usando Gemini Pro 1.5 e Llama3 (DeepHermes-3-Llama-3-8B-Preview3).

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, HuggingFace) estão configuradas corretamente no arquivo config.yaml.
     - Crie um arquivo (ex: `search_params_DDS.txt`) contendo os termos de busca relacionados a DDS (ou utilize o arquivo que está no diretório search_params/search_params_DDS.txt):

       ```txt
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

  2. **Execução para o cenário de categorização do Gemini 1.5 Pro fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

     ```bash
       python src/main.py --provider 'google' --data-source 'nvd' --search-file search_files/search-params_DDS.txt --export-format csv --output-file DDS_vulnerabilities_categorized-NVD-GEMINI-API.csv
     ```

  3. **Execução para o cenário de categorização do Llam3 (DeepHermes-3-Llama-3-8B-Preview3) fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'llama3' --data-source 'nvd' --search-file search_files/search-params_DDS.txt --export-format csv --output-file DDS_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv
  ```

  4. **Verificação:**
     - Verifique se os arquivos `google_dataset/DDS_vulnerabilities_categorized-NVD-GEMINI-API.csv` e `llama3_dataset/DDS_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv` foram criados.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #2 (Exemplo: Análise de Protocolos de Roteamento em UAVs)**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar e analisar dados _específicos_ de protocolos de roteamento em UAVs.

- **Passos:**

  1. **Configuração:**

     - Crie um arquivo (ex: `search_params_UAV.txt`) contendo os termos de busca relacionados a protocolos de roteamento de UAVs (ou utilize o arquivo que está no diretório search_params/search_params_UAV.txt):

     ```txt
     AODV
     DSR
     OLSR
     GRP
     ```

  2. **Execução para o cenário de categorização do Gemini 1.5 Pro fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

  ```bash
    python src/main.py --provider 'google' --data-source 'nvd' --search-file search_files/search_params_UAV.txt --export-format csv --output-file UAV_vulnerabilities_categorized-GEMINI-API.csv
  ```

  3. **Execução para o cenário de categorização do Llam3 (DeepHermes-3-Llama-3-8B-Preview3) fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'llama3' --data-source 'nvd' --search-file search_files/search_params_UAV.txt --export-format csv --output-file UAV_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv
  ```

  4. **Verificação:**
     - Verifique se os arquivos `google_dataset/UAV_vulnerabilities_categorized-GEMINI-API.csv` e `llama3_dataset/UAV_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv` foram criados.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #3 (Estudo de Caso MQTT):**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas ao protocolo MQTT, pré-processá-los, extrair informações relevantes e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente (variáveis de ambiente ou argumentos de linha de comando).
     - Crie um arquivo (ex: `search_params_MQTT.txt`) contendo os termos de busca relacionados a MQTT:

       ```txt
       Eclipse Mosquitto
       EMQX
       VerneMQ
       RabbitMQ
       HiveMQ
       ```

  2. **Execução para o cenário de categorização do Gemini 1.5 Pro fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

  ```bash
    python src/main.py --provider 'google' --data-source 'nvd' --search-file search_files/search_params_MQTT.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-NVD-GEMINI-API.csv
  ```

  3. **Execução para o cenário de categorização do Gemini 1.5 Pro fonte de dados VULNERS:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

  ```bash
    python src/main.py --provider 'google' --data-source 'vulners' --search-file search_files/search_params_MQTT.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-VULNERS-GEMINI-API.csv
  ```

  4. **Execução para o cenário de categorização do Llam3 (DeepHermes-3-Llama-3-8B-Preview3) fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'llama3' --data-source 'nvd' --search-file search_files/search_params_MQTT.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv
  ```

  5. **Execução para o cenário de categorização do Llam3 (DeepHermes-3-Llama-3-8B-Preview3) fonte de dados VULNERS:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'llama3' --data-source 'vulners' --search-file search_files/search_params_MQTT.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-VULNERS-LLAMA3-LOCAL.csv
  ```

  6. **Execução para o cenário de categorização do DeepSeek (API) fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'deepseek' --data-source 'nvd' --search-file search_files/search_params_MQTT.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-NVD-DEEPSEEK.csv
  ```

  7. **Execução para o cenário de categorização do DeepSeek (API) fonte de dados VULNERS:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'deepseek' --data-source 'vulners' --search-file search_files/search_params_MQTT.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-VULNERS-DEEPSEEK.csv
  ```

  4. **Verificação:**
     - Verifique se os arquivos `google_dataset/MQTT_vulnerabilities_categorized-NVD-GEMINI-API.csv`,`google_dataset/MQTT_vulnerabilities_categorized-VULNERS-GEMINI-API.csv`,`llama3_dataset/MQTT_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv`, `llama3_dataset/MQTT_vulnerabilities_categorized-VULNERS-LLAMA3-LOCAL.csv`, `deekseek_dataset/MQTT_vulnerabilities_categorized-NVD-DEEPSEEK.csv` e `deekseek_dataset/MQTT_vulnerabilities_categorized-VULNERS-DEEPSEEK.csv` foram criados.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #4 (Estudo de Caso Navegadores Web):**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas a navegadores web (browsers), pré-processá-los, extrair informações relevantes e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente.
     - Crie um arquivo (ex: `search_params_BROWSERS.txt`) contendo os termos de busca relacionados a navegadores:

       ```txt
       Google Chrome Browser
       Microsoft Edge Browser
       Mozilla Firefox Browser
       Apple Safari Browser
       Opera Browser
       ```

  2. **Execução para o cenário de categorização do Gemini 1.5 Pro fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

  ```bash
    python src/main.py --provider 'google' --data-source 'nvd' --search-file search_files/search_params_UAV.txt --export-format csv --output-file BROWSERS_vulnerabilities_categorized-NVD-GEMINI-API.csv
  ```

  3. **Execução para o cenário de categorização do Llam3 (DeepHermes-3-Llama-3-8B-Preview3) fonte de dados NVD:** Execute o seguinte comando (adaptando os nomes dos arquivos se necessário):

  ```bash
    python src/main.py --provider 'llama3' --data-source 'nvd' --search-file search_files/search_params_UAV.txt --export-format csv --output-file BROWSERS_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv
  ```

  4. **Verificação:**
     - Verifique se os arquivos `google_dataset/BROWSERS_vulnerabilities_categorized-NVD-GEMINI-API.csv` e `llama3_dataset/BROWSERS_vulnerabilities_categorized-NVD-LLAMA3-LOCAL.csv` foram criados.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Observações Gerais (para todos os estudos de caso):**

- **Reprodutibilidade:** Os resultados _exatos_ podem variar um pouco devido a:
  - **Atualizações nas bases de dados:** O NVD e o Vulners são constantemente atualizados. Novas vulnerabilidades podem ser adicionadas, e as informações sobre vulnerabilidades existentes podem ser modificadas.
  - **Estocasticidade dos LLMs:** Os LLMs (Gemini, Llama, DeepSeek) não são completamente determinísticos*. Pequenas variações nas respostas são esperadas, mesmo com o mesmo prompt e os mesmos dados de entrada. O sistema de votação ponderada ajuda a mitigar isso, mas não elimina \_completamente* a variabilidade.
- **Tempo de Execução:** A coleta de dados, especialmente do Vulners, e a categorização com os LLMs _podem levar um tempo considerável_ (dependendo do número de termos de busca, da quantidade de vulnerabilidades encontradas e da velocidade da sua conexão com a internet e das APIs). Principalmente para rodar modelos locais, como Llama3 (DeepHermes-3-Llama-3-8B-Preview3)
- **Erros/Exceções:**
- O código fornecido tem _algum_ tratamento de erros (e.g., `try...except` para chamadas de API), mas _não é exaustivo_. É _possível_ que ocorram erros durante a execução (e.g., problemas de conexão, limites de taxa de API, etc.).
- Se ocorrerem erros, _leia atentamente as mensagens de erro_. Elas podem fornecer pistas sobre o problema.
- Verifique se as _chaves de API_ estão corretas e se você _não atingiu os limites de uso_ das APIs.
- Verifique sua conexão com a internet\_.
- **Dados de Saída:**
  - Os arquivos CSV gerados terão as colunas especificadas no código (`id`, `description`, `vendor`, `cwe_category`, etc.).
  - Os valores para `cwe_category`, `explanation`, `cause` e `impact` serão preenchidos pelos LLMs (ou "UNKNOWN" se a categorização falhar).
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
    docker run vbuilder python src/main.py --provider 'llama3' --data-source 'nvd' --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS" "RTI Connext DDS"
    ```

3.  **Executar o container sem usar IA para categorização:**

    ```bash
    docker run --provider 'none' --data-source nvd --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS"
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

### Adicionar Novo Modelo de Dados

Passos para Adicionar um Novo Modelo de Dados

1.  **Registrar o Modelo:**

    - Adicione o novo modelo ao arquivo config.yaml na seção models_to_evaluate:

    ```yaml
      models_to_evaluate:
    - model: "novo-modelo"
      type: "local"
      provider: "novo_provedor"
      config: "configurações_do_modelo"
    ```

2.  **Utilizar o Modelo:**

- Adicione o novo modelo ao arquivo config.yaml na seção models_to_evaluate:

  ```bash
  python src/main.py --provider 'novo_provedor' --data-source 'nvd' --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS" "RTI Connext DDS"
  ```

## Licença

Este projeto está licenciado sob a Licença GNU - veja o arquivo [LICENSE](LICENSE) para mais detalhes.
