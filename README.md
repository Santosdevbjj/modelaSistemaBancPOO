## Modelando o Sistema Bancário em POO com Python.


![PythonDeveloper001](https://github.com/user-attachments/assets/55d38907-069b-4065-8edf-831058a70fb7) 


Bootcamp 

---


# 🏦 Modelagem de Sistema Bancário em POO com Python

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg?logo=python&logoColor=white)
![POO](https://img.shields.io/badge/Paradigma-POO-orange)
![Status](https://img.shields.io/badge/Status-Concluído-brightgreen)
![GitHub last commit](https://img.shields.io/github/last-commit/Santosdevbjj/modelaSistemaBancPOO)
![License](https://img.shields.io/badge/Licença-MIT-lightgrey)

---

## 📌 **Visão Geral do Projeto**

Este projeto consiste na **refatoração de um sistema bancário simples**, inicialmente procedural, para um modelo completamente baseado em **Programação Orientada a Objetos (POO)** utilizando Python.

A arquitetura segue rigorosamente um **diagrama UML**, implementando classes como:

- `Cliente` e `PessoaFisica`  
- `Conta` e `ContaCorrente`  
- `Transacao` (Interface), `Deposito` e `Saque`  

Com isso, o sistema garante **modularidade**, **encapsulamento**, **herança** e **polimorfismo**, tornando-se mais próximo de um design profissional e sustentável.

---

## 🧭 **Diagrama UML**

O projeto foi modelado a partir do seguinte **diagrama UML**, que define todas as classes, atributos, métodos e relações entre entidades:

![Diagrama UML do Sistema Bancário](https://github.com/Santosdevbjj/modelaSistemaBancPOO/assets/uml_diagrama_exemplo) <!-- Substituir por URL da imagem real do repositório, se quiser -->

---

## 🏗️ **Estrutura e Arquitetura do Projeto**

O código foi dividido em módulos para organizar as **entidades do sistema** (`models`) e as **funcionalidades de suporte** (`services`), conforme a estrutura típica de projetos Python:  


<img width="1011" height="765" alt="Screenshot_20251010-041717" src="https://github.com/user-attachments/assets/a4d1e974-d3bc-48db-b46a-11171ba11954" /> 

---


### 📂 **Descrição das Pastas**

| Pasta | Descrição |
|-------|-----------|
| `src/` | Código fonte principal do projeto, separando lógica de domínio da execução. |
| `src/models/` | Contém as classes principais do domínio bancário (Cliente, Conta, Transação). É o núcleo da POO. |
| `src/services/` | Contém utilitários e menus auxiliares, não relacionados diretamente às entidades. |
| `main.py` | Ponto de entrada do sistema, gerencia o loop principal de execução. |
| `.gitignore` | Ignora arquivos desnecessários como `__pycache__` e ambientes virtuais. |

---

## 📝 **Detalhamento dos Arquivos e Conceitos de POO**

| Arquivo | Localização | Descrição e Conceitos de POO |
|---------|-------------|-------------------------------|
| `cliente.py` | `src/models/` | Define a classe base `Cliente` e a especializada `PessoaFisica` (Herança). Contém lista de contas (Agregação) e método `realizar_transacao()`. |
| `conta.py` | `src/models/` | Define `Conta` e `ContaCorrente` (Herança). Implementa regras de limite e saques (Polimorfismo). Inclui a classe `Historico` para composição de transações. |
| `transacao.py` | `src/models/` | Define interface `Transacao` (classe abstrata) e implementações concretas `Deposito` e `Saque`. Demonstra Polimorfismo. |
| `utils.py` | `src/services/` | Funções auxiliares de interação, menu e exibição de extratos. |
| `main.py` | Raiz | Gerencia inicialização do sistema e interação com o usuário. |

---

## 💻 **Requisitos de Software e Hardware**

### 🧰 **Software**
- **Sistema Operacional:** Windows, macOS ou Linux  
- **Python:** Versão 3.8 ou superior (Recomendado: 3.10+)

### 🧠 **Hardware**
- **CPU:** 1.0 GHz ou superior  
- **RAM:** 512 MB livres  
- **Disco:** < 1 MB

---

## ▶️ **Como Executar o Sistema**

Siga os passos abaixo para baixar e rodar o projeto em seu ambiente local:

### 1. Clonar o Repositório

```bash
git clone https://github.com/Santosdevbjj/modelaSistemaBancPOO.git
cd modelaSistemaBancPOO


---
```

**Criar Ambiente Virtual**


# Cria o ambiente virtual
python -m venv venv

# Ativa o ambiente virtual (Linux/macOS)
source venv/bin/activate

# Ativa o ambiente virtual (Windows)
.\venv\Scripts\activate


---

**Executar o Programa**

python main.py


---


**Interagir com o Sistema**

No terminal, será exibido o menu com opções como:

[nu] Novo Usuário

[nc] Nova Conta

[d] Depósito

[s] Saque

[e] Extrato

[q] Sair



---

 **Conceitos de POO Aplicados**

Este projeto é um estudo prático e completo de POO, abordando:

**Encapsulamento:** atributos privados acessados por @property, protegendo o estado interno.

**Herança:** PessoaFisica herda de Cliente; ContaCorrente herda de Conta.

**Polimorfismo:** Interface Transacao exige implementação de registrar(). Saque e Deposito têm comportamentos distintos.

**Agregação/Composição:**

Cliente agrega múltiplas contas.

Conta possui um Historico (Composição), definindo ciclo de vida entre objetos.




---

 **Objetivo Didático**

Este repositório foi desenvolvido com foco educacional, servindo como modelo de arquitetura POO para estudantes e profissionais que desejam evoluir de códigos procedurais para projetos bem estruturados e orientados a objetos.


---

📝 **Licença**

Este projeto está sob a licença MIT.


---

👤 **Autor**

Sérgio Santos


---




