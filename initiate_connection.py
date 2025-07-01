import socket

HOST = 'modbus_scolaire.wargame.rocks'
PORT = 1502

packet = (
  b'\x00\x01'  # Transaction ID
  b'\x00\x00'  # Protocol ID
  b'\x00\x0A'  # Length (10 bytes after this)
  b'\x01'      # Unit ID
  b'\x01'      # Function Code: Read Coils
)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
  s.connect((HOST, PORT))
  s.sendall(packet)
  data = s.recv(1024)
  print("Received:", data)
