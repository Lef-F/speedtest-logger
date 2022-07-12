# Home internet speedtest

Wanna log your internet speed smoothly over time?

No worries, with the help of Python, [`speedtest-cli`](https://github.com/sivel/speedtest-cli) and SQLite you can run the following Python script in e.g. a `cronjob` and store the results one row at a time in the `speedtest` table of your `speedtest.db`.

Every time you execute `speedtest.py` it will add a new row to your `speedtest` table in your SQLite database.

```shell
python3 run_speedtest.py --db-path /path/to/my/speedtest.db
```

## My use-case

As an example, I'm running this every 10 minutes on my Raspberry Pi 4 at home using `cron` as follows:

```shell
*/10 * * * * ( cd /home/pi/speedtest-logger/ && python3 run_speedtest.py --db-path /opt/grafana/speedtest.db >> /home/pi/speedtest-logger/speedtest.log 2>&1 )
```

I'm wrapping the script in `()` so that it runs in a subshell.
This way I can `cd` into the directory where I cloned this repo.
And if the `cd` succeeds (`&&`) then `run_speedtest.py` runs and reports all its output (errors included `2>&1`) to a `speedtest.log` file, which I can check in case things are not working as expected.

---

## Setup

There are two main ways to setup the logger.

### Just git clone

Simply recursively clone this repository into whatever you wish to run it in e.g. the device, VM, container, parallel dimension etc.

The `speedtest-cli` repository that we depend on is a submodule of this repository.

```shell
git clone --recursive git@github.com:Lef-F/speedtest-logger.git
```

### Install as Python module

The application comes with `poetry` support and a `pyprojec.toml` which means you have a few options for installation.

#### The poetik way

First clone the repository:

```shell
git clone git@github.com:Lef-F/speedtest-logger.git
```

And then run `poetry install` to install the environment.

#### Using `pip`

Simply run `pip install -r requirements.txt`

## General notes

### speedtest module return dictionary

Running a speedtest with the `Speedtest` class of the `speedtest` Python module returns a dictionary with the following structure:

```json
{
    "download": 246470932.56381902,
    "upload": 52436099.26189703,
    "ping": 32.15,
    "server": {
        "url": "http://gbg-shg-speedtest1.bahnhof.net:8080/speedtest/upload.php",
        "lat": "57.7000",
        "lon": "11.9667",
        "name": "Gothenburg",
        "country": "Sweden",
        "cc": "SE",
        "sponsor": "Bahnhof AB",
        "id": "34190",
        "host": "gbg-shg-speedtest1.bahnhof.net:8080",
        "d": 402.1657229051038,
        "latency": 32.15
    },
    "timestamp": "2022-07-12T07:52:28.700544Z",
    "bytes_sent": 65667072,
    "bytes_received": 308975016,
    "share": "http://www.speedtest.net/result/13395521006.png",
    "client": {
        "ip": "123.123.123.123",
        "lat": "41.321",
        "lon": "12.118",
        "isp": "Tele2 Sweden",
        "isprating": "3.7",
        "rating": "0",
        "ispdlavg": "0",
        "ispulavg": "0",
        "loggedin": "0",
        "country": "SE"
    }
}
```
