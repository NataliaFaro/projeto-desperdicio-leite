# NataliaFaro_RM568610_fase2_cap6

#Tema: Desperdício de leite no agronegócio.
#Problema: pequenos e médios produtores podem ter perdas de leite por falhas de armazenamento, transporte ou controle manual dos dados.
#Solução: desenvolver um sistema para registrar a produção e o desperdício diário, calcular o percentual de perda.

# ============================================
# STEP 1 - IMPORTS
# ============================================
import json
import oracledb


# ============================================
# STEP 2 - ESTRUTURAS DE DADOS
# ============================================
registros = []
niveis = ("Baixo", "Médio", "Alto")


# ============================================
# STEP 3 - MENU
# ============================================
def exibir_menu():
    print("\n=== CONTROLE DE DESPERDICIO DE LEITE ===")
    print("1 - Cadastrar registro")
    print("2 - Listar registros")
    print("3 - Salvar em JSON")
    print("4 - Sair")


# ============================================
# STEP 4 - CLASSIFICAÇÃO DO DESPERDÍCIO
# ============================================
def classificar_desperdicio(percentual):
    if percentual <= 5:
        return "Baixo"
    elif percentual <= 10:
        return "Médio"
    else:
        return "Alto"


# ============================================
# STEP 5 - ARQUIVO TEXTO
# ============================================
def salvar_txt(registro):
    with open("registros.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(str(registro) + "\n")


# ============================================
# STEP 6 - ARQUIVO JSON
# ============================================
def salvar_json(registros):
    with open("registros.json", "w", encoding="utf-8") as arquivo:
        json.dump(registros, arquivo, indent=4, ensure_ascii=False)


# ============================================
# STEP 7 - CONEXÃO COM ORACLE
# ============================================
def conectar():
    conn = oracledb.connect(
        user="rm568610",
        password="110192",
        dsn="oracle.fiap.com.br:1521/ORCL"
    )
    return conn


# ============================================
# STEP 8 - INSERÇÃO NO ORACLE
# ============================================
def inserir_oracle(registro):
    conn = conectar()
    cursor = conn.cursor()

    sql = """
    INSERT INTO tb_desperdicio_leite
    (id, produtor, data, litros_produzidos, litros_desperdicados, percentual, nivel)
    VALUES (:1, :2, :3, :4, :5, :6, :7)
    """

    cursor.execute(sql, (
        registro["id"],
        registro["produtor"],
        registro["data"],
        registro["litros_produzidos"],
        registro["litros_desperdicados"],
        registro["percentual_desperdicio"],
        registro["nivel"]
    ))

    conn.commit()
    cursor.close()
    conn.close()


# ============================================
# STEP 9 - CADASTRO DE REGISTRO
# ============================================
def cadastrar_registro():
    print("\n--- CADASTRAR REGISTRO ---")

    id_registro = int(input("Digite o ID: "))
    produtor = input("Digite o nome do produtor: ")
    data = input("Digite a data (dd/mm/aaaa): ")
    litros_produzidos = float(input("Digite os litros produzidos: "))
    litros_desperdicados = float(input("Digite os litros desperdiçados: "))

    # cálculo do percentual
    percentual = (litros_desperdicados / litros_produzidos) * 100

    # classificação
    nivel = classificar_desperdicio(percentual)

    # criação do registro (dicionário)
    registro = {
        "id": id_registro,
        "produtor": produtor,
        "data": data,
        "litros_produzidos": litros_produzidos,
        "litros_desperdicados": litros_desperdicados,
        "percentual_desperdicio": percentual,
        "nivel": nivel
    }

    # armazenamento na lista
    registros.append(registro)

    # salvar em arquivo texto
    salvar_txt(registro)

    # salvar no Oracle
    try:
        inserir_oracle(registro)
        print("Registro gravado no Oracle com sucesso!")
    except Exception as e:
        print("Erro ao gravar no Oracle:", e)

    print("Registro cadastrado com sucesso!")


# ============================================
# STEP 10 - LISTAGEM DOS REGISTROS
# ============================================
def listar_registros():
    print("\n--- LISTA DE REGISTROS ---")

    if len(registros) == 0:
        print("Nenhum registro cadastrado.")
    else:
        for r in registros:
            print(f"ID: {r['id']}")
            print(f"Produtor: {r['produtor']}")
            print(f"Data: {r['data']}")
            print(f"Litros produzidos: {r['litros_produzidos']}")
            print(f"Litros desperdiçados: {r['litros_desperdicados']}")
            print(f"Percentual de desperdício: {r['percentual_desperdicio']:.2f}%")
            print(f"Nível: {r['nivel']}")
            print("-" * 30)


# ============================================
# STEP 11 - LOOP PRINCIPAL DO SISTEMA
# ============================================
opcao = 0

while opcao != 4:
    exibir_menu()
    opcao = int(input("Escolha uma opção: "))

    if opcao == 1:
        cadastrar_registro()
    elif opcao == 2:
        listar_registros()
    elif opcao == 3:
        salvar_json(registros)
        print("Dados salvos em JSON com sucesso!")
    elif opcao == 4:
        print("Encerrando o sistema...")
    else:
        print("Opção inválida.")
