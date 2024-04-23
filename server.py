import socket

# Endereço e porta do servidor
HOST = '127.0.0.1'  # localhost
PORT = 65432

# Cria um socket UDP
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s_UDP:
    # Liga o socket ao endereço e porta especificados
    s_UDP.bind((HOST, PORT))
    print('Aguardando mensagens...')
    while True:
        # Recebe os dados e o endereço do cliente
        data, addr = s_UDP.recvfrom(1024)
        data = int.from_bytes(data)
        
        print('Mensagem recebida de {}: {}'.format(addr, data ))
