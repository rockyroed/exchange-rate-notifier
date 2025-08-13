import os
import datetime

from database.connect import connect

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")


def get_rates(rows=24):
    # Connect to the database
    connection = None
    cursor = None

    try:
        connection = connect(
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host=POSTGRES_HOST,
            port=POSTGRES_PORT,
            dbname=POSTGRES_DBNAME,
        )

        if connection is None:
            return

        cursor = connection.cursor()
        cursor.execute("SELECT * FROM rates ORDER BY created_at ASC LIMIT %s;", (rows,))
        result_rows = cursor.fetchall()

        if result_rows is None:
            return None

        # Get column names
        colnames = [desc[0] for desc in cursor.description]
        result = []
        for row in result_rows:
            row_dict = dict(zip(colnames, row))
            if "created_at" in row_dict and row_dict["created_at"] is not None:
                # Convert to PHT (UTC+8)
                if row_dict["created_at"].tzinfo is None:
                    # Assume naive datetime is UTC
                    dt_utc = row_dict["created_at"].replace(tzinfo=datetime.timezone.utc)
                else:
                    dt_utc = row_dict["created_at"].astimezone(datetime.timezone.utc)
                dt_pht = dt_utc.astimezone(datetime.timezone(datetime.timedelta(hours=8)))
                row_dict["created_at"] = dt_pht.strftime("%m/%d, %I:%M %p")
            result.append(row_dict)
        return result
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
            dbname=POSTGRES_DBNAME,
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
            dbname=POSTGRES_DBNAME,
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
