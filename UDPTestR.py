import socket
import struct

# IP addy sender and receiver
HOST = '127.0.0.1'  #localhost
PORT = 65432 #listner port

# data format (same as the sender)
data_format = {
  "T_V": {"type": "Uint16", "value": 0},
  "T_SA": {"type": "Uint16", "value": 0},
  "S_M": {"type": "Uint8", "value": 0},
  "S_S": {"type": "Uint8", "value": 0},
  "Heartbeat_Orin": {"type": "Uint16", "value": 0},
}

# Unpack data
def unpack_data(data):
  """
  Input: data: byte stream
  Returns:dict with unpacked data
  """
  unpacked_data = {}

  # Get the offset into the byte stream +++++++++++++
  offset = 0


  for key, value in data_format.items():
    # check types
    if value['type'] == 'Uint8':
      unpacked_data[key] = struct.unpack_from('!B', data, offset)[0]
      offset += 1
    elif value['type'] == 'Uint16':
      unpacked_data[key] = struct.unpack_from('!H', data, offset)[0]
      offset += 2
    else:
      raise ValueError(f"Unsupported data type: {value['type']}")

  return unpacked_data

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
sock.bind((HOST, PORT))

print(f"UDP receiver listening on {HOST}:{PORT}")

while True:
  # receive data from sender
  try:
    data, addr = sock.recvfrom(1024)
    print(f"Received data from {addr}")

    # unpack
    unpacked_data = unpack_data(data)

    # TESTING: Print
    print("Received data:")
    for key, value in unpacked_data.items():
      print(f"{key}: {value}")

  except KeyboardInterrupt:
    print("Exiting...")
    break

# socket close
sock.close()
