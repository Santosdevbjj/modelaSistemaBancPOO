import textwrap

# ==============================================================================
# Funções Utilitárias e Menu
# Mantém a função menu separada para organização.
# ==============================================================================

def menu():
    """
    Exibe o menu de opções para o usuário.
    Retorna a opção escolhida.
    """
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    # textwrap.dedent remove a indentação inicial da string
    return input(textwrap.dedent(menu))

def log_transacao(mensagem):
    """
    Função simples para logar mensagens de sucesso/falha de transações.
    Pode ser expandida para um sistema de logging mais robusto no futuro.
    """
    print(mensagem)

def exibir_extrato(conta):
    """
    Exibe o extrato da conta, mostrando todas as transações registradas.
    Acessa o histórico e saldo da conta (objeto ContaCorrente).
    """
    print("\n================ EXTRATO ================")
    # Acessa o atributo transacoes do objeto historico da conta
    transacoes = conta.historico.transacoes
    extrato_string = ""

    if not transacoes:
        extrato_string = "Não foram realizadas movimentações."
    else:
        # Itera sobre os dicionários de transações no histórico
        for transacao in transacoes:
            tipo = transacao["tipo"]
            valor = transacao["valor"]
            extrato_string += f"{tipo}:\tR$ {valor:.2f}\n"

    print(extrato_string)
    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}") # Acessa o saldo via property
    print("==========================================")

