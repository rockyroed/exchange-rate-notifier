import os
from connect import connect

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")


def get_rates():
    # Connect to the database
    connection = None
    cursor = None

    try:
        connection = connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DBNAME
        )

        if connection is None:
            return

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rates;")
        rows = cursor.fetchall()

        if rows is None:
            return None

        return rows
    except Exception as e:
        print(f"Failed to get rates: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def get_rate(id):
    # Connect to the database
    connection = None
    cursor = None

    # Connect to the database
    try:
        connection = connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DBNAME
        )

        if connection is None:
            return

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rates where ID = %s;", (id,))
        row = cursor.fetchone()

        if row is None:
            return None

        # Close the cursor and connection
        cursor.close()
        connection.close()

        return row
    except Exception as e:
        print(f"Failed to get rates: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def post_rate(rate):
    """Insert a new rate (float) into the rates table."""
    connection = None
    cursor = None
    try:
        connection = connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DBNAME
        )

        if connection is None:
            return False

        cursor = connection.cursor()
        cursor.execute("INSERT INTO rates (rate) VALUES (%s);", (rate,))
        connection.commit()
        return True
    except Exception as e:
        print(f"Failed to insert rate: {e}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


if __name__ == "__main__":
    rates = get_rates()
    rate = get_rate(1)

    print(rates)
    print(rate)
