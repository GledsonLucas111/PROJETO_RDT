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