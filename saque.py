import customtkinter as ctk
import os
import json
import subprocess 
from datetime import datetime  # Importa a data e hora

# Nome dos arquivos JSON para armazenar o saldo e as transações
SALDO_FILE = "saldo.json"
TRANSACOES_FILE = "transacoes.json"

# Função para carregar o saldo do arquivo JSON
def load_saldo():
    if os.path.exists(SALDO_FILE):
        with open(SALDO_FILE, "r") as file:
            return json.load(file).get("saldo", 0.0)  # Retorna o saldo ou 0.0 se não existir
    return 0.0  # Retorna 0.0 se o arquivo não existir

# Função para carregar transações do arquivo JSON
def load_transacoes():
    if os.path.exists(TRANSACOES_FILE):
        with open(TRANSACOES_FILE, "r") as file:
            return json.load(file).get("transacoes", [])  # Retorna a lista de transações ou vazia
    return []  # Retorna lista vazia se o arquivo não existir

# Função para salvar o saldo no arquivo JSON
def save_saldo(valor):
    with open(SALDO_FILE, "w") as file:
        json.dump({"saldo": valor}, file, indent=4)

# Função para salvar transações no arquivo JSON
def save_transacoes(transacoes):
    with open(TRANSACOES_FILE, "w") as file:
        json.dump({"transacoes": transacoes}, file, indent=4)

# Função para atualizar o saldo na tela
def atualizar_saldo():
    novo_saldo = load_saldo()
    saldo_label.configure(text=f"Saldo disponível: R${novo_saldo:.2f}")

# Função para validar a entrada (apenas números)
def validar_entrada(value):
    return value.replace(".", "").isdigit() or value == ""  # Aceita apenas números ou campo vazio

# Função para processar um saque
def salvar_valor():
    valor = valor_entry.get()
    if valor.replace(".", "").isdigit():
        valor_float = float(valor)
        saldo_atual = load_saldo()
        transacoes = load_transacoes()
        
        # Obtém data e hora separadamente
        agora = datetime.now()
        data = agora.strftime("%d/%m/%Y")
        hora = agora.strftime("%H:%M:%S")
        
        # Filtra saques do dia atual
        saques_hoje = [t for t in transacoes if t["tipo"] == "SAQUE" and t["data"] == data]
        
        if len(saques_hoje) >= 3:
            saldo_label.configure(text="Limite de 3 saques diários atingido!")
            return
        
        if valor_float > 500:
            saldo_label.configure(text="Limite máximo por saque é R$500,00!")
            return
        
        if saldo_atual < valor_float:
            saldo_label.configure(text="Saldo insuficiente para saque!")
            return
        
        # Atualiza saldo e registra transação
        novo_saldo = saldo_atual - valor_float
        transacao = {"valor": valor_float, "data": data, "hora": hora, "tipo": "SAQUE"}
        transacoes.append(transacao)
        
        save_saldo(novo_saldo)
        save_transacoes(transacoes)
        atualizar_saldo()
        valor_entry.delete(0, "end")

# Função para abrir a janela de depósito
def abrir_deposito():
    app.destroy()  # Fecha a janela principal antes de abrir o depósito
    subprocess.run(["python", "painel_principal.py"], check=True)  # Chama o outro arquivo Python (deposito.py)

# Criando a interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("350x520")
app.title("Banco QAR V1")
app.configure(bg="#1E1E1E")

# Criando um frame
frame = ctk.CTkFrame(app, width=350, height=520, corner_radius=15, fg_color="#2C2F33")
frame.place(relx=0.5, rely=0.5, anchor="center")
frame.pack_propagate(False)

# Cabeçalho azul
header = ctk.CTkFrame(frame, width=350, height=100, fg_color="#3B82F6")
header.pack_propagate(False)
header.pack(side="top", fill="x")

title_label = ctk.CTkLabel(header, text="Qual é o valor do Saque?", font=("Arial", 22, "bold"), text_color="white")
title_label.pack(expand=True)

# Exibir saldo atual
saldo_label = ctk.CTkLabel(frame, text="", font=("Arial", 16), text_color="white")
saldo_label.pack(pady=10)
atualizar_saldo()  # Atualiza o saldo na inicialização

header2 = ctk.CTkFrame(frame, width=330, height=5, fg_color="#3B82F6")
header2.pack(pady=10)

# Texto fixo acima da entrada
valor_label = ctk.CTkLabel(frame, text="Digite seu valor aqui:", font=("Arial", 14), text_color="white")
valor_label.pack()

# Campo de entrada (aceita apenas números)
validacao = app.register(validar_entrada)
valor_entry = ctk.CTkEntry(frame, width=280, height=40, corner_radius=10, validate="key", validatecommand=(validacao, "%P"))
valor_entry.pack(pady=10)

# Botão para salvar o valor no JSON
salvar_button = ctk.CTkButton(frame, text="Retirar", command=salvar_valor)
salvar_button.pack(pady=10)

# Botão Voltar
voltar_button2 = ctk.CTkButton(frame, width=40, height=40, text="<", command=abrir_deposito)
voltar_button2.place(x=25, y=440)  # Ajuste a posição para a parte inferior esquerda

app.mainloop()
