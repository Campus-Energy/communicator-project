# Commmunicator Project

## Setup

1. Manually create `campusenergy` user on the server (only needed for first-time setup)
2. Switch to the `campusenergy` user

    ```sh
    su campusenergy
    ```

3. Go to `campusenergy` home directory

    ```sh
    cd /home/campusenergy
    ```

4. Clone `campusenergy` repository

    ```sh
    git clone https://github.com/Campus-Energy/communicator-project.git
    ```

5. `cd` into repository folder

    ```sh
    cd communicator-project
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
