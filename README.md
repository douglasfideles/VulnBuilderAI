# VulnBuilderAI: Ferramenta Multiplataforma para Construção de Datasets de Vulnerabilidades com Categorização por IA

[![Licença](https://img.shields.io/badge/License-GNU%20GPL-blue)](https://opensource.org/licenses/GNU)

**Resumo do Artigo:**

_Este projeto apresenta o VulnBuilderAI, uma ferramenta para construir datasets de vulnerabilidades de software. A ferramenta coleta dados de múltiplas fontes, normaliza, extrai informações relevantes usando PLN (incluindo LLMs) e categoriza as vulnerabilidades. O objetivo é gerar datasets de alta qualidade para pesquisa e prática em segurança de software._

---

## Estrutura do README.md

Este README.md está organizado nas seguintes seções:

1.  **Título e Resumo:** Título do projeto e um resumo conciso (cópia do resumo do artigo).
2.  **Estrutura do README.md:** Estrutura do presente README.md.
3.  **Selos:** Estrutura com os Selos Considerados
3.  **Informações básicas:** Esta seção deve apresentar informações básicas de todos os componentes necessários para a execução e replicação dos experimentos. Descrevendo todo o ambiente de execução, com requisitos de hardware e software.
4.  **Depêndencias:** Informações relacionadas a benchmarks utilizados e dependências para a execução são descritas nesta seção. 
Buscou-se deixar o mais claro possível, apresentando informações como versões de dependências e processos para acessar recursos de terceiros caso necessário.
5.  **Preocupações com segurança:** Lista das preocupações com a segurança.
6.  **Instalação:** O processo de baixar e instalar a aplicação deve ser descrito nesta seção.
7.  **Teste mínimo:** Explicação dos argumentos de linha de comando e exemplos de uso local e por API.
8.  **Experimentos:** Descreve um passo a passo para a execução e obtenção dos resultados do artigo. Permitindo que os revisores consigam alcançar as reivindicações apresentadas no artigo. 
9. **Licença:** Informações sobre a licença do projeto.
10. **Revisão Sistêmica da Ferramenta:** Uma revisão mais aprofundada da Ferramenta.
--- 

## Selos Considerados
Os selos considerados no processo de avaliação são: **Disponíveis**, **Funcionais**, **Sustentáveis** e **Experimentos Reprodutíveis**.

# Informações Básicas

Esta seção apresenta todos os componentes essenciais que foram necessários para a execução e replicação dos experimentos, incluindo detalhes sobre o ambiente de execução e os requisitos de hardware e software.


- **Ambiente de Execução**
  - Os experimentos para executar os estudos de casos usando a API do Gemini e DeepSeek foram realizados em um computador com processador Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz   2.81 GHz (4 núcleos) e 16GB de memória RAM, rodando o sistema opera-cional Windows 10 Home. 
  - **Sistemas Operacionais Suportados:**
    - Windows 10 ou superior

  - Para rodar o estudo de caso rodando a configuração local do Llama3 (DeepHermes-3-Llama-3-8B-Preview3) foram usados uma máquina virtual (VMs) na Google Cloud com a seguinte configuração: e2-custom-12-40960 (12 vCPUs, 40 GB de memória), Ubuntu-2004-focal-v20250213.
  - **Sistemas Operacionais Suportados:**
    - Ubuntu 20.04 LTS (ou equivalente com suporte a Python 3.10)

- **Arquitetura:** x86_64.
- **Linguagem de Programação:** Python 3.10.

**Requisitos de Hardware API**

- **CPU:** Processador com no mínimo 4 núcleos (recomendado Intel i5 ou equivalente).
- **Memória RAM:** Mínimo de 8 GB (16 GB recomendados para grandes volumes de dados).
- **Espaço em Disco:** Pelo menos 10 GB livres para armazenamento de dados e dependências.
- **GPU (opcional):** GPU com suporte a CUDA (recomendado para uso com `torch` e treinamentos de modelos).
- **Ambiente do Estudo de Caso:**
  - **Processador:** Intel(R) Core(TM) i7-7700HQ CPU @ 2.80GHz 2.81GHz (4 núcleos).
  - **Memória RAM:** 16 GB.
  - **Sistema Operacional:** Windows 10 Home.

**Requisitos de Hardware Local Google Cloud**

- **CPU:** Processador com no mínimo 12 vCPUs núcleos.
- **Memória RAM:** Mínimo de 8 GB (16 GB recomendados para grandes volumes de dados.
- **Espaço em Disco:** Pelo menos 10 GB livres para armazenamento de dados e dependências.
- **GPU (opcional):** Não utilizada, execução por CPU.
- **Ambiente do Estudo de Caso:**
  - **Processador:** e2-custom-12-40960).
  - **Memória RAM:** 40 GB.
  - **Sistema Operacional:** Ubuntu 20.04 LTS, arquiteturas x86_64.

**Requisitos de Software**

- **Python 3.10:** Certifique-se de que está instalado no sistema.
- **Gerenciador de Pacotes:** `pip` ou equivalente para instalação das dependências.
- **Ferramentas Adicionais:**
  - Git para clonagem do repositório.
  - Ambiente virtual (opcional, mas recomendado) para isolamento do projeto.
---

Esta seção foi estruturada para fornecer clareza total sobre todas as dependências envolvidas, garantindo que os experimentos sejam reprodutíveis e acessíveis. Se precisar de mais informações ou ajustes, posso complementar! 😊


---
## Dependências de Software

Abaixo estão listadas as principais bibliotecas e ferramentas necessárias, bem como suas versões:

- `requests`: versão 2.31.0
- `google-generativeai`: versão 0.1.3
- `openai`: versão 0.27.2
- `transformers`: versão 4.27.4
- `psutil`: versão 5.9.4
- `huggingface_hub`: versão 0.13.3
- `torch`: versão 2.0.0

## Preocupações com segurança

Caso a execução do artefato ofereça qualquer tipo de risco, esta seção detalha os potenciais perigos e descreve os processos necessários para garantir a segurança dos avaliadores.

**Riscos Potenciais**

1. **Uso de Recursos Externos:**
   - Dependências externas ou APIs podem expor chaves de autenticação ou dados sensíveis, caso não sejam configuradas adequadamente.
   - É importante assegurar que qualquer dado enviado a terceiros esteja em conformidade com políticas de privacidade e segurança.

2. **Execução de Código:**
   - O uso de scripts automatizados, especialmente aqueles com permissões elevadas, pode representar riscos se forem configurados incorretamente.
   - Erros no código podem levar ao uso indevido de recursos, como consumo excessivo de CPU/GPU ou perda de dados.

3. **Manipulação de Dados Brutos:**
   - Dados não sanitizados podem conter informações prejudiciais ou maliciosas, representando um risco para o sistema onde são processados.

**Medidas de Segurança**

1. **Gerenciamento de Chaves de API:**
   - Assegura que as chaves de API sejam armazenadas em variáveis de ambiente e nunca diretamente no código.
   - Exemplo de configuração:
     ```bash
     export API_KEY="SUA_CHAVE_SEGURA_AQUI"
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

## Instalação e Execução
1. Clone o repositório:
   ```bash
   git clone https://github.com/seuprojeto/seurepositorio.git
   cd seurepositorio

**Pré-requisitos**

- Python 3.8 ou superior.
- Chaves de API para os seguintes serviços (opcional, dependendo dos módulos e LLMs que você for usar):
  - **Vulners:** Obtenha uma chave em [https://vulners.com/](https://vulners.com/)
  - **Google Gemini:** Obtenha uma chave em [https://ai.google.dev/](https://ai.google.dev/)
  - **OpenAI ChatGPT:** Obtenha uma chave em [https://platform.openai.com/](https://platform.openai.com/)
  - **Llama (Meta):** Obtenha uma chave em [https://llama-api.com/](https://llama-api.com/)

**Instalação**

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

**Configuração**

Você pode configurar o VulnBuilderAI usando _variáveis de ambiente_ ou _argumentos de linha de comando_. A ordem de prioridade é: argumentos de linha de comando > variáveis de ambiente.

1.  **Arquivo de configuração (opcional):**
    _Não implementado no código fornecido._ Se você quisesse adicionar um arquivo de configuração (e.g., `config.ini` ou `config.yaml`), precisaria modificar o código (`main.py`) para ler as configurações desse arquivo.

### Teste mínimo

1.  **Usando todas as IAs, ambas as fontes e múltiplos termos de busca:**

    ```bash
    python src/main.py --provider 'gemini' --data-source both --search-params "OpenDDS" "RTI Connext DDS" --export-format csv --output-file vulnerabilidades.csv
    ```

    - `--provider 'gemini' `: Usa provider 'gemini' para definir Gemini como classificador.
    - `--data-source both`: Usa NVD e Vulners.
    - `--search-params`: Busca por vulnerabilidades relacionadas a "OpenDDS" _e_ "RTI Connext DDS".
    - `--export-format csv`: Exporta para csv, também possível json
    - O resultado é salvo em `vulnerabilidades.csv`.

2.  **Sem IA, usando apenas o NVD:**

    ```bash
    python src/main.py ==provider none --data-source nvd --search-params "OpenDDS" --export-format csv --output-file vulnerabilidades_nvd.csv
    ```

    - `--provider none`: _Não_ usa IA para categorização. Os campos de categoria (CWE, etc.) ficarão como "UNKNOWN".
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
    python src/main.py --provider 'gemini' --data-source 'vulners' --search-file search_terms.txt --output-file vulnerabilidades_gemini.csv
    ```

    - `--provider gemini`
    - `--search-file`: Usa o arquivo `search_terms.txt`.

## Experimentos

Esta seção descreve como reproduzir os experimentos apresentados no artigo.

**Reivindicação #1 (Exemplo: Coleta e Categorização de Vulnerabilidades em Browsers local)**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas a DDS, pré-processá-los, extrair informações e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente (variáveis de ambiente ou argumentos de linha de comando).
     - Crie um arquivo (ex: `search_params_Browsers.txt`) contendo os termos de busca relacionados a DDS (ou utilize o arquivo que está no diretório search_params/search_params_DDS.txt):

       ```       
      Google Chrome Browser
      Microsoft Edge Browser
      Mozilla Firefox Browser
      Apple Safari Browser
      Opera Browser
       ```

  2. **Execução:** Execute o seguinte comando (adaptando os nomes dos arquivos e as chaves de API, se necessário):

     ```bash
       python3 src/main.py --provider "llama3"  --data-source 'nvd'  --search-file search-params_BROWSERS.txt --export-format csv --output-file vulners4.csv


     ```

     - `--provider llama3`: Usa todos os LLMs (Llama 3).
     - `--data-source nvd`: Usa NVD .
     - `--search-file search_params_Browser.txt`: Usa o arquivo com os termos de busca.
     - `--output-file vulners4.csv`: Salva os resultados em `vulners4.csv`.

  3. **Verificação:**
     - Verifique se o arquivo `llama3_dataset/vulners4.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #2 (Estudo de Caso MQTT local):**

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
      python3 src/main.py --provider llama3 --data-source 'vulners' --search-file serrch.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv

     ```

     - `--provider llama3`: Usa o LLMs (Llama).
     - `--data-source vulners`: Usa Vulners.
     - `--search-file search_params_MQTT.txt`: Usa o arquivo com os termos de busca.
     - `--output-file MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv`: Salva os resultados em `llama3_dataset/MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv`.

  3. **Verificação:**
     - Verifique se o arquivo `llama3_dataset/MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

**Reivindicação #3 (Estudo de Caso MQTT Api):**

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
      python3 src/main.py --provider llama3 --data-source 'vulners' --search-file serrch.txt --export-format csv --output-file MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv

     ```

     - `--provider llama3`: Usa o LLMs (Llama).
     - `--data-source vulners`: Usa Vulners.
     - `--search-file search_params_MQTT.txt`: Usa o arquivo com os termos de busca.
     - `--output-file MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv`: Salva os resultados em `llama3_dataset/MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv`.

  3. **Verificação:**
     - Verifique se o arquivo `llama3_dataset/MQTT_vulnerabilities_categorized-LOCAL-LLM-VULNERS.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).


**Reivindicação #4 (Estudo de Caso Navegadores Web por API):**

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
     python src/main.py --provider 'gemini' --data-source 'nvd' --search-file search_files/search-params_BROWSERS.txt --export-format csv --output-file BROWSERS_vulnerabilities_categorized-GEMINI.csv

     ```

     - `--provider combined`: Usa todos os LLMs.
     - `--data-source nvd`: Usa NVD.
     - `--search-file search_files/search_params_browsers.txt`: Usa o arquivo com os termos de busca.
     - `--output-file BROWSERS_vulnerabilities_categorized-GEMINI.csv`: Salva os resultados em `gemini_dataset/BROWSERS_vulnerabilities_categorized-GEMINI.csv`.

     
  3. **Verificação:**
     - Verifique se o arquivo `dataset/browsers_vulnerabilities.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).



**Reivindicação #5 (Estudo de Caso UAV por API):**

- **Objetivo:** Demonstrar a capacidade da ferramenta de coletar dados de vulnerabilidades relacionadas a navegadores web (browsers), pré-processá-los, extrair informações relevantes e categorizá-los usando LLMs.

- **Passos:**

  1. **Configuração:**

     - Certifique-se de que as chaves de API (Vulners, Gemini, ChatGPT, Llama) estão configuradas corretamente.
     - Crie um arquivo (ex: `search_params_UAV.txt`) contendo os termos de busca relacionados a navegadores:

       ```
        AODV
        DSR
        OLSR

       ```

  2. **Execução:**

     ```bash
     python src/main.py --provider 'gemini' --data-source 'nvd' --search-file search_files/search-params_UAV.txt --export-format csv --output-file UAV_vulnerabilities_categorized-GEMINI.csv

     ```

     - `--provider gemini`: Usa todos os LLMs.
     - `--data-source nvd`: Usa NVD.
     - `--search-file search_files/search_params_UAV.txt`: Usa o arquivo com os termos de busca.
     - `--output-file UAV_vulnerabilities_categorized-GEMINI.csv`: Salva os resultados em `gemini_dataset/UAV_vulnerabilities_categorized-GEMINI.csv`.

     
  3. **Verificação:**
     - Verifique se o arquivo `gemini_dataset UAV_vulnerabilities_categorized-GEMINI.csv` foi criado.
     - Abra o arquivo e verifique se ele contém os dados esperados:
       - Colunas com os campos básicos (ID, título, descrição, etc.).
       - Colunas adicionais com as categorias extraídas pelos LLMs (CWE, explicação, fornecedor, causa, impacto).
       - Os valores devem corresponder, aproximadamente, aos resultados apresentados nas tabelas e gráficos do artigo (pequenas variações são esperadas devido à natureza estocástica dos LLMs).

## Licença

- Este projeto está licenciado sob os termos da [MIT License](https://opensource.org/licenses/MIT). Isso significa que você pode usar, modificar e distribuir este software conforme os termos da licença, desde que a atribuição original seja mantida.

- Consulte o arquivo [LICENSE](LICENSE) para obter mais detalhes.

## Revisão sistêmica

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
    docker run vbuilder python src/main.py --provider provider --data-source both --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS" "RTI Connext DDS"
    ```

3.  **Executar o container sem usar IA para categorização:**

    ```bash
    docker run --provider none --data-source nvd --export-format csv --output-file vulnerabilidades.csv --search-params "OpenDDS"
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
