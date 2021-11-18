# TamarTagNotify
Simple Python service to check your current Tamar Tag balance and message you if it drops below a set minimum.

## Install
1. Install the requirements for all users: `sudo pip3 install -r requirements.txt`
2. Copy the `config.json` into the `~/.config/tamar_tag/` directory and customise the data
3. Copy the `tamarTag.service` and `tamarTag.timer` into your `/etc/systemd/system/` directory and set the `User` and `OnCalender`
4. Enable the timer: `systemctl enable tamarTag.timer`
