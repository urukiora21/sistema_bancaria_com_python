import customtkinter as ctk  # Importa a biblioteca customtkinter para criar a interface gráfica
import os  # Importa o módulo os para interagir com o sistema de arquivos
import json  # Importa o módulo json para manipular dados em formato JSON
import subprocess  # Importa o módulo subprocess para executar comandos do sistema operacional
from datetime import datetime  # Importa a classe datetime para manipulação de datas e horas

# Nome dos arquivos JSON para armazenar o saldo e as transações
SALDO_FILE = "saldo.json"  # Arquivo onde o saldo será armazenado
TRANSACOES_FILE = "transacoes.json"  # Arquivo onde as transações serão armazenadas

# Função para carregar o saldo do arquivo JSON
def load_saldo():
    if os.path.exists(SALDO_FILE):  # Verifica se o arquivo do saldo existe
        with open(SALDO_FILE, "r") as file:  # Abre o arquivo em modo leitura
            return json.load(file).get("saldo", 0.0)  # Retorna o saldo ou 0.0 se não encontrado
    return 0.0  # Retorna 0.0 caso o arquivo não exista

# Função para carregar transações do arquivo JSON
def load_transacoes():
    if os.path.exists(TRANSACOES_FILE):  # Verifica se o arquivo de transações existe
        with open(TRANSACOES_FILE, "r") as file:  # Abre o arquivo em modo leitura
            return json.load(file).get("transacoes", [])  # Retorna a lista de transações ou uma lista vazia
    return []  # Retorna uma lista vazia caso o arquivo não exista

# Função para salvar o saldo no arquivo JSON
def save_saldo(valor):
    with open(SALDO_FILE, "w") as file:  # Abre o arquivo do saldo em modo escrita (sobrescreve)
        json.dump({"saldo": valor}, file, indent=4)  # Salva o saldo no arquivo JSON com indentação de 4 espaços

# Função para salvar transações no arquivo JSON
def save_transacoes(transacoes):
    with open(TRANSACOES_FILE, "w") as file:  # Abre o arquivo das transações em modo escrita (sobrescreve)
        json.dump({"transacoes": transacoes}, file, indent=4)  # Salva a lista de transações no arquivo JSON com indentação de 4 espaços

# Função para abrir a janela de depósito
def abrir_deposito():
    app.destroy()  # Fecha a janela principal antes de abrir a janela de depósito
    subprocess.run(["python", "painel_principal.py"], check=True)  # Chama o script painel_principal.py

# Criando a interface gráfica
ctk.set_appearance_mode("dark")  # Define o modo de aparência da interface como "escuro"
ctk.set_default_color_theme("blue")  # Define o tema de cores como "azul"

app = ctk.CTk()  # Cria a janela principal da aplicação
app.geometry("350x520")  # Define as dimensões da janela principal
app.title("Sistema Bancário")  # Define o título da janela
app.configure(bg="#1E1E1E")  # Define a cor de fundo da janela principal

frame = ctk.CTkFrame(app, width=350, height=520, corner_radius=15, fg_color="#2C2F33")  # Cria um frame para o conteúdo principal
frame.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona o frame no centro da janela
frame.pack_propagate(False)  # Impede que o frame ajuste o tamanho baseado no conteúdo

header = ctk.CTkFrame(frame, width=350, height=100, fg_color="#3B82F6")  # Cria um header com fundo azul
header.pack_propagate(False)  # Impede que o header ajuste seu tamanho baseado no conteúdo
header.pack(side="top", fill="x")  # Posiciona o header no topo e o preenche horizontalmente

title_label = ctk.CTkLabel(header, text="Extrato", font=("Arial", 22, "bold"), text_color="white")  # Cria um rótulo de título para o extrato
title_label.pack(expand=True)  # Expande o rótulo para ocupar o espaço disponível no header

# Criando os títulos das colunas para o extrato
coluna_titulo_tipo = ctk.CTkLabel(frame, text="TIPO", font=("Arial", 14), text_color="white")
coluna_titulo_valor = ctk.CTkLabel(frame, text="VALOR", font=("Arial", 14), text_color="white")
coluna_titulo_data  = ctk.CTkLabel(frame, text="DATA", font=("Arial", 14), text_color="white")
coluna_titulo_hora  = ctk.CTkLabel(frame, text="HORA", font=("Arial", 14), text_color="white")

# Posiciona os rótulos de coluna na interface
coluna_titulo_tipo.place(x=20, y=120)
coluna_titulo_valor.place(x=100, y=120)
coluna_titulo_data.place(x=180, y=120)
coluna_titulo_hora.place(x=260, y=120)

# Criação de um frame para exibir as transações
frame_inferior = ctk.CTkFrame(frame, width=330, height=280, corner_radius=15, fg_color="#444444")
frame_inferior.place(relx=0.5, y=140 + 10, anchor="n")

# Cria um canvas para exibir as transações com uma barra de rolagem
canvas = ctk.CTkCanvas(frame_inferior, bg="#444444", width=330, height=280)
scrollbar = ctk.CTkScrollbar(frame_inferior, orientation="vertical", command=canvas.yview)  # Cria uma barra de rolagem vertical
canvas.configure(yscrollcommand=scrollbar.set)  # Conecta a barra de rolagem ao canvas
scrollbar.pack(side="right", fill="y")  # Posiciona a barra de rolagem à direita
canvas.pack(side="left", fill="both", expand=True)  # Posiciona o canvas à esquerda e o expande

# Cria um frame dentro do canvas para exibir as transações
frame_transacoes = ctk.CTkFrame(canvas, fg_color="#444444")
canvas.create_window((0, 0), window=frame_transacoes, anchor="nw")  # Cria uma janela dentro do canvas

transacoes = load_transacoes()  # Carrega as transações do arquivo JSON
for i, transacao in enumerate(transacoes):  # Itera sobre as transações
    tipo = transacao.get("tipo", "Desconhecido")  # Obtém o tipo da transação
    valor = f"R$ {transacao.get('valor', 0.0):,.2f}"  # Formata o valor da transação
    data = transacao.get("data", "Desconhecida")  # Obtém a data da transação
    hora = transacao.get("hora", "Desconhecida")  # Obtém a hora da transação

    # Criação dos rótulos para cada transação
    tipo_label = ctk.CTkLabel(frame_transacoes, text=tipo, font=("Arial", 12), text_color="white")
    valor_label = ctk.CTkLabel(frame_transacoes, text=valor, font=("Arial", 12), text_color="white")
    data_label = ctk.CTkLabel(frame_transacoes, text=data, font=("Arial", 12), text_color="white")
    hora_label = ctk.CTkLabel(frame_transacoes, text=hora, font=("Arial", 12), text_color="white")

    # Posiciona os rótulos na tela usando grid
    tipo_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")
    valor_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    data_label.grid(row=i, column=2, padx=10, pady=5, sticky="w")
    hora_label.grid(row=i, column=3, padx=22, pady=5, sticky="w")

frame_transacoes.update_idletasks()  # Atualiza os itens no frame de transações
canvas.config(scrollregion=canvas.bbox("all"))  # Ajusta a região de rolagem do canvas para acomodar todas as transações

# Botão Voltar
voltar_button2 = ctk.CTkButton(frame, width=40, height=40, text="<", command=abrir_deposito)  # Cria um botão "Voltar" para abrir a janela de depósito
voltar_button2.place(x=25, y=440)  # Posiciona o botão no canto inferior esquerdo

app.mainloop()  # Inicia o loop principal da interface gráfica
