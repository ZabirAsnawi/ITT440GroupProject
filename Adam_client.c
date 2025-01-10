#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define BUFFER_SIZE 1024

int main() {
    int sock = 0;
    struct sockaddr_in serv_addr;
    char buffer[BUFFER_SIZE] = {0};
    char input[BUFFER_SIZE] = {0};
    char server_ip[16];
    int port;

    // Get server IP and port from user
    printf("Enter server IP address: ");
    scanf("%s", server_ip);
    printf("Enter server port: ");
    scanf("%d", &port);

    // Create socket
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("Socket creation error\n");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(port);

    // Convert IP address from string to binary form
    if (inet_pton(AF_INET, server_ip, &serv_addr.sin_addr) <= 0) {
        printf("Invalid address\n");
        return -1;
    }

    // Connect to server
    if (connect(sock, (struct sockaddr *)&serv_addr, sizeof(serv_addr)) < 0) {
        printf("Connection Failed\n");
        return -1;
    }

    printf("Connected to server\n");

    while (1) {
        // Get integer input from user
        printf("\nEnter an integer (or 'q' to quit): ");
        scanf("%s", input);

        // Check if user wants to quit
        if (input[0] == 'q' || input[0] == 'Q') {
            break;
        }

        // Send input to server
        send(sock, input, strlen(input), 0);

        // Receive response from server
        memset(buffer, 0, BUFFER_SIZE);
        read(sock, buffer, BUFFER_SIZE);
        printf("Server response: %s\n", buffer);
    }

    // Close socket
    close(sock);
    return 0;
}