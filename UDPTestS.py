import socket
import struct
import Speed
import Steering
import random
import time

TESTING = True

# IP addy sender and receiver
HOST = '127.0.0.1'  #localhost
PORT = 65432 #listner port

# Create UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Trun data into byte stream
def pack_data(data):
  """
  Input: dict with data
  Return: byte stream
  """
  #empty byte stream
  byte_stream = b''

  for key, value in data.items():
    # pack according to type
    if value['type'] == 'Uint8':
      byte_stream += struct.pack('!B', value['value'])
    elif value['type'] == 'Uint16':
      byte_stream += struct.pack('!H', value['value'])
    else:
      raise ValueError(f"Unsupported data type: {value['type']}")

  return byte_stream
  

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

# Define the data format
data_format = {
  "Target_Velocity*10": {"type": "Uint16", "value": 0},
  "Target_SAngle+90": {"type": "Uint16", "value": 0},
  "Send_Mode": {"type": "Uint8", "value": 0},
  "Orin_Stop_Signal": {"type": "Uint8", "value": 0},
  "Heartbeat_Orin": {"type": "Uint16", "value": 0},
}

if TESTING:
   pass
else:
  Output = Speed.speed()   
  Steering_angle = Steering.Steering(0) 
  Target_Velocity = Output[0]
  Send_Mode = Output[1] 
  Orin_Stop_Signal = Output[2] 
  Heartbeat_Orin = 1 ##########FIX###########

def get_test_data(): 
        data_test = {
        "Target_Velocity*10": {"type": "Uint16", "value": Target_Velocity},
        "Target_SAngle+90": {"type": "Uint16", "value": Steering_angle},
        "Send_Mode": {"type": "Uint8", "value": Send_Mode},
        "Orin_Stop_Signal": {"type": "Uint8", "value": Orin_Stop_Signal},
        "Heartbeat_Orin": {"type": "Uint16", "value": Heartbeat_Orin},
        }
        return data_test


def get_test_data_temp():
    return {
        "T_V": {"type": "Uint16", "value": random.randint(0, 250)},
        "T_SA": {"type": "Uint16", "value": random.randint(0, 180)},
        "S_M": {"type": "Uint8", "value": random.randint(0, 1)},
        "S_S": {"type": "Uint8", "value": random.randint(0, 1)},
        "Heartbeat_Orin": {"type": "Uint16", "value": 45},
    }
        

#send data
while True:
    data_to_send = get_test_data_temp()
    data_bytes = pack_data(data_to_send)

    # Send data
    sock.sendto(data_bytes, (HOST, PORT))

    # Receive data
    # try:
    #     received_data, addr = sock.recvfrom(1024)
    #     received_data_dict = unpack_data(received_data)
    #     print(f"Received data: {received_data_dict}")
    # except socket.timeout:
    #     print("Timeout waiting for data")

    # delay
    time.sleep(1)    

