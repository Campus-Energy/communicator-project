import argparse
import os
import sys
from crontab import CronTab

def add_cron_job(interval, command, log_file):
    # User's crontab
    cron = CronTab(user=True)

    # Check if the cron job already exists
    job_exists = False
    for job in cron:
        if job.command == command:
            job_exists = True
            break

    # If the job does not exist, add it
    if not job_exists:
        job = cron.new(command=command, comment='Communicator data processing job')
        
        # Set the job interval based on user input
        if interval == 'minute':
            job.minute.every(1)
        elif interval == 'hourly':
            job.hour.every(1)
        elif interval == 'daily':
            job.hour.every(24)
        elif interval == 'weekly':
            job.dow.on('SUN')
        elif interval == 'monthly':
            job.day.on(1)
        else:
            print('Invalid interval specified.')
            return
        
        cron.write()
        print(f'Cron job added to run {interval}.')
    else:
        print('Cron job already exists.')

def ensure_communicator_user():
    if os.geteuid() != 0:
        if os.getlogin() != 'lydia':
            print("This script must be run by the 'communicator' user.")
            sys.exit(1)

def ensure_log_directory(log_file):
    log_dir = os.path.dirname(log_file)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f'Created log directory: {log_dir}')
    else:
        print(f'Log directory already exists: {log_dir}')

if __name__ == '__main__':
    ensure_communicator_user()
    
    parser = argparse.ArgumentParser(description='Add a cron job to run a script at a specified interval.')
    parser.add_argument('interval', type=str, choices=['minute', 'hourly', 'daily', 'weekly', 'monthly'],
                        help='Interval at which to run the cron job (minute, hourly, daily, weekly, monthly)')
    parser.add_argument('script_path', type=str, help='Path to the script to be run by the cron job')
    parser.add_argument('log_file', type=str, help='Path to the log file')

    args = parser.parse_args()
    
    ensure_log_directory(args.log_file)

    command = f'/usr/bin/python3 {args.script_path} >> {args.log_file} 2>&1'
    add_cron_job(args.interval, command, args.log_file)