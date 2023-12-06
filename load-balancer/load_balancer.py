import socket
import threading
import requests
import time

# List of backend servers
backend_servers = ['http://localhost:8080', 'http://localhost:8081']
current_server = 0

def handle_client(client_socket):
    global current_server
    request = client_socket.recv(1024).decode('utf-8')
    print(f"Received request:\n{request}")

    # Round-robin selection of backend server
    backend_server = backend_servers[current_server]
    current_server = (current_server + 1) % len(backend_servers)

    # Forward request to backend server
    try:
        response = requests.get(backend_server)
        client_socket.send(f"HTTP/1.1 200 OK\n\n{response.text}".encode('utf-8'))
    except requests.RequestException as e:
        print(f"Error forwarding request to {backend_server}: {e}")
        client_socket.send(b"HTTP/1.1 502 Bad Gateway\n\nBackend server error")
    finally:
        client_socket.close()

def health_check():
    global backend_servers
    while True:
        for server in backend_servers.copy():
            try:
                response = requests.get(server + '/health-check')  # Modify this if needed
                if response.status_code != 200:
                    print(f"Server {server} failed health check with status code {response.status_code}")
                    backend_servers.remove(server)
            except requests.RequestException as e:
                print(f"Server {server} failed health check with error: {e}")
                backend_servers.remove(server)
        time.sleep(10)  # Health check interval


def main():
    # Start health check in a separate thread
    health_thread = threading.Thread(target=health_check)
    health_thread.daemon = True
    health_thread.start()

    # Load Balancer Socket Setup
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lb_socket.bind(('localhost', 80))
    lb_socket.listen(5)
    print("Load Balancer running on port 80")

    # Accepting and handling client connections
    try:
        while True:
            client, addr = lb_socket.accept()
            print(f"Received connection from {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client,))
            client_handler.start()
    except KeyboardInterrupt:
        print("Shutting down Load Balancer")
    finally:
        lb_socket.close()

if __name__ == '__main__':
    main()
