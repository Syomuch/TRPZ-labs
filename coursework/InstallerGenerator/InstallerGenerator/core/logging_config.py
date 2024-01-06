import logging
import sqlite3


class SQLiteLogHandler(logging.Handler):
    """
    A custom logging handler that stores log records in a SQLite database.

    :param db: Path to the SQLite database file (default: '.\\installer_logs.db')
    :type db: str
    """
    def __init__(self, db: str = r'.\installer_logs.db'):
        """
        Initialize the SQLiteLogHandler.

        :param db: Path to the SQLite database file (default: '.\\installer_logs.db')
        :type db: str
        """
        super().__init__()
        self.db: str = db
        self.conn: sqlite3.Connection = sqlite3.connect(self.db)
        self.cur: sqlite3.Cursor = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                time TEXT,
                level TEXT,
                message TEXT
            )
        """)
        self.conn.commit()

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit a log record by inserting it into the SQLite database.

        :param record: The log record to be emitted.
        :type record: logging.LogRecord
        """
        log_entry: str = self.format(record)
        self.cur.execute("INSERT INTO logs (time, level, message) VALUES (?, ?, ?)",
                         (record.asctime, record.levelname, log_entry))
        self.conn.commit()

def setup_logging() -> None:
    """
    Configure the logging system to use a SQLiteLogHandler and save logs to a file.

    This function sets up the logging system to store logs in a file named 'installer_creator.log' and
    also adds the SQLiteLogHandler to store logs in an SQLite database.

    Usage:
    ```
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("This is an example log message.")
    ```

    :return: None
    """
    logging.basicConfig(filename='.\installer_creator.log', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    sqlite_handler: SQLiteLogHandler = SQLiteLogHandler()
    sqlite_handler.setLevel(logging.INFO)
    formatter: logging.Formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    sqlite_handler.setFormatter(formatter)
    logging.getLogger().addHandler(sqlite_handler)
