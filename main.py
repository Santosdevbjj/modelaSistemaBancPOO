import textwrap
# Importa as classes e funções necessárias
from src.models.cliente import Cliente, PessoaFisica
from src.models.conta import ContaCorrente
from src.models.transacao import Deposito, Saque
from src.services.utils import menu, exibir_extrato

# ==============================================================================
# Funções de Helper para o Menu Principal
# ==============================================================================

def filtrar_cliente(cpf, clientes):
    """
    Localiza um cliente na lista de clientes pelo CPF.
    Retorna o objeto Cliente ou None.
    """
    # Filtra a lista para encontrar o cliente (objeto)
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    # Retorna o primeiro cliente encontrado ou None
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    """
    Pede ao cliente para selecionar uma de suas contas.
    Idealmente, clientes teriam apenas uma conta neste modelo, mas prepara para futuro.
    Retorna o objeto Conta.
    """
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    # Implementação simplificada: retorna a primeira conta se houver
    # Em um sistema real, o cliente escolheria a conta.
    return cliente.contas[0]

def criar_cliente(clientes):
    """
    Cria um novo cliente (PessoaFisica) e o adiciona à lista de clientes.
    Verifica a duplicidade de CPF.
    """
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    # Instancia um objeto PessoaFisica (POO)
    cliente = PessoaFisica(
        nome=nome,
        data_nascimento=data_nascimento,
        cpf=cpf,
        endereco=endereco,
    )

    clientes.append(cliente)
    print("=== Usuário criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    """
    Cria uma nova conta corrente (ContaCorrente) para um cliente existente.
    A conta é adicionada à lista de contas do sistema e à lista de contas do cliente.
    """
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    # Instancia um objeto ContaCorrente (POO)
    # Usa o método de classe nova_conta para criação (padrão Factory Method simples)
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta) # Adiciona à lista geral de contas
    cliente.adicionar_conta(conta) # Associa a conta ao objeto Cliente (agregação)

    print("\n=== Conta criada com sucesso! ===")

def listar_contas(contas):
    """
    Exibe todas as contas do sistema.
    Utiliza o método __str__ (polimorfismo) da classe ContaCorrente para formatar a saída.
    """
    if not contas:
        print("\n@@@ Nenhuma conta cadastrada. @@@")
        return

    for conta in contas:
        # O print(conta) chama implicitamente conta.__str__()
        print("=" * 100)
        print(textwrap.dedent(str(conta)))


# ==============================================================================
# Lógica Principal do Sistema
# ==============================================================================

def main():
    """
    Função principal que gerencia o loop do menu e as operações do sistema.
    Aplica as classes e métodos modelados.
    """
    # Listas para armazenar objetos
    clientes = []  # Lista de objetos Cliente
    contas = []    # Lista de objetos ContaCorrente

    while True:
        # Chama a função utilitária
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            try:
                valor = float(input("Informe o valor do depósito: "))
                # Instancia o objeto Deposito
                deposito = Deposito(valor)
                # O cliente realiza a transação na conta, encapsulando a lógica
                cliente.realizar_transacao(conta, deposito)
            except ValueError:
                print("\n@@@ Valor inválido! Use apenas números. @@@")


        elif opcao == "s":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            try:
                valor = float(input("Informe o valor do saque: "))
                # Instancia o objeto Saque
                saque = Saque(valor)
                # O cliente realiza a transação na conta
                cliente.realizar_transacao(conta, saque)
            except ValueError:
                print("\n@@@ Valor inválido! Use apenas números. @@@")


        elif opcao == "e":
            cpf = input("Informe o CPF do cliente: ")
            cliente = filtrar_cliente(cpf, clientes)

            if not cliente:
                print("\n@@@ Cliente não encontrado! @@@")
                continue

            conta = recuperar_conta_cliente(cliente)
            if not conta:
                continue

            # Chama a função utilitária com o objeto conta
            exibir_extrato(conta)

        elif opcao == "nu":
            criar_cliente(clientes)

        elif opcao == "nc":
            # O número da conta é o tamanho da lista + 1
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "lc":
            listar_contas(contas)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

# Ponto de entrada do programa
if __name__ == "__main__":
    main()
