"""
Teste Técnico – IntuitiveCare
Etapa 2 – Transformação, Validação e Enriquecimento de Dados
"""

import pandas as pd
import re
from pathlib import Path



# CONFIGURAÇÕES

PASTA_DADOS = Path("data")
ARQUIVO_DESPESAS = PASTA_DADOS / "consolidado_despesas.csv"
ARQUIVO_CADASTRO = PASTA_DADOS / "Relatorio_cadop.csv"
ARQUIVO_SAIDA = PASTA_DADOS / "despesas_agregadas.csv"



# FUNÇÕES AUXILIARES

def normalizar_cnpj(cnpj):
    return re.sub(r"\D", "", str(cnpj))


def validar_cnpj(cnpj):
    cnpj = normalizar_cnpj(cnpj)

    if len(cnpj) != 14 or cnpj == cnpj[0] * 14:
        return False

    def calcular_digito(cnpj, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)

    pesos_1 = [5,4,3,2,9,8,7,6,5,4,3,2]
    pesos_2 = [6] + pesos_1

    digito1 = calcular_digito(cnpj[:12], pesos_1)
    digito2 = calcular_digito(cnpj[:12] + digito1, pesos_2)

    return cnpj[-2:] == digito1 + digito2



# PIPELINE PRINCIPAL

def main():
    print("Iniciando ETAPA 2 – Validação, Enriquecimento e Agregação")

    df_despesas = pd.read_csv(ARQUIVO_DESPESAS, sep=";")
    df_cadastro = pd.read_csv(ARQUIVO_CADASTRO, sep=";")

  
    # NORMALIZAÇÃO
    
    df_cadastro["CNPJ"] = df_cadastro["CNPJ"].apply(normalizar_cnpj)

   
    # JOIN CORRETO (REG_ANS)
  
    df_join = df_despesas.merge(
        df_cadastro[
            ["REGISTRO_OPERADORA", "CNPJ", "Razao_Social", "Modalidade", "UF"]
        ],
        left_on="REG_ANS",
        right_on="REGISTRO_OPERADORA",
        how="left"
    )

    df_join.rename(columns={
        "Razao_Social": "RazaoSocial"
    }, inplace=True)


    # VALIDAÇÕES


    df_join["CNPJ_Valido"] = df_join["CNPJ"].apply(validar_cnpj)
    df_join["Valor_Positivo"] = df_join["ValorDespesas"] > 0
    df_join["RazaoSocial_Valida"] = (
        df_join["RazaoSocial"].notna() &
        (df_join["RazaoSocial"].str.strip() != "")
    )

 
    # FILTRO FINAL (estratégia escolhida)

    df_validos = df_join[
        df_join["CNPJ_Valido"] &
        df_join["Valor_Positivo"] &
        df_join["RazaoSocial_Valida"]
    ].copy()


    # AGREGAÇÃO

    df_agregado = (
        df_validos
        .groupby(["RazaoSocial", "UF"])
        .agg(
            Total_Despesas=("ValorDespesas", "sum"),
            Media_Trimestral=("ValorDespesas", "mean"),
            Desvio_Padrao=("ValorDespesas", "std")
        )
        .reset_index()
        .sort_values(by="Total_Despesas", ascending=False)
    )


    # SAÍDA

    df_agregado.to_csv(ARQUIVO_SAIDA, index=False, sep=";")

    print("ETAPA 2 concluída com sucesso!")
    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")


if __name__ == "__main__":
    main()