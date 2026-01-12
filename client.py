import socket
import time

SERVER_IP = "localhost"
SERVER_PORT = 5000
TIMEOUT = 3.0 # Tempo de espera do cliente 

def checksum(data):
    return sum(ord(c) for c in data) % 256

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    
    seq = 0

    while True:
        msg = input("\nDigite a mensagem (ou 's' para sair): ")
        if msg.lower() == 's': break

        # Menu de Simulação 
        print("\n1. Entrega Normal\n2. Corromper Dados\n3. Atraso\n")
        opcao = input("Escolha: ")

        # Define as variáveis de simulação
        check_envio = checksum(msg)
        flag_atraso = 0

        if opcao == "2":
            check_envio = 999 # Simula corrupção 
        elif opcao == "3":
            flag_atraso = 1 # Instrução para o servidor atrasar 

        # Monta o pacote: "seq|checksum|flag_atraso|mensagem"
        packet = f"{seq}|{check_envio}|{flag_atraso}|{msg}"

        # Loop de Retransmissão (RDT 3.0)
        while True:
            print(f"[CLIENTE] Enviando Seq={seq} (Atraso={flag_atraso})...") 
            sock.sendto(packet.encode(), (SERVER_IP, SERVER_PORT))
            
            try:
                # Aguarda confirmação 
                data_ack, _ = sock.recvfrom(1024)
                ack_msg = data_ack.decode()
                print(f"[CLIENTE] Resposta: {ack_msg}")

                if f"ACK|{seq}" in ack_msg:
                    print("[CLIENTE] ✅ Sucesso! Alternando sequência.")
                    seq = 1 - seq
                    break # Sai do loop de retransmissão
            
            except socket.timeout:
                print("[CLIENTE] ⏰ TIMEOUT! O servidor demorou ou o pacote sumiu.") 
                print("[CLIENTE] Retransmitindo pacote...") 
                # O loop 'while True' enviará novamente o mesmo pacote

if __name__ == "__main__":
    main()