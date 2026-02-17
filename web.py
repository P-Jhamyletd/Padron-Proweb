from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse





class WebRequestHandler(BaseHTTPRequestHandler):

    def url(self):
        return urlparse(self.path)

    def query_data(self):
        return dict(parse_qsl(self.url().query))

    def do_GET(self):

        ruta = self.url().path
        query = self.query_data()

        #PARA OBSERVAR EN LA TERMINAL 
        print("----- REQUEST -----")
        print("Host:", self.headers.get("Host"))
        print("User-Agent:", self.headers.get("User-Agent"))
        print("Ruta:", ruta)

        #CONTENIDO 
        contenido = {
            "/": self.home_page(),
            "/proyecto/web-uno": "<h1>Proyecto: web-uno</h1>",
            "/proyecto/web-dos": "<h1>Proyecto: web-dos</h1>",
            "/proyecto/web-tres": "<h1>Proyecto: web-tres</h1>",
        }

        # HTML DINAMICO
        if ruta.startswith("/proyecto/") and "autor" in query:
            proyecto = ruta.split("/")[-1]
            respuesta = f"<h1>Proyecto: {proyecto} Autor: {query['autor']}</h1>"
            self.responder(200, respuesta)
            return

        #SITIO CON DICCIONARIO
        if ruta in contenido:
            self.responder(200, contenido[ruta])
        else:
            self.responder(404, "<h1>Error 404 - Página no encontrada</h1>")

    # ----- MÉTODO PARA RESPONDER -----
    def responder(self, codigo, contenido_html):
        self.send_response(codigo)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

            #PARA VER TERMINAL 
        print("----- RESPONSE -----")
        print("Content-Type: text/html")
        print("Server:", self.version_string())
        print("Date:", self.date_time_string())

        self.wfile.write(contenido_html.encode("utf-8"))

    # ----- HOME PAGE -----
    def home_page(self):
        try:
            with open("home.html", "r", encoding="utf-8") as f:
                return f.read()
        except:
            return "<h1>No se encontró home.html</h1>"


if __name__ == "__main__":
    print("Servidor escuchando en puerto 8000")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
