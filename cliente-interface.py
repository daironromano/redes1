import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import Frame

# Configurações do cliente
HOST = '127.0.0.1'
PORT = 12345

# Função para receber mensagens do servidor
def recebe_mensagens(cliente_socket, area_texto):
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            if mensagem:
                area_texto.config(state=tk.NORMAL)
                area_texto.insert(tk.END, f'{mensagem}\n', 'left')
                area_texto.config(state=tk.DISABLED)
                area_texto.yview(tk.END)
        except:
            print("Erro ao receber mensagem. Servidor desconectado\n")
            cliente_socket.close()
            break

# Função para enviar mensagens ao servidor
def envia_mensagens(cliente_socket, mensagem_entry, area_texto, usuario):
    mensagem = mensagem_entry.get().strip()
    if mensagem:
        cliente_socket.send(f'<{usuario}> {mensagem}'.encode('utf-8'))
        area_texto.config(state=tk.NORMAL)
        area_texto.insert(tk.END, f'Você: {mensagem}\n', 'right')
        area_texto.config(state=tk.DISABLED)
        area_texto.yview(tk.END)
        mensagem_entry.delete(0, tk.END)

def main():
    usuario = input("Usuário>> ")
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((HOST, PORT))
        print(f"Conectado ao servidor no endereço IP: {HOST}, na porta: {PORT}")
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao servidor no endereço IP: {HOST}, na porta: {PORT}. O servidor pode não estar em execução.")
        return

    # Configuração da interface gráfica
    janela = tk.Tk()
    janela.title("Redes de Apoio")

    # Configurando área do chat
    janela.geometry("440x600")

    # Frame esquerdo dividido verticalmente
    frame_esquerdo = Frame(janela, bg="#87CEEB")
    frame_esquerdo.place(relx=0, rely=0, relwidth=0.5, relheight=1)

    # Subdividindo o frame esquerdo em dois
    frame_superior_esquerdo = Frame(frame_esquerdo, bg="#87CEEB")
    frame_superior_esquerdo.place(relx=0, rely=0, relwidth=1, relheight=0.5)

    frame_inferior_esquerdo = Frame(frame_esquerdo, bg="#87CEEB")
    frame_inferior_esquerdo.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

    # Adicionando o título: Redes de Apoio
    label_titulo = tk.Label(frame_superior_esquerdo, text="Redes\nde\nApoio", font=("Roboto", 20, "bold"), bg="#F0FFFF", width=10, height=5, anchor="center")
    label_titulo.pack(expand=True)

    # Adicionando o nome do usuário no frame inferior esquerdo
    label_usuario = tk.Label(frame_inferior_esquerdo, text="Usuário:", font=("Roboto", 12), bg="#87CEEB")
    label_usuario.pack(anchor="n", pady=(0,10))

    # Adicionando o nome do usuário abaixo do texto "Usuário:"
    label_usuario = tk.Label(frame_inferior_esquerdo, text=usuario, font=("Roboto", 16), bg="#FFFFFF", width=16, height=2)
    label_usuario.pack(ancho="n", pady=(2,0))

    # Frame direito para o chat
    frame_direito = Frame(janela, bg="lightblue")
    frame_direito.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    # Configurando a área de texto no frame direito
    area_texto = scrolledtext.ScrolledText(frame_direito, state=tk.DISABLED, bg="lightblue", bd=0, relief="flat", font=("Roboto", 10))
    area_texto.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    area_texto.tag_config('left', justify='left', background="#e6e6e6", foreground="#000000", borderwidth=2, relief="solid")
    area_texto.tag_config('right', justify='right', background="#d1ffd1", foreground="#000000", borderwidth=2, relief="solid")

    # Configurando a área de entrada de mensagens no frame direito
    mensagem_frame = tk.Frame(frame_direito, bg="#ffffff", bd=1, relief="solid")
    mensagem_frame.pack(padx=10, pady=10, fill=tk.X)
    mensagem_entry = tk.Entry(mensagem_frame, width=50, bd=0, relief="flat", bg="#ffffff", fg="#000000")
    mensagem_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
    mensagem_entry.bind("<Return>", lambda event: envia_mensagens(cliente_socket, mensagem_entry, area_texto, usuario))

    # Iniciar a thread para receber mensagens
    threading.Thread(target=recebe_mensagens, args=(cliente_socket, area_texto)).start()

    # Iniciar o loop principal
    janela.mainloop()

if __name__ == "__main__":
        main()