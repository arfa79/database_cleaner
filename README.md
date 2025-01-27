# Python Backup Automation with Docker

This project automates the process of backing up old records from an RDBMS (MySQL), saving them as CSV files, and then deleting the old records from the database. The backup script is set to run at regular intervals using Docker and Docker Compose. It also includes a supervisor to restart the script in case of any errors.

## Features
- Automatic backup of database records older than a specified number of days.
- Old records are removed from the database after backup.
- Backup is saved as CSV files with timestamps.
- Environment variables are used for database connection details and other configurations.
- Docker Compose is used to orchestrate services, including MySQL and the backup service.
- Supervisor ensures the backup script automatically restarts in case of failure.
- Logs for the backup process are stored for error tracking.

## Prerequisites

Before running this project, ensure you have the following installed:
- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Project Structure

```bash
.
├── backup_script.py           # Python script to perform backup and delete records
├── Dockerfile                 # Dockerfile to build the backup container
├── docker-compose.yml         # Docker Compose file to manage the services
├── requirements.txt           # Python dependencies
├── supervisord.conf           # Supervisor configuration for managing the backup script
└── README.md                  # Project documentation
```

## Environment Variables

The following environment variables are used in the `docker-compose.yml` file to configure the backup script:

- `DB_HOST`: Hostname for the MySQL database (default: `db` in Docker Compose setup).
- `DB_USER`: MySQL username for the database.
- `DB_PASSWORD`: MySQL password for the database.
- `DB_NAME`: Name of the MySQL database.
- `N_DAYS`: Number of days before which records are considered old and need to be backed up (default: `7` days).
- `BACKUP_DIR`: Directory path inside the container where the backups will be stored (default: `/backup`).

These variables can be modified directly in the `docker-compose.yml` file under the `backup` service.

## How to Run

### 1. Clone the repository:

```bash
git clone <repository-url>
cd <project-folder>
```

### 2. Build and run the project:

```bash
docker-compose up --build
```

This command will:
- Set up a MySQL database in a Docker container.
- Build and run the Python backup service in a separate Docker container.
- The Python script will run every 24 hours and take backups of the old records from the database.

### 3. Stop the services:

```bash
docker-compose down
```

This will stop all running containers.

## Docker Compose Services

- **db**: The MySQL database service.
- **backup**: The Python backup service, which is scheduled to run periodically and create backup files for records older than `n` days.

## Supervisor

Supervisor is used inside the `backup` service to manage the execution of the Python script. It ensures that the script is automatically restarted if it crashes for any reason. The logs for the backup process are saved in `/var/log/backup_script.out.log` for standard output and `/var/log/backup_script.err.log` for errors.

## Logs

Backup logs are generated inside the container at the following locations:
- **Standard Output**: `/var/log/backup_script.out.log`
- **Error Log**: `/var/log/backup_script.err.log`

## Backup Files

Backup files are stored in the `/backup` directory inside the container. The file names follow the format:

```
backup_YYYYMMDD_HHMMSS.csv
```

Each file contains the records older than the specified `N_DAYS` threshold at the time the backup was taken.

To access the backup files on your host system, you can map the volume in the `docker-compose.yml` to a folder on your machine by editing this section:

```yaml
volumes:
  - ./backup:/backup
```

## Customization

You can adjust the frequency of the backup execution by modifying the `sleep` duration in the `docker-compose.yml` entrypoint:

```yaml
entrypoint: ["sh", "-c", "while true; do python backup_script.py; sleep 86400; done"]
```

Change `86400` to the number of seconds you want the script to wait between executions. (e.g., `3600` for one hour).

## License

This project is licensed under the GPL3 License.