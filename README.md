# Commmunicator Project

## Setup

1. Manually create `communicator` user on the server (only needed for first-time setup)
2. Switch to the `communicator` user

    ```sh
    su communicator
    ```

3. Go to `communicator` home directory

    ```sh
    cd /home/communicator
    ```

4. Clone `communicator` repository

    ```sh
    git clone <url>
    ```

5. `cd` into repository folder

    ```sh
    cd <project folder name>
    ```

6. Install python3 packages from `requirements.txt`

    ```sh
    sudo pip3 install -r requirements.txt
    ```

7. Run `init_crontab.py`

    ```sh
    python3 init_crontab.py <interval> <path/to/your_script.py>
    ```

    - Replace `<interval>` with one of `hourly`, `daily`, `weekly`, or `monthly`.
    - Replace `<path/to/your_script.py>` with the actual path to the script you want to schedule.
