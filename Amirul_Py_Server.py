import socket
import threading

def handle_client(client_socket, client_address):
    print(f"Connection established with {client_address}")

    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Process the received data (convert integer to hex)
            if data.isdigit():
                integer_value = int(data)
                hex_value = hex(integer_value)[2:].upper()
                response = f"Integer received is {integer_value} and its value in Hex is {hex_value}"
            else:
                response = "Invalid input. Please send an integer."

            # Send the response back to the client
            client_socket.sendall(response.encode())

    except Exception as e:
        print(f"Error handling client {client_address}: {e}")

    finally:
        print(f"Connection with {client_address} closed.")
        client_socket.close()

def main():
    print("TCP Server")

    # Capture user input for server port
    server_port = int(input("Enter port number for the server to listen on: "))

    # Create a socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("0.0.0.0", server_port))
        server_socket.listen(5)

        print(f"Server is listening on port {server_port}...")

        while True:
            try:
                # Accept an incoming connection
                client_socket, client_address = server_socket.accept()

                # Handle the client in a separate thread
                client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
                client_thread.start()

            except KeyboardInterrupt:
                print("Server is shutting down...")
                break

if __name__ == "__main__":
    main()
