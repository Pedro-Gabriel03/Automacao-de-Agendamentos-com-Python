# Automação de Agendamentos com Python

Projeto demonstrativo de automação de processos de agendamento utilizando Python, Selenium e Pandas.

A aplicação realiza a leitura de registros em uma planilha Excel e automatiza etapas de preenchimento de formulários web, validação de informações e atualização de status.

## Funcionalidades

- Leitura de dados a partir de planilhas Excel
- Identificação de registros pendentes
- Preenchimento automatizado de formulários web
- Validação de dados antes do processamento
- Seleção de datas e horários disponíveis
- Atualização do status dos registros processados
- Tratamento de erros durante a execução

## Tecnologias utilizadas

- Python
- Selenium
- Pandas
- PyAutoGUI
- OpenPyXL
- python-dotenv

## Estrutura do projeto

```text
automacao-agendamento/
├── automacao_agendamento_demo.py
├── dados_agendamento_exemplo.xlsx
├── .env.example
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.10 ou superior
- Google Chrome
- ChromeDriver compatível com a versão do navegador
- Acesso autorizado ao sistema utilizado na automação

## Instalação

Clone o repositório:

```bash
git clone https://github.com/SEU-USUARIO/automacao-agendamento-python.git
```

Entre na pasta:

```bash
cd automacao-agendamento-python
```

Crie um ambiente virtual:

```bash
python -m venv venv
```

Ative o ambiente virtual no Windows:

```bash
venv\Scripts\activate
```

Instale as dependências:

```bash
pip install pandas openpyxl selenium pyautogui python-dotenv
```

## Configuração

Crie um arquivo `.env` na raiz do projeto, utilizando o `.env.example` como referência.

Configure as variáveis necessárias:

```env
AGENDAMENTO_LOGIN=usuario
AGENDAMENTO_SENHA=senha
AGENDAMENTO_URL=https://sistema-exemplo.invalid
AGENDAMENTO_CNPJ=00000000000000
AGENDAMENTO_NAVIO=NAVIO EXEMPLO
```

As credenciais devem ser fornecidas localmente e não devem ser compartilhadas ou enviadas ao GitHub.

## Planilha de dados

O projeto acompanha uma planilha demonstrativa chamada `dados_agendamento_exemplo.xlsx`.

A planilha possui os seguintes campos:

| Campo | Descrição |
|---|---|
| CONTAINER | Identificador do contêiner |
| ARMADOR | Empresa responsável pelo transporte |
| TAMANHO | Tipo ou tamanho do contêiner |
| CPF | Documento utilizado no formulário |
| CAVALO | Placa do veículo |
| STATUS | Situação do registro |

Os dados disponibilizados neste repositório são fictícios e destinados exclusivamente à demonstração.

## Execução

Após configurar as variáveis de ambiente e a planilha:

```bash
python automacao_agendamento_demo.py
```

A automação abrirá o navegador e iniciará o processamento dos registros pendentes.

## Segurança

Este repositório contém uma versão demonstrativa do projeto.

- Não contém credenciais reais.
- Utiliza dados fictícios na planilha.
- Não deve ser utilizado para acessar sistemas sem autorização.
- As configurações de acesso devem ser mantidas em variáveis de ambiente.

## Observação

O funcionamento depende da estrutura HTML do sistema utilizado. Caso os elementos da página sejam alterados, os seletores Selenium poderão precisar de ajustes.

Este projeto foi preparado para fins de estudo, demonstração e portfólio.