# ledman

A LED command and control thing. Build with [pi-blaster](https://github.com/sarfata/pi-blaster) and [Bottle](http://bottlepy.org/).
Runs on Rasbian Jissie and likely other things to. 

## Install
First install [pi-blaster](https://github.com/sarfata/pi-blaster).

Then get Ledman. These command assume you use Rasbian Jissie with the Systemd (which is default), but feel free to rol your own.

    git clone https://github.com/victorhaggqvist/ledman
    sudo aptitude install uwsgi uwsgi-plugin-python3 python3-bottle nginx
    
    sudo rm /etc/nginx/sites-enabled/default
    cp /home/pi/ledman/nginx.conf.sample /home/pi/ledman/nginx.conf
    sudo ln -s /home/pi/ledman/nginx.conf /etc/nginx/sites-enabled/ledman
    sudo ln -s /home/pi/ledman/ledman.ini /etc/uwsgi/ledman.ini
    sudo cp /home/pi/ledman/ledman.autostart.service /etc/systemd/system/ledman.autostart.service
    sudo mkdir -p /etc/uwsgi # this dir may not exist
    sudo cp /home/pi/ledman/ledman.uwsgi.service /etc/systemd/system/ledman.uwsgi.service
    
    sudo systemctl enable ledman.autostart.service
    sudo systemctl enable ledman.uwsgi.service
    sudo systemctl start ledman.uwsgi.service
    sudo systemctl start nginx
    
You may need to alter the above paths or the paths in the config files to fit your needs.
    
## Config
On first run a config file will be created. Edit it as you like.

Multiple apikeys may be added comma (,) separeted, have a look in `ledman.conf`.

Also since the the server make use of tmiebased tokens for auth, make sure to have your timezone setup. On a debian system this can be done like so.

    sudo dpkg-reconfigure tzdata

## License

    The MIT License (MIT)

    Copyright (c) 2015 Victor Häggqvist <victor@hggqvst.com>
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
