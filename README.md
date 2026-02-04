TESTE DE TRANSFORMAÇÃO E VALIDAÇÃO DE DADOS

# Sobre o projeto

Este projeto foi desenvolvido como parte do Teste Técnico – IntuitiveCare (Etapa 2).
O objetivo desta etapa é realizar a validação, enriquecimento e agregação dos dados de despesas consolidados na Etapa 1, utilizando dados cadastrais públicos da ANS.

O código implementa validações críticas de qualidade de dados, faz o enriquecimento por meio de join entre bases distintas e gera uma visão agregada das despesas por operadora e UF.

# Objetivos

- Confirmar a integridade dos dados financeiros consolidados
- Validar CNPJs utilizando regras oficiais (formato e dígitos verificadores)
- Garantir valores numéricos positivos
- Validar a presença de Razão Social
- Enriquecer os dados com informações cadastrais das operadoras
- Realizar agregações estatísticas para análise financeira
- Documentar decisões técnicas e trade-offs adotados

# Estrutura do projeto
Etapa_2/
│
├── data/
│   ├── consolidado_despesas.csv
│   ├── Relatorio_cadop.csv
│   └── despesas_agregadas.csv
│
├── etapa2.py
└── README.md

# Tecnologias utilizadas

- Python 3.9 ou superior
- Pandas
- Pathlib
- Expressões regulares (re)

# Pré-requisitos

Antes de executar o projeto, é necessário ter instalado:

- Python 3.9 ou superior
- Biblioteca pandas

Instalação da dependência:
- pip install pandas

Ou, se necessário:

- pip3 install pandas

# Fontes de dados

- Consolidado de despesas
- Arquivo gerado na Etapa 1:
- consolidado_despesas.csv

# Colunas principais:

- REG_ANS
- ValorDespesas
- Ano
- Trimestre

# Cadastro de operadoras ativas (ANS)

Arquivo público disponibilizado pela ANS:

https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/

## Arquivo utilizado:

- Relatorio_cadop.csv
- Colunas relevantes:
- REGISTRO_OPERADORA
- CNPJ
- Razao_Social
- Modalidade
- UF
- Estratégias de Validação de Dados
- Validação de CNPJ
- Foi implementada validação completa do CNPJ considerando:
- Remoção de caracteres não numéricos
- Verificação de tamanho (14 dígitos)
- Cálculo e verificação dos dígitos verificadores
- Trade-off técnico
- Estratégia escolhida:
- Registros com CNPJ inválido são descartados do conjunto final.

## Prós:

- Garante alta qualidade e confiabilidade dos dados
- Evita análises financeiras com entidades inconsistentes

## Contras:

- Possível perda de registros relevantes caso o erro esteja na base cadastral
- Validação de valores financeiros

## Critério aplicado:

- Apenas registros com ValorDespesas > 0 são mantidos

## Motivo:

- Valores negativos ou nulos não fazem sentido para análise agregada de despesas.
- Validação de Razão Social

## Critérios:

- Campo não nulo
- Campo não vazio após remoção de espaços
- Enriquecimento de Dados
- Estratégia de Join
- O enriquecimento é feito utilizando a chave correta:
- REG_ANS (despesas) ⟷ REGISTRO_OPERADORA (cadastro)
- Trade-off técnico

## Estratégia escolhida:

- Join do tipo LEFT, seguido de validação e filtragem.

## Justificativa:

- Mantém inicialmente todos os registros de despesas
- Permite identificar operadoras sem cadastro correspondente
- Evita perda silenciosa de dados antes da validação
- Tratamento de falhas no cadastro
- Registros sem correspondência no cadastro
- São descartados na etapa de validação, pois:
- Não possuem Razão Social válida
- Não permitem análise institucional confiável
- CNPJs duplicados no cadastro

A abordagem adotada considera o cadastro oficial como fonte confiável, assumindo consistência do REGISTRO_OPERADORA.

## Agregação dos dados

Após validação e enriquecimento, os dados são agregados por:

- RazaoSocial
- UF
- Métricas calculadas
- Total de despesas por operadora/UF
- Média trimestral de despesas
- Desvio padrão das despesas (indicador de volatilidade)
- Estratégia de ordenação

## Os resultados são ordenados por:

- Total_Despesas (decrescente)
- Trade-off técnico
- Estratégia escolhida:
- Ordenação em memória com pandas.

## Justificativa:

- Volume de dados compatível com processamento local
- Simplicidade e clareza do código
- Adequado ao contexto do teste técnico
- Como executar o projeto
- No terminal, dentro da pasta da Etapa 2, execute:
python etapa2.py

- Ou, se necessário:
python3 etapa2.py

## Resultado

- Após a execução, será gerado o arquivo:

data/despesas_agregadas.csv


- O arquivo contém:
- Razão Social
- UF
- Total de Despesas
- Média Trimestral
- Desvio Padrão

Ao final da execução, uma mensagem de sucesso será exibida no terminal.
