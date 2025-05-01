#!/bin/bash

# MycoMonitor Backup Script
# Creates a backup of configuration and data

# Settings
BACKUP_DIR="/var/backups/mycomonitor"
CONFIG_DIR="/etc/mycomonitor"
DATA_DIR="/var/lib/mycomonitor"
LOG_DIR="/var/log/mycomonitor"
BACKUP_RETAIN_DAYS=30

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="mycomonitor_backup_${TIMESTAMP}.tar.gz"

# Ensure backup directory exists
mkdir -p "${BACKUP_DIR}"

# Create backup
tar czf "${BACKUP_DIR}/${BACKUP_NAME}" \
    --warning=no-file-changed \
    "${CONFIG_DIR}" \
    "${DATA_DIR}" \
    "${LOG_DIR}"

# Remove old backups
find "${BACKUP_DIR}" -type f -name "mycomonitor_backup_*.tar.gz" -mtime +${BACKUP_RETAIN_DAYS} -delete

# Create checksum
cd "${BACKUP_DIR}"
sha256sum "${BACKUP_NAME}" > "${BACKUP_NAME}.sha256"

# Set permissions
chown pi:pi "${BACKUP_DIR}/${BACKUP_NAME}"*
chmod 640 "${BACKUP_DIR}/${BACKUP_NAME}"*

echo "Backup completed: ${BACKUP_DIR}/${BACKUP_NAME}"
