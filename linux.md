`timedatectl set-timezone Asia/Kolkata` </br>


**Update Specific package**

`sudo apt --only-upgrade install python`

**Hold package for upgrade**

`sudo apt-mark hold systemd`

`sudo apt-mark unhold systemd`

**Clean up**

`sudo apt autoremove`

`sudo apt autoclean`

`sudo apt-add-repository -r ppa:certbot/certbot`

after that `sudo apt update` `sudo apt-get update`

**Useful Packages**

`sudo apt install bat` - usage `batcat file.py`

**Resize root partition**

`sudo apt install cloud-guest-utils`

`sudo growpart /dev/xvda 1`

`sudo resize2fs /dev/xvda1`

`df -hT`
