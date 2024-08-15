from yarcon import Connection


def main():
    with Connection(addr="127.0.0.1", debug=True) as conn:
        logged = conn.login("test123")

        if logged:
            res = conn.command("say hello from yarcon")
            print(f"response: {res}")


if __name__ == '__main__':
    main()
