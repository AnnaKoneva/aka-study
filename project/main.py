import sys
import serv


if __name__ == "__main__":
    server = serv.HTTPServer(port=int(*sys.argv[1:]))
    server.register(lambda request: request.url == "/html/", lambda request: request.reply('<H1>"Hello world!!!!"</H1>', content_type = 'text/html')) 
    server.register(lambda r: r.url == '/crash/me/', lambda r: no_you)
    server.listen()
