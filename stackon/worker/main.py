import engine.client


def main():
    client = engine.client.Client("worker-1")
    try:
        client.run()
    except KeyboardInterrupt:
        print(
            "Received exit signal. Stopping main thread, waiting for child threads to finish..."
        )


if __name__ == "__main__":
    main()
