# ledman

A LED command and control thing. Build with pi-blaster and bottle.

# Install

    cd ~
    git clone https://github.com/victorhaggqvist/ledman
    cd ledman
    sudo apt-get install python-pip
    sudo pip install -r requirements.txt
    sudo rm /etc/nginx/sites-enabled/default
    sudo ln -s /home/pi/ledman/nginx.conf /etc/nginx/sites-enabled/ledman
    chmod +x ledman.py
    ./ledman -s start
