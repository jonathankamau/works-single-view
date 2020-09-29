from scripts.database_connection import DatabaseConnection

db_conn = DatabaseConnection()
if __name__ == '__main__':
    db_conn.save_data()