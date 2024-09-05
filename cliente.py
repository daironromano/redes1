import socket
import threading

# Configurações do cliente
HOST = '127.0.0.1'  # Endereço IP do servidor
PORT = 12345        # Porta do servidor
# Função para receber mensagens do servidor
def recebe_mensagens(cliente_socket):
    while True:
        try:
            mensagem = cliente_socket.recv(1024).decode('utf-8')
            if mensagem:
                print(mensagem)
        except:
            print("Erro ao receber mensagem. Servidor desconectado\n")
            cliente_socket.close()
            break

def envia_menssagens(cliente_socket, usuario):

    # Loop para enviar mensagens ao servidor
    while True:
        try:
            mensagem = input().strip()
            if mensagem:  # Verifica se a mensagem não está vazia
                cliente_socket.send(f'<{usuario}> {mensagem}'.encode('utf-8'))
        except KeyboardInterrupt:
            print("Desconectando do servidor...")
            cliente_socket.close()
            break

def main():
    usuario = input("Usuário>> ")

    # Configuração do socket do cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        cliente_socket.connect((HOST, PORT))
        print(f"Conectado ao servidor no endereço IP: {HOST}, na porta: {PORT}")
    except ConnectionRefusedError:
        print(f"Não foi possível conectar ao servidor no endereço IP: {HOST}, na porta: {PORT}. O servidor pode não estar em execução.")
        return

    # Inicia a thread para receber mensagens
    threading.Thread(target=recebe_mensagens, args=(cliente_socket,)).start()

    # Chama a função para enviar mensagens
    envia_menssagens(cliente_socket, usuario)

main()
