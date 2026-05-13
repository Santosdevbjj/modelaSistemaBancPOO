# Sistema Bancário em Python: Refatoração de Código Procedural para Arquitetura POO com UML

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![POO](https://img.shields.io/badge/Paradigma-POO-F97316?style=flat)
![UML](https://img.shields.io/badge/Modelagem-UML-8B5CF6?style=flat)
![Status](https://img.shields.io/badge/Status-Concluído-22C55E?style=flat)
![MIT License](https://img.shields.io/badge/Licença-MIT-6B7280?style=flat)

> Refatoração completa de sistema bancário procedural para arquitetura orientada a objetos, guiada por diagrama UML: encapsulamento, herança, polimorfismo e composição implementados em Python com separação de domínio e serviços.

---

## 1. Problema de Negócio

Sistemas bancários começam simples — funções soltas, variáveis globais, lógica de saque misturada com validação de saldo misturada com exibição de menu. Essa abordagem procedural funciona enquanto o sistema é pequeno. À medida que regras de negócio crescem — limites por tipo de conta, diferentes perfis de cliente, múltiplos tipos de transação — o código procedural se torna um risco: cada nova regra precisa ser adicionada em múltiplos lugares, qualquer mudança pode quebrar comportamentos não relacionados, e não há forma segura de testar componentes isoladamente.

O desafio central deste projeto é demonstrar, com código real e modelagem UML explícita, como a refatoração para **Programação Orientada a Objetos** transforma um sistema frágil e acoplado em uma arquitetura onde cada responsabilidade tem um lugar definido, regras de negócio estão encapsuladas nas entidades corretas e novas funcionalidades podem ser adicionadas sem reescrever o que já funciona.

---

## 2. Contexto

O projeto foi desenvolvido no **Bootcamp Luizalabs — Back-end com Python**, com objetivo de ir além da implementação e construir o ciclo completo de engenharia de software: modelagem UML → design de classes → implementação → separação de responsabilidades.

O domínio bancário foi escolhido por ser rico em padrões de OOP aplicáveis diretamente: clientes com múltiplas contas (agregação), contas com histórico de transações (composição), diferentes tipos de transação com interface comum (polimorfismo), e regras específicas por tipo de conta como limites e contadores de saque (herança com override).

A arquitetura final separa o **domínio** (`src/models/`) dos **serviços auxiliares** (`src/services/`) — estrutura equivalente à camada de domínio + camada de apresentação em aplicações de produção.

---

## 3. Premissas

- O diagrama UML define o contrato de design: nenhuma classe, atributo ou método foi adicionado sem correspondência no diagrama. A implementação segue o modelo, não o contrário.
- `ContaCorrente` aplica limite por transação de R$ 500,00 e máximo de 3 saques diários — regras fixadas como parâmetros default no construtor, alteráveis por instância sem modificar a classe.
- A classe `Transacao` é abstrata (`ABC`) com método `registrar(conta)` obrigatório — qualquer nova transação (transferência, PIX, tarifa) deve implementar esse contrato para ser aceita pelo sistema.
- Cada transação se registra no histórico da conta (`conta.historico.adicionar_transacao(self)`) ao invés de ser registrada externamente — o objeto de transação é responsável por seu próprio registro, mantendo o histórico sempre consistente com as operações bem-sucedidas.
- O sistema usa listas em memória (`clientes`, `contas`) sem persistência — decisão de escopo que isola o aprendizado de OOP sem dependência de banco de dados. A camada de persistência é o próximo passo natural.

---

## 4. Estratégia da Solução

### 4.1 Diagrama UML como Contrato de Design

O diagrama UML define cinco classes principais com suas relações:

```
Cliente ◄────────────── PessoaFisica
   │ (agregação)
   └──── [Conta] ◄───── ContaCorrente
              │ (composição)
              └──── Historico
                       │
                    [Transacao] ◄── Deposito
                                 ◄── Saque
```

- **Herança:** `PessoaFisica → Cliente`, `ContaCorrente → Conta`
- **Composição:** `Conta` possui um `Historico` — o histórico não existe sem a conta
- **Agregação:** `Cliente` referencia múltiplas `Conta` — contas podem existir independentemente
- **Interface (ABC):** `Transacao` define contrato; `Deposito` e `Saque` implementam

### 4.2 Estrutura de Arquivos

```
modelando-sistema-bancario-em-POO/
├── main.py                    → Ponto de entrada, loop principal, orquestração
├── src/
│   ├── models/
│   │   ├── cliente.py         → Classes Cliente e PessoaFisica (herança, encapsulamento)
│   │   ├── conta.py           → Classes Historico, Conta e ContaCorrente (composição, polimorfismo)
│   │   └── transacao.py       → Interface Transacao (ABC), Deposito e Saque
│   └── services/
│       └── utils.py           → Menu, exibição de extrato, logging (sem lógica de domínio)
└── .gitignore
```

### 4.3 Os Quatro Pilares de POO Implementados

**Encapsulamento:** atributos com prefixo `_` acessados exclusivamente via `@property`. O saldo (`_saldo`) só é alterado pelos métodos `depositar()` e `sacar()` — nenhum código externo modifica o estado da conta diretamente.

```python
@property
def saldo(self):
    return self._saldo  # Leitura pública, escrita protegida
```

**Herança com override:** `ContaCorrente.sacar()` estende `Conta.sacar()` sem duplicar código — valida limites específicos e delega a operação base via `super().sacar(valor)`:

```python
def sacar(self, valor):
    excedeu_limite = valor > self.limite          # Regra específica de ContaCorrente
    excedeu_saques = self._numero_saques >= self.limite_saques  # Regra específica

    if excedeu_limite:
        print(f"@@@ Limite por saque: R$ {self.limite:.2f} @@@")
    elif excedeu_saques:
        print("@@@ Limite de saques diários atingido @@@")
    elif super().sacar(valor):                    # Delega para Conta.sacar()
        self._numero_saques += 1
        return True
    return False
```

**Polimorfismo:** `cliente.realizar_transacao(conta, transacao)` aceita qualquer objeto que implemente `Transacao.registrar()` — `Deposito`, `Saque` ou qualquer futura transação:

```python
def realizar_transacao(self, conta, transacao):
    return transacao.registrar(conta)  # Polimorfismo: Deposito ou Saque, mesma interface
```

**Composição:** `Conta` cria e possui seu `Historico` internamente — o histórico não pode existir sem a conta, e é destruído junto com ela:

```python
def __init__(self, numero, cliente):
    self._historico = Historico()  # Composição: Historico criado dentro de Conta
```

### 4.4 Fluxo Completo de uma Transação

```
main.py                    cliente.py              transacao.py         conta.py
   │                           │                       │                   │
   ├─ saque = Saque(valor)     │                       │                   │
   ├─ cliente.realizar_transacao(conta, saque)          │                   │
   │        │                  │                       │                   │
   │        └─ transacao.registrar(conta) ─────────────►                   │
   │                                                   ├─ conta.sacar() ──►│
   │                                                   │    ◄── True        │
   │                                                   └─ conta.historico.adicionar_transacao(self)
```

---

## 5. Decisões Técnicas

### Por que `Transacao` como classe abstrata (`ABC`) ao invés de classe concreta ou protocolo?

`ABC` com `@abstractmethod` garante em tempo de instanciação que qualquer subclasse implemente `registrar(conta)` e `valor`. Se um desenvolvedor criar `Transferencia(Transacao)` sem implementar `registrar`, Python lança `TypeError` imediatamente — antes de qualquer execução. Protocolo (`Protocol`) seria mais flexível, mas menos explícito sobre o contrato. Para um sistema bancário onde transações incompletas são inaceitáveis, o contrato explícito via `ABC` é a escolha correta.

### Por que a transação se registra no histórico ao invés do cliente ou da conta fazerem isso?

A alternativa seria `conta.historico.adicionar_transacao(transacao)` chamado em `main.py` após cada operação. O problema: se o desenvolvedor esquecer essa linha, a operação ocorre mas não é registrada — inconsistência silenciosa. Ao delegar ao próprio objeto `Deposito`/`Saque` a responsabilidade de se registrar (`conta.historico.adicionar_transacao(self)` dentro de `registrar()`), o registro é inseparável da operação. Não há como realizar uma transação sem registrá-la.

### Por que separar `src/models/` e `src/services/`?

`models/` contém entidades de domínio puro — sem `print`, sem lógica de apresentação, sem dependência de interface. `services/` contém tudo que depende de como o sistema interage com o usuário. Essa separação permite trocar a interface (de CLI para API REST, por exemplo) sem tocar nas regras de negócio. O método `exibir_extrato(conta)` em `utils.py` acessa `conta.historico.transacoes` e `conta.saldo` via interface pública — sem conhecer os detalhes internos da conta.

### Por que `nova_conta` como `@classmethod` ao invés de construtor direto?

`ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)` é um Factory Method simples: centraliza a lógica de criação e torna a assinatura mais legível com parâmetros nomeados. Para subclasses futuras (`ContaPoupanca`, `ContaSalario`), cada uma pode ter seu próprio `nova_conta` com parâmetros específicos sem alterar a interface de criação em `main.py`.

---

## 6. Insights

A refatoração de procedural para OOP revelou padrões com impacto direto em sistemas de maior escala:

**A lógica de `super().sacar(valor)` em `ContaCorrente` elimina duplicação crítica:** a versão procedural validava saldo em dois lugares — na função de saque e em cada verificação de limite. Com herança, `Conta.sacar()` valida saldo e `ContaCorrente.sacar()` valida limites, chamando `super()` para a validação base. Cada regra vive em exatamente um lugar.

**Encapsulamento revela contratos implícitos:** ao proteger `_saldo` com `@property` sem setter, fica imediatamente óbvio que saldo só muda via `depositar()` ou `sacar()`. Na versão procedural, `saldo` era uma variável modificável de qualquer ponto — o histórico e o saldo podiam ficar dessincronizados sem nenhum aviso.

**A composição `Conta → Historico` foi a decisão de design mais impactante:** na versão procedural, o extrato era uma lista global. Com composição, cada conta carrega seu próprio histórico, isolado e consistente. Isso permite no futuro ter múltiplas contas por cliente sem risco de transações de uma conta aparecerem no extrato de outra.

**O filtro de cliente por CPF via list comprehension é O(n):** para o escopo atual, adequado. Em produção com milhares de clientes, isso migraria para um dicionário `{cpf: cliente}` — lookup O(1). A estrutura de domínio (`cliente.cpf`) já está correta para essa migração; apenas `filtrar_cliente()` em `main.py` precisaria ser alterado.

---

## 7. Resultados

- **Arquitetura POO completa** guiada por diagrama UML com cinco classes, dois relacionamentos de herança, uma composição, uma agregação e uma interface abstrata.

- **Quatro pilares de OOP demonstrados com código real:** encapsulamento via `@property`, herança com `super()` em `ContaCorrente.sacar()`, polimorfismo via `Transacao.registrar()` e composição em `Conta → Historico`.

- **Regras de negócio encapsuladas nas entidades corretas:** limite de R$ 500 e máximo de 3 saques diários vivem em `ContaCorrente`, não em `main.py` — qualquer parte do sistema que use `ContaCorrente.sacar()` automaticamente respeita essas regras.

- **Auto-registro de transações:** `Deposito` e `Saque` se registram no histórico da conta ao executar `registrar()` — impossível realizar operação sem registrá-la, eliminando a classe de bugs de inconsistência entre saldo e extrato.

- **Arquitetura extensível:** adicionar `ContaPoupanca` com rendimento mensal exige apenas uma nova subclasse de `Conta`. Adicionar `Transferencia` exige apenas uma nova subclasse de `Transacao`. Nenhuma das classes existentes precisa ser modificada.

---

## 8. Tecnologias Utilizadas

| Tecnologia | Papel no Projeto |
|---|---|
| Python 3.8+ | Linguagem principal, OOP, ABC, `@property`, `@classmethod` |
| `abc.ABC` + `@abstractmethod` | Interface `Transacao` — contrato obrigatório para subclasses |
| `textwrap.dedent` | Formatação de strings multilinhas no menu e extrato |
| Git / GitHub | Versionamento e hospedagem do repositório |

---

## 9. Como Executar

**Pré-requisito:** Python 3.8+

```bash
# Clone o repositório
git clone https://github.com/Santosdevbjj/modelando-sistema-bancario-em-POO.git
cd modelando-sistema-bancario-em-POO

# (Opcional) Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux/macOS
.\venv\Scripts\activate    # Windows

# Execute o sistema
python main.py
```

**Menu interativo disponível:**

```
[nu]  Novo usuário      → Cria objeto PessoaFisica com CPF, nome, data e endereço
[nc]  Nova conta        → Cria ContaCorrente associada a um cliente por CPF
[d]   Depositar         → Instancia Deposito(valor) e registra na conta
[s]   Sacar             → Instancia Saque(valor) com validação de limite e contador
[e]   Extrato           → Exibe histórico de transações e saldo atual
[lc]  Listar contas     → Exibe todas as contas via __str__ de ContaCorrente
[q]   Sair
```

**Fluxo de teste rápido:**

```
1. [nu] → Criar cliente com CPF 12345678900
2. [nc] → Criar conta para CPF 12345678900
3. [d]  → Depositar R$ 1000,00
4. [s]  → Sacar R$ 200,00 (dentro do limite)
5. [s]  → Sacar R$ 600,00 (excede limite de R$ 500 — deve falhar)
6. [e]  → Verificar extrato: Deposito R$ 1000 + Saque R$ 200 = Saldo R$ 800
```

---

## 10. Aprendizados

**O maior aprendizado foi entender quando usar herança versus composição.** A tentação inicial foi colocar `historico` como atributo de `Cliente` — afinal, o cliente "tem" um histórico. O modelo UML mostrou o erro: o histórico pertence à `Conta`, não ao cliente. Um cliente com duas contas tem dois históricos separados. Essa distinção só ficou clara ao modelar as relações no diagrama antes de escrever código.

**Sobre `super()` em herança:** a primeira versão de `ContaCorrente.sacar()` copiou toda a lógica de `Conta.sacar()` e adicionou as verificações de limite. Essa duplicação significava que qualquer bug corrigido em `Conta.sacar()` precisaria ser corrigido também em `ContaCorrente.sacar()`. A refatoração para `super().sacar(valor)` reduziu `ContaCorrente.sacar()` a apenas suas responsabilidades exclusivas — um exemplo concreto de como herança reduz duplicação.

**O que faria diferente hoje:** implementaria persistência com SQLite desde o início — o design de domínio já está correto para isso, `Cliente` e `Conta` precisariam apenas de um repositório que serialize os objetos. Adicionaria também `pytest` com fixtures para testar `ContaCorrente.sacar()` nos cenários de limite excedido, saques esgotados e saldo insuficiente — os três casos críticos que o sistema bancário não pode errar.

---

## 11. Próximos Passos

- Implementar persistência com SQLite ou JSON, serializando os objetos de domínio sem alterar as classes de modelo
- Adicionar `ContaPoupanca` com taxa de rendimento mensal como nova subclasse de `Conta` — demonstrando extensibilidade sem modificação de código existente
- Implementar `Transferencia(Transacao)` que debita de uma conta e credita em outra dentro de `registrar()`
- Adicionar suíte de testes com `pytest`: cenários de saque com limite excedido, saldo insuficiente e contador de saques esgotado
- Substituir lista `clientes` por dicionário `{cpf: cliente}` para lookup O(1) em vez de O(n)
- Expor o sistema como API REST com FastAPI, mantendo `src/models/` intocado — mudando apenas a camada de interface

---

## Autor

**Sergio Santos** — Senior Data Engineer & Cloud Architect

[![Portfólio](https://img.shields.io/badge/Portfólio-Sérgio_Santos-111827?style=for-the-badge&logo=githubpages&logoColor=00eaff)](https://portfoliosantossergio.vercel.app)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sérgio_Santos-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://linkedin.com/in/santossergioluiz)
[![GitHub](https://img.shields.io/badge/GitHub-Santosdevbjj-24292f?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Santosdevbjj)
