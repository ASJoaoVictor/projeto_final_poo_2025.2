# 💰 Sistema de Finanças Pessoais

![Status](https://img.shields.io/badge/status-concluido-green)
![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/framework-flask-red)
![License](https://img.shields.io/badge/license-MIT-grey)

> Um sistema web completo para gestão financeira pessoal, permitindo o controle de carteiras, transações, metas e objetivos de longo prazo.

## 📝 Sobre o Projeto

Este projeto consiste em uma aplicação web desenvolvida em **Python** utilizando o framework **Flask**. O sistema foi projetado para permitir que o usuário gerencie suas finanças pessoais de forma centralizada, oferecendo controle sobre múltiplas carteiras, categorização de despesas e acompanhamento de metas financeiras.

O diferencial do sistema é a integridade dos dados, implementando regras de negócio que impedem, por exemplo, que uma carteira fique com saldo negativo ou que transações sejam criadas sem categoria válida.

---

## ✨ Funcionalidades

O sistema atende aos seguintes Requisitos Funcionais (RF):

### 🔐 Acesso e Perfil
- [x] **Cadastro e Login:** Criação de conta e autenticação segura de usuários.

### 💳 Gestão de Carteiras
- [x] **Múltiplas Carteiras:** Criação de carteiras (ex: Conta Corrente, Carteira Digital) com saldo inicial.
- [x] **Exclusão em Cascata:** Ao excluir uma carteira, todas as transações vinculadas a ela são removidas automaticamente.
- [x] **Cálculo Automático:** O saldo é recalculado automaticamente a cada nova transação.

### 💸 Transações (Receitas e Despesas)
- [x] **Registro Detalhado:** Inclusão de valor, data, categoria, descrição e carteira de origem/destino.
- [x] **Categorias Obrigatórias:** O sistema impede transações sem categoria ou com categorias inexistentes.
- [x] **Validação de Saldo:** O sistema **bloqueia** o registro de despesas caso o saldo da carteira seja insuficiente para cobrir o valor.

### 🎯 Planejamento Financeiro
- [x] **Metas (Mensais/Anuais):** Definição de metas com nome, valor-alvo e prazo, com barra de progresso automática.
- [x] **Objetivos Específicos:** Gestão de objetivos de longo prazo (ex: "Viagem", "Compra de Notebook") com acompanhamento baseado no saldo ou categorias específicas.
- [x] **Objetivos Específicos:** Gestão de objetivos de longo prazo (ex: "Viagem", "Compra de Notebook") com acompanhamento baseado no saldo ou carteira específicas.

### 📊 Relatórios e Dashboard
- [x] **Histórico Mensal:** Visualização de extrato filtrado por mês/ano.
- [x] **Indicadores:** Total de receitas, total de despesas e saldo final.
- [x] **Gráficos:** Relatórios visuais de gastos por categoria.

---

## 🛡️ Regras de Negócio e Tratamento de Erros

O backend implementa diversas exceções personalizadas para garantir que o sistema nunca entre em um estado inválido. Abaixo estão as principais regras tratadas:

### 💰 Financeiro & Transações
| Exceção | Descrição |
| :--- | :--- |
| `SaldoInsuficienteError` | Impede despesas maiores que o saldo disponível na carteira. |
| `ValorInvalidoError` | Bloqueia valores negativos ou zero em operações que exigem positivos. |
| `TransacaoInexistenteError` | Disparado ao tentar editar/excluir uma transação que não existe no banco. |

### 📂 Carteiras & Categorias
| Exceção | Descrição |
| :--- | :--- |
| `CarteiraJaExisteError` | Evita criação de carteiras com nomes duplicados para o mesmo usuário. |
| `CarteiraInexistenteError` | Garante que transações sejam vinculadas a carteiras reais. |
| `CategoriaJaExisteError` | Evita duplicidade no cadastro de categorias personalizadas. |
| `CategoriaInexistenteError` | Disparado ao tentar usar ou buscar uma categoria que não existe. |

### 🎯 Metas & Objetivos
| Exceção | Descrição |
| :--- | :--- |
| `MetaJaExisteError` | Impede a criação de metas duplicadas para a mesma categoria. |
| `MetaInexistenteError` | Tratamento para tentativas de acesso a metas não cadastradas. |
| `ObjetivoInexistenteError` | Tratamento para tentativas de acesso a objetivos inválidos. |

### 👤 Usuários
| Exceção | Descrição |
| :--- | :--- |
| `UsuarioJaExisteError` | Garante unicidade de e-mail/login no cadastro. |
| `UsuarioInexistenteError` | Tratamento de segurança para falhas de autenticação ou busca de ID. |

---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** [Python 3](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/)
* **Banco de Dados:** SQLite
* **ORM:** SQLAlchemy
* **Frontend:** HTML5, Tailwind CSS, JavaScript (Chart.js), Jinja2

---

## 🚀 Instalação e Execução

Siga o passo a passo para rodar o projeto localmente.

### Pré-requisitos
* Git
* Python 3.8 ou superior

### 1. Clone o repositório

```bash
git clone https://github.com/ASJoaoVictor/projeto_final_poo_2025.2.git
cd projeto_final_poo_2025.2
```

### 2. Crie e ative um ambiente virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a aplicação
```bash
# Via script (Linux/Mac)
./iniciar_app.sh

# Ou via Python direto (Windows/Linux/Mac)
python app.py
```
## 📝 Licença
Este projeto está sob a licença MIT. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
