## 🚀 Como Rodar o Projeto

Pré-requisitos: Ter o **Python 3** instalado.

### Passo 1: Executar o Servidor
Abra o primeiro terminal na pasta do projeto e execute:
```bash
python servidor.py

```

*O servidor iniciará na porta 5000 e ficará aguardando pacotes.*

### Passo 2: Executar o Cliente

Abra um segundo terminal e execute:

```bash
python cliente.py

```

*O cliente iniciará e solicitará a mensagem para envio.*

---

## 🧪 Guia de Testes (Passo a Passo)

O sistema possui um menu interativo para simular o comportamento de um canal instável. Abaixo estão os cenários que devem ser testados:

### Cenário 1: Entrega Normal (Sucesso)

1. No Cliente, digite a mensagem: `Ola Mundo`
2. No menu, escolha: **`1 - Entrega normal`**
3. **Resultado Esperado:**
* O Cliente recebe o ACK imediatamente.
* O Servidor imprime a mensagem recebida corretamente.
* O fluxo segue para a próxima mensagem.



### Cenário 2: Simulação de Corrupção (Erro de Checksum)

1. No Cliente, digite a mensagem: `Teste Erro`
2. No menu, escolha: **`2 - Corromper dados`**
3. **O que acontece:** O código altera o checksum propositalmente antes de enviar.
4. **Resultado Esperado:**
* **Servidor:** Detecta o erro (`Checksum Inválido`) e ignora o pacote (não envia ACK).
* **Cliente:** O temporizador estoura. Aparece a mensagem `⏰ TIMEOUT! Retransmitindo...`.
* O pacote é reenviado automaticamente.



### Cenário 3: Simulação de Atraso (Timeout Prematuro)

1. No Cliente, digite a mensagem: `Teste Delay`
2. No menu, escolha: **`3 - Inserir atraso`**
3. **O que acontece:** O sistema "dorme" por alguns segundos antes de completar o envio/resposta.
4. **Resultado Esperado:**
* O atraso faz o cliente esperar o tempo determinado para so assim enviar para o servidor.

