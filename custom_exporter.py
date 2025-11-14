from prometheus_client import start_http_server, Gauge
import mysql.connector
import time

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'NewPassword123!',
    'database': 'uefa_champions_league_2025'
}

# === Метрики ===
active_connections = Gauge('mysql_active_connections', 'Number of active MySQL connections')
table_count = Gauge('mysql_table_count', 'Number of tables in the database')
uptime_seconds = Gauge('mysql_uptime_seconds', 'MySQL server uptime in seconds')
database_size_mb = Gauge('mysql_database_size_mb', 'Total database size in MB')
query_rate = Gauge('mysql_query_rate', 'Approximate queries executed per minute')
row_count = Gauge('mysql_row_count', 'Total number of rows in all tables')

def collect_metrics():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Активные подключения
    cursor.execute("SHOW STATUS LIKE 'Threads_connected';")
    active_connections.set(int(cursor.fetchone()[1]))

    # Количество таблиц
    cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = DATABASE();")
    table_count.set(cursor.fetchone()[0])

    # Аптайм
    cursor.execute("SHOW STATUS LIKE 'Uptime';")
    uptime_seconds.set(int(cursor.fetchone()[1]))

    # Размер базы данных (MB)
    cursor.execute("""
        SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2)
        FROM information_schema.tables WHERE table_schema = DATABASE();
    """)
    size = cursor.fetchone()[0]
    database_size_mb.set(size if size else 0)

    # Количество запросов (примерно)
    cursor.execute("SHOW GLOBAL STATUS LIKE 'Questions';")
    total_queries = int(cursor.fetchone()[1])
    query_rate.set(total_queries / 60)

    # Количество строк во всех таблицах
    cursor.execute("""
        SELECT SUM(table_rows) FROM information_schema.tables
        WHERE table_schema = DATABASE();
    """)
    total_rows = cursor.fetchone()[0]
    row_count.set(total_rows if total_rows else 0)

    cursor.close()
    conn.close()

if __name__ == '__main__':
    print("Custom MySQL Exporter running on port 9105 ...")
    start_http_server(9105)
    while True:
        collect_metrics()
        time.sleep(20)
