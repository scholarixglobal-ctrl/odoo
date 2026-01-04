FROM odoo:19.0

USER root

# Install Python dependencies for auto_database_backup module
RUN pip3 install --no-cache-dir --break-system-packages \
    dropbox \
    pyncclient \
    boto3 \
    nextcloud-api-wrapper \
    paramiko

USER odoo
