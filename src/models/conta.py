# Importa as classes necessárias do módulo transacao
from src.models.transacao import Transacao, Saque, Deposito

# ==============================================================================
# Classes de Histórico, Conta e Conta Corrente
# ==============================================================================

class Historico:
    """
    Classe responsável por registrar e armazenar o histórico de transações de uma conta.
    Utiliza o encapsulamento para proteger a lista de transações.
    """
    def __init__(self):
        # Lista de transações (objetos de Saque ou Deposito)
        self._transacoes = []

    @property
    def transacoes(self):
        """Retorna a lista de transações."""
        return self._transacoes

    def adicionar_transacao(self, transacao: Transacao):
        """Adiciona uma transação (objeto) ao histórico."""
        # Garante que apenas objetos de Transacao sejam adicionados
        if isinstance(transacao, Transacao):
            self._transacoes.append(
                {
                    "tipo": transacao.__class__.__name__, # Nome da classe (Deposito ou Saque)
                    "valor": transacao.valor,
                }
            )

class Conta:
    """
    Classe base para todas as contas bancárias.
    Define os atributos e métodos básicos (saldo, número, agência, cliente, histórico).
    """
    def __init__(self, numero, cliente):
        # Atributos de classe (fixos)
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente # Objeto Cliente
        self._historico = Historico() # Objeto Histórico

    # Propriedades de leitura (getters) - Encapsulamento
    @classmethod
    def nova_conta(cls, cliente, numero):
        """Método de classe para criar uma nova conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        """Retorna o saldo da conta."""
        return self._saldo

    @property
    def numero(self):
        """Retorna o número da conta."""
        return self._numero

    @property
    def agencia(self):
        """Retorna o número da agência."""
        return self._agencia

    @property
    def cliente(self):
        """Retorna o objeto Cliente associado."""
        return self._cliente

    @property
    def historico(self):
        """Retorna o objeto Histórico."""
        return self._historico

    # Métodos de Operação (Interface básica)
    def sacar(self, valor):
        """
        Tenta realizar um saque.
        Deve ser estendido por classes filhas para incluir regras específicas (limites, etc.).
        """
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")

        elif valor > 0:
            # Altera o estado interno da conta
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")

        return False

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        if valor > 0:
            # Altera o estado interno da conta
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

class ContaCorrente(Conta):
    """
    Classe que herda de Conta e implementa as regras específicas de Conta Corrente:
    limite de saque por transação e limite de número de saques diários.
    """
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        # Chama o construtor da classe base (Conta)
        super().__init__(numero, cliente)
        # Atributos específicos da ContaCorrente
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    # Propriedades
    @property
    def limite(self):
        return self._limite

    @property
    def limite_saques(self):
        return self._limite_saques

    # Sobrescrevendo o método sacar da classe base (Polimorfismo)
    def sacar(self, valor):
        """Implementa a lógica de saque com limites e contagem de saques."""
        excedeu_limite = valor > self.limite
        excedeu_saques = self._numero_saques >= self.limite_saques

        if excedeu_limite:
            print(f"\n@@@ Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f}. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        # Chama o método sacar da classe base (Conta) se as regras específicas passarem
        elif super().sacar(valor):
            # Se o saque na classe base for True (sucesso), incrementa o contador
            self._numero_saques += 1
            return True

        return False

    def __str__(self):
        """Método especial para representação em string (listagem de contas)."""
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

