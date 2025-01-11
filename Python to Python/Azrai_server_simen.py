import socket
import threading

def handle_client(client_socket):
    """Handles communication with the connected client."""
    try:
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            if not data:
                break

            # Convert the received number to float
            try:
                received_number = float(data.decode('utf-8').strip())
                
                # Check if the number is an integer
                if received_number.is_integer():
                    # If the number is an integer, format it as an int
                    response = f"Number received is {int(received_number)} and its value in Hex is {hex(int(received_number))[2:].upper()}"
                else:
                    # If the number is a float, include the fractional part
                    int_part = int(received_number)
                    frac_part = received_number - int_part
                    
                    # Convert integer part to hex
                    int_hex = hex(int_part)[2:].upper()
                    
                    # Convert fractional part to hex (limit to 4 digits for simplicity)
                    frac_hex = ""
                    for _ in range(4):  # Limit to 4 digits of precision
                        frac_part *= 16
                        hex_digit = int(frac_part)
                        frac_hex += hex(hex_digit)[2:].upper()
                        frac_part -= hex_digit
                        if frac_part == 0:
                            break
                    
                    hex_value = f"{int_hex}.{frac_hex}"
                    response = f"Number received is {received_number} and its value in Hex is {hex_value}"

            except ValueError:
                response = "Invalid input. Please send a valid number."

            # Send the response back to the client
            client_socket.send(response.encode('utf-8'))
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()
        print("Client disconnected.")


def main():
    """Main server function."""
    # Get the port number from user input
    try:
        port = int(input("Enter the port number the server should listen on (e.g., 65432): ").strip())
    except ValueError:
        print("Invalid port number. Using default port 65432.")
        port = 65432

    # Specify the IP address
    ip_address = "192.168.80.128"  # Listen on all available interfaces

    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified IP address and port
    try:
        server.bind((ip_address, port))
    except OSError as e:
        print(f"Failed to bind to {ip_address}:{port}. Error: {e}")
        return

    # Start listening for incoming connections
    server.listen(5)
    print(f"Server listening on {ip_address}:{port}...")

    try:
        while True:
            # Accept a new client connection
            client_socket, addr = server.accept()
            print(f"Connection established with {addr}")

            # Handle the client in a separate thread
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
    finally:
        server.close()

if __name__ == "__main__":
    main()
