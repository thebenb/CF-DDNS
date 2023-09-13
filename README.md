# CF-DDNS

A simple "quick and dirty" DNS record updater for people with a Dynamic IP who use Cloudflare.

Written semi-minimally in Python.

## Features

-   Automatically grabs current public IP and updates configured subdomains
    -   Does not update other info (such as the proxy toggle or record type), allowing you to do that from the dashboard
-   Low performance footprint (As far as I know)
-   Uses the official Cloudflare API library
-   Simple JSON configuration to hold all data
    -   Subdomains
    -   Cloudflare API details
    -   Checking interval
-   Supports addition of Discord Webhook which provides summaries if records are changed
-   Does not send excessive API requests (only updates on first launch or when IP changes)

## Installation

I built this to run as a docker container, but if you just want to run `main.py` somewhere, go ahead, just make sure you run `pip install -r requirements.txt` first. I won't stop you. If anyone needs I can add other run methods such as a cronjob-compatible implementation (just ask me and I'll do it for you).

### 1. Download

Feel free to download the repo as a .zip or clone it to a folder of your choice with:

```shell
git clone https://github.com/thebenb/CF-DDNS.git
```

### 2. Configure

Copy (or rename) the `config_tempalte.json` to `config.json` and edit file to match your credentials. At a bare minimum, your config should look like this:

```json
{
    "subdomains": ["something.example.com"],
    "config": {
        "api_key": "Your API key for the zone",
        "zone_id": "Your Zone ID",
        "check_interval": 300,
        "discord_webhook": ""
    }
}
```

_`discord_webhook`_ is left blank, meaning that no discord notification will be sent

For those not familiar with JSON: Each subdomain needs to be in quotations and with a comma inbetween them.

### 3. Run

Assuming you have `docker-compose` installed, just run:

```bash
docker-compose up -d
```

Every time you update the `config.json`

Enjoy!

## Potential upgrades:

-   [ ] Adding more customisation to the discord webhook (Currently details such as name and photo must be done on discord)
-   [ ] Adding the ability to run the script in other ways (Not Docker-compose)

If there's a demand I'll add these features.

## Notes

This is one of my first ever "published" scripts designed for public use/adaptation so some of my implementation may be concerning or strange. This is very much a "set and forget" system so I'm not overly concerned, but any upgrades / advice are welcome and appreciated.

This is also written in a fairly "hands off" and opinionated manner, I encourage you to do a google search if you have trouble with getting info such as your API key, Cloudflare have the most updated documentation on this so I believe that they're the best place to go.
