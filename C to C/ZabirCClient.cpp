#include <iostream>
#include <cstring>
#include <string>
#include <unistd.h>
#include <arpa/inet.h>

using namespace std;

int main() {
    int clientSocket;
    string serverIP;
    int portNumber;

    cout << "Enter server IP address: ";
    cin >> serverIP;
    cout << "Enter server port number: ";
    cin >> portNumber;

    // Create socket
    clientSocket = socket(AF_INET, SOCK_STREAM, 0);
    if (clientSocket < 0) {
        cerr << "Error creating socket." << endl;
        return 1;
    }

    // Set up server address
    sockaddr_in serverAddr{};
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(portNumber);
    inet_pton(AF_INET, serverIP.c_str(), &serverAddr.sin_addr);

    // Connect to server
    if (connect(clientSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) < 0) {
        cerr << "Connection failed." << endl;
        return 1;
    }

    cout << "Connected to server." << endl;

    while (true) {
        // Get user input
        string input;
        cout << "Enter an integer (or 'exit' to quit): ";
        cin >> input;

        // Exit if user types 'exit'
        if (input == "exit") {
            break;
        }

        // Send input to server
        send(clientSocket, input.c_str(), input.length(), 0);

        // Receive response from server
        char buffer[1024];
        memset(buffer, 0, sizeof(buffer));
        int bytesReceived = recv(clientSocket, buffer, sizeof(buffer), 0);
        if (bytesReceived <= 0) {
            cout << "Server disconnected." << endl;
            break;
        }

        // Print server response
        cout << "Server response: " << buffer << endl;
    }

    close(clientSocket);
    return 0;
}
