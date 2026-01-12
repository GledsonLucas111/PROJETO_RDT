import socket
import time


SERVER_PORT = 5000

    # Checksum simples (soma dos valores ASCII mod 256)
def checksum(data):
    return sum(ord(c) for c in data) % 256

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", SERVER_PORT))

    print(f"=== SERVIDOR RDT 3.0 AGUARDANDO NA PORTA {SERVER_PORT} ===")
    
    # RDT 3.0 começa esperando pelo pacote com sequência 0
    seq_esperada = 0

    while True:
        try:
            # Recebe o pacote
            data_recv, addr = sock.recvfrom(1024)
            msg_decoded = data_recv.decode()
            
            # Formato esperado: "seq|checksum|conteudo"
            try:
                parts = msg_decoded.split("|", 3)
                seq_recebida = int(parts[0])
                check_recebido = int(parts[1])
                flag_atraso = int(parts[2])  # 0 para normal, 1 para atraso
                dados = parts[3]
            except ValueError:
                print(f"\n[SERVIDOR] Erro de formatação no pacote: {msg_decoded}")
                continue

            # Calcula o checksum local para verificar integridade
            check_calc = checksum(dados)
            print(f"\n[SERVIDOR] Recebido: Seq={seq_recebida} | Dados='{dados}' | ChecksumRecebido={check_recebido}")

            # 1. Verifica Corrupção
            if check_recebido != check_calc:
                print(f"[SERVIDOR] ❌ PACOTE CORROMPIDO DETECTADO! (Calc: {check_calc} != Recv: {check_recebido})")
                print("[SERVIDOR] Ação: Ignorar pacote (não enviar ACK).")
                # No RDT 3.0, corrupção = silêncio. O cliente dará timeout.
                continue
            # 2. Verifica a Flag de Atraso enviada pelo Cliente 
            if flag_atraso == 1:
                print("[SERVIDOR] ⏳ Flag de atraso detectada! Dormindo 5s...")
                time.sleep(5) # Maior que o timeout do cliente
            # 2. Verifica Número de Sequência
            if seq_recebida == seq_esperada:
                print(f"[SERVIDOR] ✅ Pacote íntegro e na sequência correta ({seq_recebida}).")
                print(f"[SERVIDOR] Processando dados: {dados}")
                
                # Envia ACK correspondente
                pacote_ack = f"ACK|{seq_esperada}"
                sock.sendto(pacote_ack.encode(), addr)
                print(f"[SERVIDOR] Enviado: {pacote_ack}")
                
                # Alterna o estado (espera o próximo: 0->1 ou 1->0)
                seq_esperada = 1 - seq_esperada

            else:
                # Caso receba um pacote duplicado (ex: ACK anterior foi perdido e cliente reenviou)
                # O servidor deve reconfirmar o último recebimento correto para destravar o cliente.
                print(f"[SERVIDOR] ⚠️ Pacote Duplicado (Esperava {seq_esperada}, veio {seq_recebida}).")
                print(f"[SERVIDOR] Ação: Reenviar ACK do pacote recebido ({seq_recebida}).")
                pacote_ack = f"ACK|{seq_recebida}"
                sock.sendto(pacote_ack.encode(), addr)

        except Exception as e:
            print(f"[Erro] {e}")

main()