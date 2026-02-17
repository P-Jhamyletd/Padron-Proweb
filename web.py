from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qsl


class WebRequestHandler(BaseHTTPRequestHandler):

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        url = self.url()
        return dict(parse_qsl(url.query))

    def do_GET(self):

        url = urlparse(self.path)
        query = dict(parse_qsl(url.query))
        ruta = url.path

        # HOME PAGE
        if ruta == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

            with open("home.html", "r", encoding="utf-8") as f:
                contenido = f.read()

            self.wfile.write(contenido.encode("utf-8"))
            return

        # HTML dinámico
        if ruta.startswith("/proyecto/"):
            proyecto = ruta.split("/")[-1]
            autor = query.get("autor", "desconocido")

            respuesta = f"""
            <html>
            <head><title>Proyecto</title></head>
            <body>
            <h1>Proyecto: {proyecto}</h1>
            <h2>Autor: {autor}</h2>
            </body>
            </html>
            """

            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(respuesta.encode("utf-8"))
            return

        # ERROR 404
        self.send_response(404)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(b"<h1>Error 404 - Pagina no encontrada</h1>")


def run():
    server_address = ("", 8000)
    httpd = HTTPServer(server_address, WebRequestHandler)
    print("Servidor corriendo en http://localhost:8000")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
