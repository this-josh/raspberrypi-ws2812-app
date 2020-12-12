cd /src/git/raspberrypi
echo activating env
source lights_app/bin/activate
echo starting server
sudo lights_app/bin/python3 build_app.py

# sudo /home/src/git/raspberrypi/lights_app/bin/python3 build_app.py/


# cd /lib/systemd/system/

# source /src/git/raspberrypi/on.sh

# sudo systemctl daemon-reload
# sudo systemctl enable lights.service
# sudo systemctl start lights.service
# systemctl status lights.service

# sudo systemctl stop lights.service
# sudo systemctl disable lights.service
