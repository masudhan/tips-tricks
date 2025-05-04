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

**Create user in linux**

`sudo useradd -m -s /bin/bash madhu`

`sudo passwd madhu`

`sudo usermod -aG sudo madhu` #Give sudo privileges

`sudo usermod -aG docker madhu` #Add to docker group

***Add user to sudoers(if not already in sudo group)***

`sudo visudo`

`madhu ALL=(ALL:ALL) ALL`

`sudo -l` #Check sudo access

`sudo userdel -r madhu` # -r = remove home directory too


