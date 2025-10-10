from abc import ABC, abstractmethod

# ==============================================================================
# Interface e Classes de Transação
# Implementando o conceito de polimorfismo com a classe abstrata Transacao
# ==============================================================================

class Transacao(ABC):
    """
    Interface (Classe Abstrata) para todas as transações bancárias.
    Define o contrato básico que toda transação deve seguir: registrar.
    """
    @property
    @abstractmethod
    def valor(self):
        """Retorna o valor da transação."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """
        Registra a transação na conta, modificando seu estado.
        Deve ser implementado pelas classes filhas.
        """
        pass

class Deposito(Transacao):
    """
    Representa uma transação de depósito.
    """
    def __init__(self, valor):
        # Encapsulamento: o valor é protegido e acessado via property
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """
        Realiza o depósito na conta.
        Retorna True se o depósito for bem-sucedido.
        """
        # Utiliza o método depositar da conta, garantindo a lógica de negócio
        sucesso = conta.depositar(self.valor)

        if sucesso:
            # Adiciona a si mesma ao histórico da conta
            conta.historico.adicionar_transacao(self)
        
        return sucesso

class Saque(Transacao):
    """
    Representa uma transação de saque.
    """
    def __init__(self, valor):
        # Encapsulamento
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        """
        Realiza o saque na conta.
        Retorna True se o saque for bem-sucedido.
        """
        # Utiliza o método sacar da conta, garantindo a lógica de negócio (limites, saques)
        sucesso = conta.sacar(self.valor)

        if sucesso:
            # Adiciona a si mesma ao histórico da conta
            conta.historico.adicionar_transacao(self)
        
        return sucesso

