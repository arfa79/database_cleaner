import os
import csv
import mysql.connector
from datetime import datetime, timedelta

db_host = os.getenv('DB_HOST', 'localhost')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', 'password')
db_name = os.getenv('DB_NAME', 'mydatabase')
n_days = int(os.getenv('N_DAYS', '7'))
backup_dir = os.getenv('BACKUP_DIR', '/backup')

def connect_to_database():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

def backup_and_delete():
    conn = connect_to_database()
    cursor = conn.cursor()
    
    today = datetime.now()
    old_date = today - timedelta(days=n_days)
    
    cursor.execute("SELECT * FROM records WHERE date < %s", (old_date,))
    records = cursor.fetchall()

    if not records:
        print("No records to backup.")
        return
    
    backup_file = os.path.join(backup_dir, f"backup_{today.strftime('%Y%m%d_%H%M%S')}.csv")
    with open(backup_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i[0] for i in cursor.description])
        writer.writerows(records)
