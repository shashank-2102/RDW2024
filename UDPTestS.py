import socket
import struct
import Speed
import Steering

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

Output = Speed.speed()
Steering_angle = Steering.Steering()
Target_Velocity = Output[0] * 10
Send_Mode = Output[1]
Orin_Stop_Signal = Output[2]

def get_test_data(): 
        data_test = {
        "Target_Velocity*10": {"type": "Uint16", "value": Target_Velocity},
        "Target_SAngle+90": {"type": "Uint16", "value": 69},
        "Send_Mode": {"type": "Uint8", "value": Send_Mode},
        "Orin_Stop_Signal": {"type": "Uint8", "value": Orin_Stop_Signal},
        "Heartbeat_Orin": {"type": "Uint16", "value": Steering_angle},
        }
        return data_test
        

#send data
while True:

    data_to_send = get_test_data()
    #User input
    #   for key, value in data_format.items():
    #     if value is not None:
    #       try:
    #         data_format[key]["value"] = int(input(f"{key}: "))
    #       except ValueError:
    #         print(f"Invalid input for {key}. Please enter an integer.")
            

    # use pack func
    # data_bytes = pack_data(data_format)
    data_bytes = pack_data(data_to_send)

    # send data
    sock.sendto(data_bytes, (HOST, PORT))

    # receive data
    try:
        received_data, addr = sock.recvfrom(1024)
    except socket.timeout:
        print("Timeout waiting for data")
        continue

    # unpack received data
    received_data_dict = unpack_data(received_data)


    

