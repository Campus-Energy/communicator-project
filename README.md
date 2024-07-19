# Communicator Project

## Setup

1. Manually create the `campusenergy` user on the server (only needed for first-time setup).

2. Switch to the `campusenergy` user.

    ```sh
    su campusenergy
    ```

3. Go to the `campusenergy` home directory.

    ```sh
    cd /home/campusenergy
    ```

4. Ensure there is a `.pgpass` file set up in the home directory of the user that will run the cron job. Verify that it has the correct permissions.

    Create the `.pgpass` file if it doesn't exist.
    
    ```sh
    touch ~/.pgpass
    ```

    Edit the `.pgpass` file to add your database credentials.
    
    ```sh
    nano ~/.pgpass
    ```

    Add the following line (replace with your actual credentials):
    
    ```plaintext
    localhost:5432:uhm2023:campusenergy:your_password
    ```

    Set the correct permissions.
    
    ```sh
    chmod 600 ~/.pgpass
    ```

5. Clone the `communicator-project` repository.

    ```sh
    git clone https://github.com/Campus-Energy/communicator-project.git
    ```

6. Create a folder in the home directory named `inbox`; files pending data extraction and upload should be placed here.

    ```sh
    mkdir inbox
    ```

7. `cd` into the repository folder.

    ```sh
    cd communicator-project
    ```

8. Install python3 packages from `requirements.txt`.

    ```sh
    sudo pip3 install -r requirements.txt
    ```

9. Run `init_crontab.py`.

    ```sh
    python3 /home/campusenergy/communicator-project/init_crontab.py <interval - minute, hourly, daily, weekly, or monthly> /home/campusenergy/communicator-project/db_upload.py /home/campusenergy/db_upload.log
    ```

10. Check the log file to verify script execution.

    ```sh
    cd ..
    cat db_upload.log
    ```

11. To remove the cron job, open the crontab file and delete the line with the existing cron job:

    ```sh
    crontab -e
    ```

    The job will look something like this:
    ```plaintext
    * * * * * /usr/bin/python3 /home/campusenergy/communicator-project/db_upload.py >> /home/campusenergy/db_upload.log 2>&1 # Communicator data processing job
    ```

    Delete the line and save your deletion.

