import datetime
import os

from database.connect import connect

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DBNAME = os.getenv("POSTGRES_DBNAME")


def get_rates(rows: int | None = None, daily: bool = False) -> list[dict] | None:
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

        if rows is not None:
            cursor.execute(
                """
            SELECT * FROM (
                SELECT * FROM rates ORDER BY created_at DESC LIMIT %s
            ) AS recent_rates ORDER BY created_at ASC;
            """,
                (rows,),
            )
        elif daily:
            cursor.execute(
                """
                SELECT * FROM rates WHERE created_at BETWEEN (CURRENT_DATE - INTERVAL '1 day')
                AND NOW() ORDER BY created_at ASC;
                """,
            )
        else:
            cursor.execute("""
            SELECT * FROM rates ORDER BY created_at ASC;
            """)
        result_rows = cursor.fetchall()

        if result_rows is None:
            return None

        description = cursor.description
        if description is None:
            return None

        # Get column names
        colnames = [desc[0] for desc in description]
        result: list[dict] = []
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
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()


def get_previous_average() -> float | None:
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
            return None

        cursor = connection.cursor()
        cursor.execute("""
            WITH current_window AS (
                SELECT MIN(created_at) AS start_ts
                FROM rates
                WHERE created_at BETWEEN (CURRENT_DATE - INTERVAL '1 day') AND NOW()
            )
            SELECT AVG(rate)
            FROM rates, current_window
            WHERE current_window.start_ts IS NOT NULL
              AND rates.created_at < current_window.start_ts
              AND rates.created_at >= current_window.start_ts - INTERVAL '1 day';
        """)
        row = cursor.fetchone()

        if row is None or row[0] is None:
            return None

        return float(row[0])
    except Exception as e:
        print(f"Failed to get previous average: {e}")
        return None
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
    import json

    rates = get_rates(daily=True)
    rate = get_rate(1)

    print(json.dumps(rates, indent=4))
    if rates:
        print(len(rates))
    print(json.dumps(rate, indent=4))
