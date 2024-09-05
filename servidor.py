import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345        # Porta do servidor

# Lista para armazenar os clientes conectados
clientes = []

# Função para lidar com as mensagens recebidas dos clientes
def lidar_com_clientes(cliente_socket):
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            if mensagem:
                print(f"Mensagem recebida de {cliente_socket.getpeername()}: {mensagem}")
                broadcast(mensagem, cliente_socket)
            else:
                remove(cliente_socket)
                break
        except:
            remove(cliente_socket)
            break

# Função para retransmitir mensagens para todos os clientes
def broadcast(mensagem, cliente_socket):
    for cliente in clientes:
        if cliente != cliente_socket:
            try:
                cliente.send(mensagem.encode('utf-8'))
                print(f"Mensagem retransmitida para {cliente.getpeername()}")
            except:
                remove(cliente)

# Função para remover clientes desconectados
def remove(cliente_socket):
    if cliente_socket in clientes:
        clientes.remove(cliente_socket)
        print(f"Cliente {cliente_socket.getpeername()} desconectado")

def main():
    # Configuração do socket do servidor
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        servidor_socket.bind((HOST, PORT))
        servidor_socket.listen()

        print(f"Servidor iniciado no endereço IP: {HOST}, na porta: {PORT}")
    except:
        return print("\nNão foi possível iniciar o servidor!\n")

    while True:
        cliente_socket, endereco_do_cliente = servidor_socket.accept()
        clientes.append(cliente_socket)
        print(f"Conexão estabelecida com {endereco_do_cliente}")
        threading.Thread(target=lidar_com_clientes, args=(cliente_socket,)).start()
main()
