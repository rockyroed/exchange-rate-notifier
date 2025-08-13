import psycopg2


def connect(user, password, host, port, dbname):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=host,
            port=port,
            dbname=dbname
        )

        return connection
    except Exception as e:
        print(f"Failed to connect: {e}")
        return None
