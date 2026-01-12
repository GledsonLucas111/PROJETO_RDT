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