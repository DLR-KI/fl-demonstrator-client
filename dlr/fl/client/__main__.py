from . import Settings, import_string


__all__ = ["main"]


def default_main():
    """
    Default main function for the client server.

    This function will not be called if the `MAIN_MODULE` attribute is set inside the Settings.
    """
    from http.server import HTTPServer
    from .client_server import ClientServerHandler

    server = HTTPServer((Settings.SERVER_HOST, Settings.SERVER_PORT), ClientServerHandler)
    print("Starting server, use <Ctrl + C> to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
        server.shutdown()


def main():
    """
    Client server main entry point.

    Starts the custom main function if the `MAIN_MODULE` attribute is set inside the Settings.
    Otherwise the default main function is started.
    """
    if hasattr(Settings, "MAIN_MODULE"):
        fn_main = import_string(Settings.MAIN_MODULE)
        fn_main()
    else:
        default_main()


if __name__ == "__main__":
    main()
