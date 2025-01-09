#include <iostream>
#include <cstring>
#include <unistd.h>
#include <arpa/inet.h>
#include <thread>

using namespace std;

// Function to handle client connection
void handleClient(int clientSocket) {
    char buffer[1024];
    int number;

    while (true) {
        // Receive integer from client
        memset(buffer, 0, sizeof(buffer));
        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesReceived <= 0) {
            cout << "Client disconnected." << endl;
            break;
        }

        // Convert received number to integer
        number = atoi(buffer);

        // Convert integer to hex
        char hexBuffer[32];
        sprintf(hexBuffer, "Integer received is %d and its value in Hex is %X", number, number);

        // Send hex string back to client
        send(clientSocket, hexBuffer, strlen(hexBuffer), 0);
    }

    close(clientSocket);
}

int main() {
    int serverSocket;
    int portNumber;

    cout << "Enter port number to listen on: ";
    cin >> portNumber;

    // Create socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSocket < 0) {
        cerr << "Error creating socket." << endl;
        return 1;
    }

    // Bind socket to the port
    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(portNumber);
    serverAddr.sin_addr.s_addr = INADDR_ANY;

    if (bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        cerr << "Error binding socket to port." << endl;
        return 1;
    }

    // Listen for incoming connections
    listen(serverSocket, 5);
    cout << "Server listening on port " << portNumber << "..." << endl;

    while (true) {
        // Accept client connection
        sockaddr_in clientAddr{};
        socklen_t clientLen = sizeof(clientAddr);
        int clientSocket = accept(serverSocket, (sockaddr*)&clientAddr, &clientLen);
        if (clientSocket < 0) {
            cerr << "Error accepting client connection." << endl;
            continue;
        }

        cout << "Client connected." << endl;

        // Handle client in a separate thread
        thread clientThread(handleClient, clientSocket);
        clientThread.detach();
    }

    close(serverSocket);
    return 0;
}
