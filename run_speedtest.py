from sqlite3 import connect
from subprocess import check_output
# from speedtest import Speedtest

def run_speedtest(
    secure: bool = True,
    servers: list = None,
    threads: int = None,
) -> dict:
    """Run a speedtest and return the results.

    Arguments:
    ----------
        servers: list
            List of servers to test against. If None, a list of
            servers will be chosen based on who's the best by latency.
            Default is None.
        threads: int
            Number of threads to use. If None, the speedtest will not be limited
            to a set number of threads. Default is None.
    """
    if not isinstance(servers, list):
        servers = []

    s = Speedtest(secure=secure)
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()

    return s.results.dict()

def create_table(db_name, table_name):
    db = connect(db_name)
    c = db.cursor()
    c.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            server_id NUM
            , sponsor TEXT
            , server_name TEXT
            , timestamp TEXT NOT NULL
            , distance REAL
            , ping REAL NOT NULL
            , download REAL NOT NULL
            , upload REAL NOT NULL
            , share TEXT
            , ip_address TEXT
        )
        """
    )
    db.commit()
    db.close()

def insert_into_db(db_name, table_name, data):
    db = connect(db_name)
    c = db.cursor()
    print(f'inserting to table {table_name} the following data: {data}')

    c.execute(
        f"""
        INSERT INTO {table_name}
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        data
    )
    db.commit()
    db.close()

def main(speedtest_exec_path: str, db_path: str):
    print('Beginning speed test...')

    # TODO: use the speedtest library to run the speedtest instead of a subprocess shell call
    # results = run_speedtest()

    speed_check = check_output([speedtest_exec_path, '--csv','--secure'])
    speed_check = speed_check.decode('utf-8').strip()
    speed_check = speed_check.split(',')

    print('Creating database...')
    create_table(db_path, 'speedtest')

    print('Inserting data into database...')
    insert_into_db(db_path, 'speedtest', speed_check)

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        '--db_path',
        help='Path to your SQLite database file. Gets created if it does not exist.',
        required=True,
    )
    parser.add_argument(
        '--speedtest_exec_path',
        help='Path to your speedtest-cli executable.',
        required=True,
    )
    args = parser.parse_args()

    main(args.speedtest_exec_path, args.db_path)
