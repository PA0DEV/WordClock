


class WebServer:
    def __init__(self) -> None:
        try:
            import usocket as socket
        except:
            import socket

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(('', 80))
        self.s.listen(5)

    def indexHTML(self):
        pass

    def listenClient(self):
        conn, addr = self.s.accept()
        print("[WEB] got connection from %s" %str(addr))
        request = conn.recv(1024)
        request = str(request)
        print("[WEB] Request: %s" %request)
