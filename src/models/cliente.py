# ==============================================================================
# Classes de Cliente
# Cliente é a classe base, PessoaFisica herda de Cliente.
# ==============================================================================

class Cliente:
    """
    Classe base para um cliente do banco.
    Armazena dados pessoais e lista de contas.
    """
    def __init__(self, endereco):
        # Encapsulamento
        self._endereco = endereco
        self._contas = [] # Lista de objetos Conta

    @property
    def contas(self):
        """Retorna a lista de contas do cliente."""
        return self._contas

    def realizar_transacao(self, conta, transacao):
        """
        Executa uma transação (objeto Deposito ou Saque) na conta.
        O método registrar da transação irá atualizar o estado da conta.
        """
        # A transação é passada para a conta e o próprio objeto transacao se registra.
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        """Adiciona um objeto Conta à lista de contas do cliente."""
        self._contas.append(conta)


class PessoaFisica(Cliente):
    """
    Classe específica para Clientes Pessoa Física (herda de Cliente).
    Adiciona atributos específicos como CPF, nome e data de nascimento.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        # Chama o construtor da classe base
        super().__init__(endereco)
        # Atributos específicos
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    # Propriedades de leitura
    @property
    def nome(self):
        """Retorna o nome do cliente."""
        return self._nome

    @property
    def cpf(self):
        """Retorna o CPF do cliente."""
        return self._cpf

    def __str__(self):
        """Representação em string para depuração ou listagem."""
        return f"Nome: {self.nome}, CPF: {self.cpf}"

