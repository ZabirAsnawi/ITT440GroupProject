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
                int_part = int(received_number)
                frac_part = received_number - int_part

                # Convert integer part to hex
                int_hex = hex(int_part)[2:].upper() 
                #test
                # If the fractional part is 0, just send the integer part
                if frac_part == 0:
                    hex_value = int_hex
                    response = f"Number received is {received_number} and its value in Hex is {hex_value}"
                else:
                    # Convert fractional part to hex (limit to 4 digits for simplicity)
                    frac_hex = ""
                    for _ in range(4):  # Limit to 4 digits of precision
                        frac_part *= 16
                        hex_digit = int(frac_part)
                        frac_hex += hex(hex_digit)[2:].upper()
                        frac_part -= hex_digit
                        if frac_part == 0:
                            break
                    
                    # Combine the integer and fractional part
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
    # Specify the IP address and port number
    ip_address = "192.168.80.128"
    port = 65432

    # Create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the specified IP address and port
    server.bind((ip_address, port))

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