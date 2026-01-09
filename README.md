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
- [x] **Edição/Exclusão:** Permite alterar nome/descrição ou excluir carteiras (somente se não houver transações vinculadas).
- [x] **Cálculo Automático:** O saldo é recalculado automaticamente a cada nova transação.

### 💸 Transações (Receitas e Despesas)
- [x] **Registro Detalhado:** Inclusão de valor, data, categoria, descrição e carteira de origem/destino.
- [x] **Categorias Obrigatórias:** O sistema impede transações sem categoria ou com categorias inexistentes.
- [x] **Validação de Saldo:** O sistema **bloqueia** o registro de despesas caso o saldo da carteira seja insuficiente para cobrir o valor.

### 🎯 Planejamento Financeiro
- [x] **Metas (Mensais/Anuais):** Definição de metas com nome, valor-alvo e prazo, com barra de progresso automática.
- [x] **Objetivos Específicos:** Gestão de objetivos de longo prazo (ex: "Viagem", "Compra de Notebook") com acompanhamento baseado no saldo ou categorias específicas.

### 📊 Relatórios e Dashboard
- [x] **Histórico Mensal:** Visualização de extrato filtrado por mês/ano.
- [x] **Indicadores:** Total de receitas, total de despesas e saldo final.
- [x] **Gráficos:** Relatórios visuais de gastos por categoria.

---

## 🛡️ Tratamento de Erros e Regras de Negócio

Para garantir a consistência do sistema, foram implementadas as seguintes exceções personalizadas:

1.  **`SaldoInsuficienteError`**: Disparado ao tentar registrar uma despesa maior que o saldo atual da carteira.
2.  **`CategoriaInvalidaError`**: Disparado se o usuário tentar forçar uma categoria que não existe no sistema.
3.  **`ValorInvalidoError`**: Disparado para tentativas de input de valores negativos ou formatos incorretos.

---

## 🛠 Tecnologias Utilizadas

* **Linguagem:** [Python 3](https://www.python.org/)
* **Framework Web:** [Flask](https://flask.palletsprojects.com/)
* **Banco de Dados:** SQLite (Desenvolvimento) / MySQL (Produção)
* **ORM:** SQLAlchemy
* **Frontend:** HTML5, CSS3, Tailwind, Jinja2

---

## 🚀 Instalação e Execução

Siga o passo a passo para rodar o projeto localmente.

### Pré-requisitos
* Git
* Python 3.8 ou superior

### 1. Clone o repositório

```bash
git clone [https://github.com/SEU_USUARIO/financas-pessoais.git](https://github.com/SEU_USUARIO/financas-pessoais.git)
cd financas-pessoais
