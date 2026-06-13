import gurobipy as gp
from pathlib import Path
from enum import IntEnum


class GurobiStatusCodeMapping(IntEnum):
    LOADED = 1
    OPTIMAL = 2
    INFEASIBLE = 3
    INF_OR_UNBD = 4
    UNBOUNDED = 5
    CUTOFF = 6
    ITERATION_LIMIT = 7
    NODE_LIMIT = 8
    TIME_LIMIT = 9
    SOLUTION_LIMIT = 10
    INTERRUPTED = 11
    NUMERIC = 12
    SUBOPTIMAL = 13
    INPROGRESS = 14
    USER_OBJ_LIMIT = 15
    WORK_LIMIT = 16
    MEM_LIMIT = 17
    LOCALLY_OPTIMAL = 18
    LOCALLY_INFEASIBLE = 19


class Instancia:
    def __init__(
        self,
        name,
        fabricas,
        depositos,
        clientes,
        custos_fixos_fabricas,
        custos_fixos_depositos,
        capacidades_fabricas,
        capacidades_depositos,
        demandas_clientes,
        custos_fabrica_deposito,
        custos_deposito_cliente,
    ):
        self.name = name
        self.F = fabricas
        self.D = depositos
        self.C = clientes
        self.custos_fixos_fabricas = custos_fixos_fabricas
        self.custos_fixos_depositos = custos_fixos_depositos
        self.capacidades_fabricas = capacidades_fabricas
        self.capacidades_depositos = capacidades_depositos
        self.demandas_clientes = demandas_clientes
        self.custos_fabrica_deposito = custos_fabrica_deposito
        self.custos_deposito_cliente = custos_deposito_cliente


def ler_instancia(nome_arquivo: str):
    path = "instancias/" + nome_arquivo + ".txt"
    try:
        with open(path, "r", encoding="utf-8") as arq:
            linhas = []
            for linha in arq:
                linha = linha.strip()
                if linha != "":
                    linhas.append(linha)
    except Exception as e:
        print("Verifique o path das suas instâncias! ", {e})
        return None

    primeira = linhas[0].split()

    n_fabricas = int(primeira[0])
    n_depositos = int(primeira[1])
    n_clientes = int(primeira[2])

    print("Fábricas :", n_fabricas)
    print("Depósitos:", n_depositos)
    print("Clientes :", n_clientes)

    F = range(n_fabricas)
    D = range(n_depositos)
    C = range(n_clientes)

    indice = 1

    demandas_clientes = {}
    for cliente in C:
        demandas_clientes[cliente] = float(linhas[indice])
        indice += 1

    capacidades_fabricas = {}
    custos_fixos_fabricas = {}
    for fabrica in F:
        valores = linhas[indice].split()
        capacidades_fabricas[fabrica] = float(valores[0])
        custos_fixos_fabricas[fabrica] = float(valores[1])
        indice += 1

    custos_fabrica_deposito = {}
    for fabrica in F:
        valores = linhas[indice].split()
        for deposito in D:
            custos_fabrica_deposito[fabrica, deposito] = float(valores[deposito])

        indice += 1

    capacidades_depositos = {}
    custos_fixos_depositos = {}
    for deposito in D:
        valores = linhas[indice].split()
        capacidades_depositos[deposito] = float(valores[0])
        custos_fixos_depositos[deposito] = float(valores[1])
        indice += 1

    custos_deposito_cliente = {}
    for deposito in D:
        valores = linhas[indice].split()
        for cliente in C:
            custos_deposito_cliente[deposito, cliente] = float(valores[cliente])

        indice += 1

    return Instancia(
        nome_arquivo,
        F,
        D,
        C,
        custos_fixos_fabricas,
        custos_fixos_depositos,
        capacidades_fabricas,
        capacidades_depositos,
        demandas_clientes,
        custos_fabrica_deposito,
        custos_deposito_cliente,
    )


def criar_modelo(dados: Instancia, nome_arquivo: str):
    m = gp.Model("PLFC2N")

    transp_fabrica_deposito = m.addVars(
        dados.F, dados.D, vtype=gp.GRB.CONTINUOUS, lb=0, name="transp_fabrica_deposito"
    )

    transp_deposito_cliente = m.addVars(
        dados.D, dados.C, vtype=gp.GRB.CONTINUOUS, lb=0, name="transp_deposito_cliente"
    )

    abertura_fabrica = m.addVars(dados.F, vtype=gp.GRB.BINARY, name="abertura_fabrica")
    abertura_deposito = m.addVars(
        dados.D, vtype=gp.GRB.BINARY, name="abertura_deposito"
    )

    m.setObjective(
        gp.quicksum(
            dados.custos_fixos_fabricas[f] * abertura_fabrica[f] for f in dados.F
        )
        + gp.quicksum(
            dados.custos_fixos_depositos[d] * abertura_deposito[d] for d in dados.D
        )
        + gp.quicksum(
            dados.custos_fabrica_deposito[f, d] * transp_fabrica_deposito[f, d]
            for f in dados.F
            for d in dados.D
        )
        + gp.quicksum(
            dados.custos_deposito_cliente[d, c] * transp_deposito_cliente[d, c]
            for d in dados.D
            for c in dados.C
        ),
        gp.GRB.MINIMIZE,
    )

    for c in dados.C:
        m.addConstr(
            gp.quicksum(transp_deposito_cliente[d, c] for d in dados.D)
            == dados.demandas_clientes[c],
            name=f"demanda_cliente_{c}",
        )

    for d in dados.D:
        m.addConstr(
            gp.quicksum(transp_fabrica_deposito[i, d] for i in dados.F)
            >= gp.quicksum(transp_deposito_cliente[d, c] for c in dados.C),
            name=f"fluxo_deposito_{d}",
        )

    for f in dados.F:
        m.addConstr(
            gp.quicksum(transp_fabrica_deposito[f, d] for d in dados.D)
            <= dados.capacidades_fabricas[f] * abertura_fabrica[f],
            name=f"capacidade_fabrica_{f}",
        )

    for d in dados.D:
        m.addConstr(
            gp.quicksum(transp_deposito_cliente[d, c] for c in dados.C)
            <= dados.capacidades_depositos[d] * abertura_deposito[d],
            name=f"capacidade_deposito_{d}",
        )

    m.write("modelos/" + nome_arquivo + ".lp")
    return m, {
        "abertura_deposito": abertura_deposito,
        "abertura_fabrica": abertura_fabrica,
        "transp_deposito_cliente": transp_deposito_cliente,
        "transp_fabrica_deposito": transp_fabrica_deposito,
    }


def main(dados: Instancia, arquivo: str):
    model, vd = criar_modelo(dados, arquivo)

    model.setParam("TimeLimit", 500.0)
    model.optimize()

    with open("resultado_" + arquivo + ".txt", "w", encoding="utf-8") as res:
        if model.status == gp.GRB.OPTIMAL:
            res.write(
                f"STATUS: {model.Status}-{GurobiStatusCodeMapping(model.status).name}\n"
            )
            res.write(f"Valor ótimo = {model.objVal}\n")
            res.write(f"Gap: {model.MIPGap * 100}%\n")

            res.write("\nFÁBRICAS ABERTAS:\n")
            fab_abertas = []
            for f in dados.F:
                if vd["abertura_fabrica"][f].X > 0.5:
                    fab_abertas.append(f)

            res.write(f"{str(fab_abertas)}\n")

            res.write("\nDEPÓSITOS ABERTOS:\n")
            dep_abertos = []
            for d in dados.D:
                if vd["abertura_deposito"][d].X > 0.5:
                    dep_abertos.append(d)

            res.write(f"{str(dep_abertos)}\n")

            res.write("\nFLUXO FASE 1:\n")
            for f in dados.F:
                for d in dados.D:
                    valor_fluxo = vd["transp_fabrica_deposito"][f, d].X
                    if valor_fluxo > 1e-6:
                        res.write(f"Fabrica {f} >> Depósito {d} = {valor_fluxo:.2f}\n")

            res.write("\nFLUXO FASE 2:\n")
            for d in dados.D:
                for c in dados.C:
                    valor_fluxo = vd["transp_deposito_cliente"][d, c].X
                    if valor_fluxo > 1e-6:
                        res.write(f"Depósito {d} >> Cliente {c} = {valor_fluxo:.2f}\n")
        else:
            res.write(
                f"STATUS: {model.Status}-{GurobiStatusCodeMapping(model.status).name}"
            )
            res.write("\nNenhuma solução ótima encontrada.")


if __name__ == "__main__":
    p = Path("./instancias/")
    instancias = [arq.stem for arq in p.iterdir() if arq.suffix in [".txt"]]

    for i in instancias:
        print("\nINÍCIO instancia " + i)
        dados = ler_instancia(i)
        if dados:
            main(dados, i)
        print("FIM instancia " + i)
