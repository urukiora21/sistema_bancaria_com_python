import customtkinter as ctk  # Biblioteca para criar interfaces modernas
from PIL import Image  # Manipulação de imagens
import os  # Para manipular arquivos do sistema
import subprocess
import json  # Para salvar e carregar usuários
import sys  # Para fechar o aplicativo completamente

# Nome dos arquivos JSON para armazenar o saldo e as transações
SALDO_FILE = "saldo.json"
TRANSACOES_FILE = "transacoes.json"

class App(ctk.CTk):
    def __init__(self):
        """
        Inicializa a janela principal do aplicativo.
        Configura a interface gráfica, carrega imagens, e configurações iniciais.
        """
        super().__init__()

        # Configurações da Janela Principal
        self.title("Banco QAR V1")
        self.geometry("350x520")
        self.resizable(False, False)  # Impede redimensionamento

        # Diretório das imagens
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagens")
        self.logo_path = os.path.join(image_path, "painel1.png")
        self.cartao_path = os.path.join(image_path, "cartao.png")  
        self.extratobranco_path = os.path.join(image_path, "extratobranco.png")  
        self.depositobranco_path = os.path.join(image_path, "depositobranco.png")  
        self.saquebranco_path = os.path.join(image_path, "saquebranco.png")  

        # Carregar imagens
        self.carregar_imagens()

        # Exibir a imagem de fundo, se existir
        if os.path.exists(self.logo_path):
            bg_image = ctk.CTkImage(light_image=Image.open(self.logo_path), size=(350, 520))
            bg_label = ctk.CTkLabel(self, image=bg_image, text="")
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        else:
            print(f"Erro: Imagem '{self.logo_path}' não encontrada!")

        # Exibir a imagem do cartão, se existir
        if os.path.exists(self.cartao_path):
            cartao_image = ctk.CTkImage(light_image=Image.open(self.cartao_path), size=(300, 180))
            self.label_cartao = ctk.CTkLabel(self, image=cartao_image, text="")
            self.label_cartao.place(x=25, y=320)
        else:
            print(f"Erro: Imagem '{self.cartao_path}' não encontrada!")

        # Label de Boas-Vindas
        self.label_boas_vindas = ctk.CTkLabel(
            self, text="Olá Jessie",
            text_color="#ffffff",
            font=("Arial", 12),
            fg_color="#2c2f33"
        )
        self.label_boas_vindas.place(x=15, y=108)

        # Label da Conta
        self.label_conta = ctk.CTkLabel(
            self, text="Conta",
            text_color="#ffffff",
            font=("Arial", 18),
            fg_color="#2c2f33"
        )
        self.label_conta.place(x=15, y=140)

        # Exibir saldo atual
        self.saldo_label = ctk.CTkLabel(self, text="", font=("Arial", 16),fg_color="#2c2f33", text_color="white")
        self.saldo_label.place(x=15, y=160)  # Ajuste as coordenadas conforme necessário
        self.atualizar_saldo()  # Atualiza o saldo na inicialização

        # Botões de Ação
        self.botao_deposito = ctk.CTkButton(
            self, text="", image=self.depositobranco_image, height=80, width=80, 
            compound="top",   # Move a imagem mais para cima
            command=self.abrir_deposito  
        )
        self.botao_deposito.place(x=25, y=220)

        self.botao_extrato = ctk.CTkButton(
            self, text="", image=self.extratobranco_image, height=80, width=80, 
            compound="top",   # Move a imagem mais para cima
            command=self.abrir_extrato
        )
        self.botao_extrato.place(x=132, y=220)

        self.botao_saque = ctk.CTkButton(
            self, text="", image=self.saquebranco_image, height=80, width=80, 
            compound="top",   # Move a imagem mais para cima
            command=self.abrir_saque  # Chama a função correta
        )
        self.botao_saque.place(x=240, y=220)

    def carregar_imagens(self):
        """
        Carrega todas as imagens necessárias para os botões e outros elementos gráficos.
        Caso a imagem não seja encontrada, imprime uma mensagem de erro.
        """
        # Carregar imagens
        if os.path.exists(self.extratobranco_path):
            self.extratobranco_image = ctk.CTkImage(light_image=Image.open(self.extratobranco_path), size=(60, 60))
        else:
            print(f"Erro: Imagem '{self.extratobranco_path}' não encontrada!")
            self.extratobranco_image = None

        if os.path.exists(self.depositobranco_path):
            self.depositobranco_image = ctk.CTkImage(light_image=Image.open(self.depositobranco_path), size=(60, 60))
        else:
            print(f"Erro: Imagem '{self.depositobranco_path}' não encontrada!")
            self.depositobranco_image = None

        if os.path.exists(self.saquebranco_path):
            self.saquebranco_image = ctk.CTkImage(light_image=Image.open(self.saquebranco_path), size=(60, 60))
        else:
            print(f"Erro: Imagem '{self.saquebranco_path}' não encontrada!")
            self.saquebranco_image = None

    def load_saldo(self):
        """
        Carrega o saldo armazenado no arquivo JSON.
        Retorna 0.0 se o arquivo não existir ou se não houver saldo.
        """
        if os.path.exists(SALDO_FILE):
            with open(SALDO_FILE, "r") as file:
                return json.load(file).get("saldo", 0.0)
        return 0.0  # Retorna 0.0 se o arquivo não existir

    def atualizar_saldo(self):
        """
        Atualiza a exibição do saldo na interface gráfica.
        """
        novo_saldo = self.load_saldo()
        self.saldo_label.configure(text=f"R${novo_saldo:.2f}")

    def abrir_deposito(self):
        """
        Abre a tela de depósito, fechando a janela principal.
        Executa o script 'deposito.py' em um novo processo.
        """
        self.destroy()  # Fecha a janela principal antes de abrir o depósito
        subprocess.run(["python", "deposito.py"], check=True)  # Chama o outro arquivo Python

    def abrir_saque(self):
        """
        Abre a tela de saque, fechando a janela principal.
        Executa o script 'saque.py' em um novo processo.
        """
        self.destroy()  # Fecha a janela principal antes de abrir o saque
        subprocess.run(["python", "saque.py"], check=True)  # Chama o outro arquivo Python

    def abrir_extrato(self):
        """
        Abre a tela de extrato, fechando a janela principal.
        Executa o script 'extrato.py' em um novo processo.
        """
        self.destroy()  # Fecha a janela principal antes de abrir o extrato
        subprocess.run(["python", "extrato.py"], check=True)  # Chama o outro arquivo Python

    def abrir_janela(self, janela):
        """
        Fecha o aplicativo atual e abre uma nova janela selecionada.
        """
        self.destroy()  # Fecha a janela atual
        nova_janela = janela()  # Cria uma nova janela
        nova_janela.mainloop()  # Inicia a nova janela

if __name__ == "__main__":
    """
    Inicia a aplicação configurando o modo escuro e rodando a janela principal.
    """
    ctk.set_appearance_mode("dark")  # Define o modo escuro como padrão
    app = App()
    app.mainloop()
