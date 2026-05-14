import socket, threading
import time

HOST = "127.0.0.1"
PORT = 8200

def recv_loop(sock, stop_event):
    sock.settimeout(1.0)
    while not stop_event.is_set():
        try:
            data = sock.recv(1024)
            if not data:
                print("\n[server closed connection]")
                stop_event.set()
                break
            print("\n[server]:", data.decode(errors="replace"))
        except socket.timeout:
            pass
        except OSError:
            stop_event.set()
            break

def main():

    time.sleep(1)  # wait for server to start
    stop_event = threading.Event()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    t = threading.Thread(target=recv_loop, args=(sock, stop_event), daemon=True)
    t.start()

    try:
        while not stop_event.is_set():
            msg = input("client> ")
            if msg.lower() in ("q", "quit", "exit"):
                stop_event.set()
                break
            sock.sendall(msg.encode())
    except KeyboardInterrupt:
        stop_event.set()

    try:
        sock.shutdown(socket.SHUT_RDWR)
    except OSError:
        pass
    sock.close()
    print("Client closed")

if __name__ == "__main__":
    main()
