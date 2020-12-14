Note the app is run as lights.service
# useful commands
```
sudo systemctl stop lights.service
sudo systemctl daemon-reload
sudo systemctl start lights.service
systemctl status lights.service

cd /etc/systemd/system/multi-user.target.wants

nano `ls -Art | tail -n 1`
```
