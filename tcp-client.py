import socket
import threading

def receive_data(sock):
    buffer = ''
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("\nConnection closed by the server.")
                break
            buffer += data.decode('utf-8', errors='ignore')
            while '\r\n' in buffer:
                message, buffer = buffer.split('\r\n', 1)
                print("\nReceived:", message)
        except Exception as e:
            print(f"\nAn error occurred in receiving data: {e}")
            break

def main():
    HOST = '193.1.3.1'  # Replace with the IP address of your RUT956 device
    PORT = 2506         # Replace with the port number configured for serial over IP

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print(f"Connected to {HOST}:{PORT}")

            # Start a thread to receive data
            receiver_thread = threading.Thread(target=receive_data, args=(s,), daemon=True)
            receiver_thread.start()

            # Main thread for sending data
            while True:
                try:
                    message = input()  # Read user input
                    if message.lower() in ('exit', 'quit'):
                        print("Exiting...")
                        break
                    # Append CRLF to the message
                    message_with_crlf = message + '\r\n'
                    s.sendall(message_with_crlf.encode('utf-8'))
                except KeyboardInterrupt:
                    print("\nExiting...")
                    break
                except Exception as e:
                    print(f"\nAn error occurred in sending data: {e}")
                    break

    except ConnectionRefusedError:
        print(f"Could not connect to {HOST}:{PORT}. Please check the IP and port.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
