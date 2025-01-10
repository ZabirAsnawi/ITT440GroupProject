import socket
import threading
import sys

def handle_client(client_socket, addr):
    print(f"Connected to client: {addr}")
    while True:
        try:
            # Receive data from client
            data = client_socket.recv(1024).decode().strip()
            if not data:
                break
            
            # Convert received number to integer and then to hex
            number = int(data)
            hex_value = hex(number)[2:].upper()  # Remove '0x' prefix and convert to uppercase
            
            # Format response
            response = f"Integer received is {number} and its value in Hex is {hex_value}"
            
            # Send response back to client
            client_socket.send(response.encode())
            
        except Exception as e:
            print(f"Error handling client: {e}")
            break
    
    client_socket.close()
    print(f"Connection closed with {addr}")

def main():
    # Get port number from user
    port = int(input("Enter server port number: "))
    
    # Create server socket
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    
    print(f"Server listening on port {port}")
    
    try:
        while True:
            # Accept client connection
            client_socket, addr = server.accept()
            
            # Create new thread for each client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    finally:
        server.close()

if __name__ == "__main__":
    main()
