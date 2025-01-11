import socket

def main():
    # Error handling IP and Port invalid input
    # Get the server IP address from user input
    while True:
        server_ip = input("Enter the server IP address (e.g., 192.168.80.128): ").strip()
        if server_ip.count('.') == 3 and all(part.isdigit() and 0 <= int(part) <= 255 for part in server_ip.split('.') if part):
            break
        print("Invalid IP address. Please enter a valid IPv4 address (e.g., 192.168.80.128).")

    # Get the server port number from user input
    while True:
        try:
            server_port = int(input("Enter the server port number (e.g., 65432): ").strip())
            if 1 <= server_port <= 65535:
                break
            else:
                print("Port number must be between 1 and 65535.")
        except ValueError:
            print("Invalid port number. Please enter a number between 1 and 65535.")

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        while True:
            try:
                # Get user input
                user_input = input("Enter a number (or type 'exit' to quit): ").strip()

                if user_input.lower() == 'exit':
                    print("Closing connection...")
                    break

                # Send the input to the server
                client.send(user_input.encode('utf-8'))

                # Receive and display the server's response
                response = client.recv(1024).decode('utf-8')
                print(f"Server response: {response}")

            except KeyboardInterrupt:
                print("\nConnection closed by user (Ctrl+C).")
                break

    except ConnectionError:
        print("Failed to connect to the server. Please check the IP and port.")
    finally:
        client.close()
        print("Disconnected from the server.")

if __name__ == "__main__":
    main()
