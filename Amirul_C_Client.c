#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

int main() {
    char server_ip[50];
    int server_port;
    char input[BUFFER_SIZE];
    char response[BUFFER_SIZE];

    printf("Enter server IP address: ");
    scanf("%s", server_ip);

    printf("Enter server port number: ");
    scanf("%d", &server_port);

    // Create a socket
    int client_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (client_socket < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // Define server address
    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(server_port);

    if (inet_pton(AF_INET, server_ip, &server_address.sin_addr) <= 0) {
        perror("Invalid address/Address not supported");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    // Connect to the server
    if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
        perror("Connection to the server failed");
        close(client_socket);
        exit(EXIT_FAILURE);
    }

    printf("Connected to the server at %s:%d\n", server_ip, server_port);

    while (1) {
        printf("Enter an integer (or type 'exit' to terminate): ");
        scanf("%s", input);

        if (strcmp(input, "exit") == 0) {
            printf("Terminating connection...\n");
            break;
        }

        // Send the input to the server
        send(client_socket, input, strlen(input), 0);

        // Receive the server's response
        memset(response, 0, BUFFER_SIZE);
        int bytes_received = recv(client_socket, response, BUFFER_SIZE - 1, 0);
        if (bytes_received <= 0) {
            printf("Connection closed by server.\n");
            break;
        }

        response[bytes_received] = '\0';
        printf("Server response: %s\n", response);
    }

    // Close the socket
    close(client_socket);
    return 0;
}
