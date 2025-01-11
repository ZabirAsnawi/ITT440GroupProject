#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

void handle_client(int client_socket) {
    char buffer[BUFFER_SIZE];
    int bytes_received;

    while ((bytes_received = recv(client_socket, buffer, BUFFER_SIZE - 1, 0)) > 0) {
        buffer[bytes_received] = '\0'; // Null-terminate the string

        // Check if the input is a valid integer
        char *endptr;
        long int_value = strtol(buffer, &endptr, 10);

        if (*endptr == '\0') { // Valid integer
            char response[BUFFER_SIZE];
            snprintf(response, BUFFER_SIZE, "Integer received is %ld and its value in Hex is %lX", int_value, int_value);
            send(client_socket, response, strlen(response), 0);
        } else {
            const char *error_message = "Invalid input. Please send an integer.";
            send(client_socket, error_message, strlen(error_message), 0);
        }
    }

    close(client_socket);
    printf("Client disconnected.\n");
}

int main() {
    int server_socket, client_socket;
    struct sockaddr_in server_address, client_address;
    socklen_t client_address_length = sizeof(client_address);

    int port;
    do {
        printf("Enter port number (1-65535): ");
        scanf("%d", &port);

        if (port < 1 || port > 65535) {
            printf("Invalid port number. Please enter a value between 1 and 65535.\n");
        } else if (port < 1024) {
            printf("This port (%d) cannot be accessed because it is reserved for well-known services.\n", port);
        } else if (port >= 49152) {
            printf("This port (%d) is in the dynamic/private range, typically used for ephemeral connections.\n", port);
        } else {
            break; // Valid port within the general range
        }
    } while (1);

    // Create a socket
    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Define the server address
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(port);
    server_address.sin_addr.s_addr = INADDR_ANY;

    // Bind the socket to the specified port
    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) == -1) {
        perror("Binding failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    // Listen for incoming connections
    if (listen(server_socket, 5) == -1) {
        perror("Listening failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("Server is listening on port %d...\n", port);

    // Accept and handle incoming connections
    while ((client_socket = accept(server_socket, (struct sockaddr *)&client_address, &client_address_length)) != -1) {
        printf("Connection established with a client.\n");
        handle_client(client_socket);
    }

    if (client_socket == -1) {
        perror("Accept failed");
    }

    close(server_socket);
    return 0;
}
