import socket

def main():
    """Main client function."""
    # Specify the server IP address and port number
    server_ip = "192.168.80.128"
    server_port = 65432

    # Create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server
        client.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        while True:
            try:
                # Get user input
                user_input = input("Enter an integer (or type 'exit' to quit): ").strip()

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
        print("Failed to connect to the server.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()
        print("Disconnected from the server.")

if __name__ == "__main__":
    main()
