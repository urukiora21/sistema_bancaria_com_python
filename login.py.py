import customtkinter as ctk  # Biblioteca para criar interfaces gráficas modernas
import json  # Módulo para manipulação de arquivos JSON
import os  # Módulo para manipulação de arquivos e diretórios do sistema
import painel_principal  # Importando o módulo da janela principal do sistema
from PIL import Image  # Módulo para manipulação de imagens (Python Imaging Library)

# Nome do arquivo JSON onde os dados dos usuários serão armazenados
USER_DATA_FILE = "users.json"

# Função para carregar os usuários do arquivo JSON
def load_users():
    """
    Carrega os usuários do arquivo JSON. Se o arquivo não existir,
    retorna um dicionário com um usuário padrão (admin).
    """
    if os.path.exists(USER_DATA_FILE):  # Verifica se o arquivo de usuários existe
        with open(USER_DATA_FILE, "r") as file:  # Abre o arquivo para leitura
            return json.load(file)  # Retorna o conteúdo do arquivo como dicionário
    return {"admin": "admin"}  # Retorna um dicionário com um usuário pré-cadastrado

# Função para salvar os usuários no arquivo JSON
def save_users(users):
    """
    Salva o dicionário de usuários no arquivo JSON.
    """
    with open(USER_DATA_FILE, "w") as file:  # Abre o arquivo para escrita (sobrescreve o arquivo existente)
        json.dump(users, file, indent=4)  # Salva o dicionário de usuários no formato JSON com indentação de 4 espaços

# Função para validar o CPF (aceita apenas números ou campo vazio)
def validar_cpf(text):
    return text.isdigit() or text == ""  # Aceita apenas números ou campo vazio

# Função para garantir que o usuário 'admin' esteja cadastrado no sistema
def ensure_admin_user():
    """
    Garante que o usuário 'admin' esteja cadastrado no sistema.
    Se o arquivo não existir, cria um arquivo com o usuário admin.
    """
    if not os.path.exists(USER_DATA_FILE):  # Verifica se o arquivo de usuários não existe
        save_users({"admin": "admin"})  # Cria o arquivo com o usuário admin pré-cadastrado

# Chama a função para garantir que o usuário 'admin' seja criado, caso necessário
ensure_admin_user()

# Função para autenticar o usuário durante o login
def authenticate_user(username, password, login_window, error_label):
    """
    Verifica se o nome de usuário e a senha são válidos.
    Se forem, fecha a janela de login e abre o painel principal.
    Caso contrário, exibe uma mensagem de erro.
    """
    users = load_users()  # Carrega os usuários do arquivo JSON
    if username in users and users[username] == password:  # Verifica se o nome de usuário e senha estão corretos
        print("Login bem-sucedido!")  # Mensagem no terminal (pode ser removida em produção)
        login_window.destroy()  # Fecha a janela de login
        painel_principal.App().mainloop()  # Abre a janela principal do sistema
    else:
        error_label.configure(text="⚠   Usuário ou senha incorretos  ⚠", text_color="white")  # Exibe a mensagem de erro

# Função que cria a tela de login
def login_screen():
    """
    Cria a janela de login utilizando a biblioteca CustomTkinter.
    """
    ctk.set_appearance_mode("dark")  # Define o modo escuro para a interface
    ctk.set_default_color_theme("blue")  # Define a cor do tema como azul

    # Criando a janela principal da tela de login
    app = ctk.CTk()  # Cria a janela principal
    app.geometry("350x520")  # Define o tamanho da janela
    app.title("Banco QAR V1")  # Define o título da janela
    app.configure(bg="#1E1E1E")  # Define a cor de fundo como cinza escuro
    app.resizable(False, False)  # Impede o redimensionamento da janela

    # Definindo o diretório das imagens
    image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imagens")

    # Caminho da imagem do logo
    logo_path = os.path.join(image_path, "base_superior.png")

    # Carrega a imagem do logo
    base_superior = ctk.CTkImage(light_image=Image.open(logo_path), size=(350, 150))  # Ajusta o tamanho da imagem

    # Criando um frame centralizado para o conteúdo da tela de login
    frame = ctk.CTkFrame(app, width=350, height=600, corner_radius=15, fg_color="#2C2F33")  # Cria o frame de login
    frame.place(relx=0.5, rely=0.5, anchor="center")  # Posiciona o frame no centro da tela

    # Exibe o logo no topo do frame
    logo_label = ctk.CTkLabel(frame, image=base_superior , text="")  # Cria o rótulo do logo
    logo_label.pack(pady=5)  # Adiciona o logo com um padding de 5

    # Rótulo de erro (inicialmente vazio)
    error_label = ctk.CTkLabel(frame, text="", text_color="white", font=("Arial", 12))  # Cria o rótulo de erro
    error_label.pack(pady=5)  # Adiciona o rótulo de erro

    # Campos de entrada para o nome de usuário e senha
    username_entry = ctk.CTkEntry(frame, placeholder_text="usuario", width=280, height=40, corner_radius=10)  # Campo de entrada para o usuário
    username_entry.pack(pady=10)  # Adiciona o campo de entrada com padding de 10

    password_entry = ctk.CTkEntry(frame, placeholder_text="Senha", show="*", width=280, height=40, corner_radius=10)  # Campo de entrada para a senha
    password_entry.pack(pady=10)  # Adiciona o campo de senha com padding de 10

    # Função para permitir que a tecla "Enter" execute o login
    def on_enter(event=None):
        authenticate_user(username_entry.get(), password_entry.get(), app, error_label)  # Chama a função de autenticação

    # Adiciona evento de tecla "Enter" aos campos de entrada
    app.bind("<Return>", on_enter)  # Associa o evento "Enter" à função de login

    # Botão de login
    login_button = ctk.CTkButton(
        frame, text="ENTRAR", fg_color="#3B82F6", hover_color="#2563EB", text_color="white",  # Define o botão de login
        width=280, height=40, corner_radius=10,
        command=on_enter  # Quando clicado, executa a função de login
    )
    login_button.pack(pady=15)  # Adiciona o botão com padding de 15

    # Links informativos
    forgot_password_label = ctk.CTkLabel(frame, text="Esqueceu o nome de usuário/senha?", text_color="#93C5FD", font=("Arial", 12))  # Rótulo de recuperação
    forgot_password_label.pack(pady=5)  # Adiciona o rótulo com padding de 5

    forgot_password_label = ctk.CTkLabel(frame, text="user:admin / senha:admin", text_color="#93C5FD", font=("Arial", 12))  # Informações de login
    forgot_password_label.pack(pady=5)  # Adiciona o rótulo com padding de 5

    register_label = ctk.CTkLabel(frame, text="CONTACTE O ADMINISTRADOR", text_color="#3B82F6", font=("Arial", 13, "bold"))  # Rótulo de contato com administrador
    register_label.pack(pady=20)  # Adiciona o rótulo de contato

    # Inicia a interface gráfica
    app.mainloop()  # Inicia o loop principal da interface

# Executa a tela de login se este arquivo for executado diretamente
if __name__ == "__main__":
    login_screen()  # Chama a função que cria a tela de login
