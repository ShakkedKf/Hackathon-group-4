import socket
import threading
import os
import time

def kill_port(port):
    os.system(f"lsof -ti :{port} | xargs kill -9 2>/dev/null")
    time.sleep(1.0)  # wait for OS to release the port

HOST = "127.0.0.1"
PORT = 8200

def server_thread(stop_event):
    
    kill_port(PORT)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(1)
    server.settimeout(1.0)

    print(f"Server listening on {HOST}:{PORT}")

    conn = None
    try:
        while not stop_event.is_set():
            if conn is None:
                try:
                    conn, addr = server.accept()
                    print("Client connected:", addr)
                    conn.settimeout(1.0)
                except socket.timeout:
                    continue

            # receive many messages from same client
            try:
                data = conn.recv(1024)
                if not data:
                    print("Client disconnected")
                    conn.close()
                    conn = None
                    continue

                msg = data.decode(errors="replace")
                print("Received:", msg)
                if msg.lower() == "name":
                    conn.sendall(b"Name: Server")
                else:
                    conn.sendall(f"ACK: {msg}".encode())

            except socket.timeout:
                continue

    finally:
        if conn:
            conn.close()
        server.close()
        print("Server closed")

if __name__ == "__main__":
    stop = threading.Event()
    t = threading.Thread(target=server_thread, args=(stop,))
    t.start()

    while True:
        cmd = input("Server cmd (q=quit): ").strip().lower()
        if cmd == "q":
            stop.set()
            break

    t.join()
