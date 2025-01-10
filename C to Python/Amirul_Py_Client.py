import socket

def main():
    print("Python TCP Client")

    server_ip = input("Enter server IP address: ")
    server_port = int(input("Enter server port number: "))

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            client_socket.connect((server_ip, server_port))
            print(f"Connected to server at {server_ip}:{server_port}")

            while True:
                user_input = input("Enter an integer (or type 'exit' to terminate): ")

                if user_input.lower() == 'exit':
                    print("Terminating connection...")
                    break

                client_socket.sendall(user_input.encode())
                response = client_socket.recv(1024).decode()
                print(f"Server response: {response}")

        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
