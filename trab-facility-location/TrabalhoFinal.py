import gurobipy as gp


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
    path = 'trab-facility-location/instancias/' + nome_arquivo + '.txt'
    try:
        with open(path, "r", encoding="utf-8") as arq:
            linhas = []
            for linha in arq:
                linha = linha.strip()
                if linha != "":
                    linhas.append(linha)
    except Exception as e:
        print('Verifique o path das suas instâncias! ', {e})
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
            >= dados.demandas_clientes[c],
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

    m.write('trab-facility-location/modelos/' + nome_arquivo + '.lp')
    return m, {
        "abertura_deposito": abertura_deposito,
        "abertura_fabrica": abertura_fabrica,
        "transp_deposito_cliente": transp_deposito_cliente,
        "transp_fabrica_deposito": transp_fabrica_deposito,
    }


def main(dados: Instancia):
    model, vd = criar_modelo(dados, arquivo)
    model.optimize()

    if model.status == gp.GRB.OPTIMAL:
        print(f"\nValor ótimo = {model.objVal}")

        print("\nFÁBRICAS ABERTAS")
        for f in dados.F:
            if vd["abertura_fabrica"][f].X > 0.5:
                print(f"Fábrica {f}")

        print("\nDEPÓSITOS ABERTOS")
        for d in dados.D:
            if vd["abertura_deposito"][d].X > 0.5:
                print(f"Depósito {d}")

        print("\nFLUXO FASE 1")
        for f in dados.F:
            for d in dados.D:
                if vd["transp_fabrica_deposito"][f, d].X > 1e-6:
                    print(
                        f"Fabrica {f} >> Depósito {d} = {vd['transp_fabrica_deposito'][f,d].X}"
                    )

        print("\nFLUXO FASE 2")
        for d in dados.D:
            for c in dados.C:
                if vd["transp_deposito_cliente"][d, c].X > 1e-6:
                    print(
                        f"Depósito {d} >> Cliente {c} = {vd['transp_deposito_cliente'][d,c].X}"
                    )
    else:
        print("\nNenhuma solução ótima encontrada.")


arquivo = "toy"
dados = ler_instancia(arquivo)
if dados:
    main(dados)
