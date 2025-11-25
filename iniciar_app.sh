#!/bin/bash

# Define o caminho para o ambiente virtual
VENV_PATH="./venv"

# Define o nome do script Python a ser executado
APP_SCRIPT="app.py"

# --- Início da execução ---

echo "Verificando e ativando o ambiente virtual..."

# Verifica se o diretório do ambiente virtual existe
if [ ! -d "$VENV_PATH" ]; then
    echo "Erro: Ambiente virtual não encontrado em $VENV_PATH"
    echo "Certifique-se de ter criado o ambiente (ex: python3 -m venv venv) e instalado as dependências (ex: pip install -r requirements.txt)."
    exit 1
fi

# Ativa o ambiente virtual (para Linux/macOS)
source "$VENV_PATH/bin/activate"

# Se estiver usando Windows Git Bash, o comando pode ser diferente:
# source "$VENV_PATH/Scripts/activate"

echo "Ambiente virtual ativado."
echo "Executando o script Python: $APP_SCRIPT"

# Executa o script Python usando o interpretador do ambiente ativado
python "$APP_SCRIPT"

# Opcional: Desativa o ambiente virtual após a execução
# deactivate

echo "Script concluído."
