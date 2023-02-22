# WGmetrics
This project provides a simple web app that returns Wireguard peers' statistics as a JSON

## Run WGmetrics
* `git clone git@github.com:Improvy/WGmetrics.git`
* `cd WGMetrics`
* `pip install -r /path/to/requirements.txt`
* Set environment variables `WGMETRICS_HOST` and `WGMETRICS_PORT` with IP address and port which the application should listen to
* Run the app `python3 web/app.py`
* Then send the GET request to `http://IP:port/wgmetrics?interface={wireguard_interface}` (for example: `http://IP:port/wgmetrics?interface=wg0`)