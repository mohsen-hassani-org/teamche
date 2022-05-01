import os
import subprocess
from django.conf import settings

def backup_database(name):
    """Backup database using dbbackup module."""
    if (
        not name.endswith('.gz') or
        not name.endswith('.bz2') or
        not name.endswith('.zip') or
        not name.endswith('.gzip')
    ):
        name += '.gz'
    db_host = settings.DATABASES['default']['HOST']
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    backup_path = os.path.join(settings.DBBACKUP_STORAGE_OPTIONS['location'], name)
    dump_table(db_host, db_name, db_user, backup_path)
    return name

def restore_database(name):
    """Restore database using dbbackup module."""
    db_host = settings.DATABASES['default']['HOST']
    db_name = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    backup_path = os.path.join(settings.DBBACKUP_STORAGE_OPTIONS['location'], name)
    restore_table(db_host, db_name, db_user, backup_path)
    return

    

def dump_table(host_name, database_name, user_name, output):
    subprocess.run([
        'pg_dump',
        '-h', host_name,
        '-d', database_name,
        '-U', user_name,
        '-p', '5432',
        '-Fc',
        '-f', output
    ])

def restore_table(host_name, database_name, user_name, backup):
    subprocess.run([
        'pg_restore',
        '-h', host_name,
        '-d', database_name,
        '-U', user_name,
        '-p', '5432',
        '--clean',
        backup
    ])
