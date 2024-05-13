import multiprocessing

################### MOVED TO CENTRAL LOGIC ###################

def receive_data(queue):
    while True:
        data = queue.get()  # Get data from the queue
        print("Received data:", data)  # Print the received data
        process_data(data)
        save_data(data)


def process_data(data):
    # Add your data processing logic here
    print("Processing received data:", data)

def save_data(data):
    with open("output1.txt", "a") as file:
        file.write(str(data) + "\n")


if __name__ == "__main__":
    # Create a multiprocessing Queue
    queue = multiprocessing.Queue()

    # Start the receiver process
    receiver_process = multiprocessing.Process(target=receive_data, args=(queue,))
    receiver_process.start()

    # Keep the receiver process running
    receiver_process.join()
