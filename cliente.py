import socket
import time
import random

# Configurações
SERVER_IP = "localhost"
SERVER_PORT = 5000
TIMEOUT = 3.0  # Segundos para estourar o tempo 

# Inicialização do Socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT) # Define o temporizador do socket 

# Variável global de sequência
seq = 0

def checksum(data):
    return sum(ord(c) for c in data) % 256

def menu():
    print("\n===== MENU DE SIMULAÇÃO DO CANAL =====")
    print("1 - Entrega normal")
    print("2 - Corromper dados (Altera Checksum)")
    print("3 - Inserir atraso artificial (Delay)")
   
    try:
        return int(input("Escolha o comportamento para este envio: "))
    except:
        return 1

def send_packet(data):
    global seq
    
    # Prepara os dados brutos
    chk_real = checksum(data)
    
    # Exibe menu ANTES de entrar no loop de envio
    opcao = menu()
    
    # Lógica de manipulação para simular falhas 
    chk_to_send = chk_real
    simular_delay = False
    
    if opcao == 2:
        print("[CLIENTE-SIMULAÇÃO] 🔨 Os dados serão enviados CORROMPIDOS (Checksum inválido).")
        chk_to_send = 999  # Valor incorreto proposital [cite: 38]
    elif opcao == 3:
        print("[CLIENTE-SIMULAÇÃO] ⏳ Um atraso será inserido antes do envio.")
        simular_delay = True
    else:
        print("[CLIENTE-SIMULAÇÃO] Envio normal.")

# Loop de envio (Stop-and-Wait)
    while True:
        # Monta o pacote: seq|checksum|dados
        pacote = f"{seq}|{chk_to_send}|{data}"
        
        # Aplica o atraso se solicitado (simula latência da rede)
        if simular_delay:
            delay = random.randint(2, 4)
            print(f"[CLIENTE] ...Dormindo por {delay}s simulando atraso...")
            time.sleep(delay)
            simular_delay = False # Aplica atraso apenas na primeira tentativa (opcional)

        print(f"\n[CLIENTE] Enviando pacote (Seq: {seq})...")
        print(f"          Dados: '{data}' | Checksum Enviado: {chk_to_send}")
        
        sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))
        
        # Estado: Aguardando ACK 
        try:
            # Tenta receber resposta
            recv_data, _ = sock.recvfrom(1024)
            ack_msg = recv_data.decode()
            
            print(f"[CLIENTE] Mensagem recebida: {ack_msg}")

            if "ACK" in ack_msg:
                _, ack_seq_str = ack_msg.split("|")
                ack_seq = int(ack_seq_str)
                
                # Verifica se é o ACK esperado 
                if ack_seq == seq:
                    print(f"[CLIENTE] ✅ ACK {ack_seq} Recebido com sucesso!")
                    # Alterna sequência para o próximo pacote (0 -> 1 ou 1 -> 0)
                    seq = 1 - seq
                    break # Sai do loop de retransmissão
                else:
                    print(f"[CLIENTE] ⚠️ ACK incorreto recebido (Esperado: {seq}, Veio: {ack_seq}). Ignorando.")
            
        except socket.timeout:
            # Timeout estourou: Retransmitir 
            print(f"[CLIENTE] ⏰ TIMEOUT! Não recebi ACK para Seq {seq}. Retransmitindo...")
            print(f"[CLIENTE] (Causa provável: Pacote corrompido/ignorado pelo servidor ou ACK perdido)")



print("=== CLIENTE RDT 3.0 INICIADO ===")
while True:
    msg = input("\nDigite a mensagem a ser enviada (ou 'sair'): ")
    if msg.lower() == 'sair':
        break
    send_packet(msg)
