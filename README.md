# CF-DDNS

A simple "set up once and forget" DNS record updater for people with a Dynamic IP who use Cloudflare.

Written semi-minimally in Python.

## Features

-   Automatically grabs current public IP and updates configured subdomains
    -   Does not update other info (such as the proxy toggle or record type), allowing you to do that from the dashboard
-   Low performance footprint (As far as I know)
-   Uses the official Cloudflare API library
-   Simple JSON configuration to hold data
    -   Cloudflare API details
    -   Checking interval
-   Supports addition of Discord Webhook which provides summaries if records are changed
-   Does not send excessive API requests (only updates specific records on IP change)

## Work in Progress

-   [ ] Better installation method
-   [ ] Publishing to Docker hub(?)

## How it works

1. When the program is first started, it keeps a record of your current IP address and stores it locally. (The IP is then read from the storage from then on.)
2. Every `x` minutes, the program checks your machine's IP address again, and compares it to the stored IP.
3. If the IPs are different, the Cloudflare API is used to search your records that point to the stored IP.
4. Those records are then edited to reflect your new IP address.
5. (Optional) you get a nifty discord message telling you what happened.

## Installation

I built this to run as a docker container, but if you just want to run `main.py` somewhere, go ahead, just make sure you run `pip install -r requirements.txt` first. I won't stop you. If anyone needs I can add other run methods such as a cronjob-compatible implementation (just ask me and I'll do it for you).

### 1. Download

Feel free to download the repo as a .zip or clone it to a folder of your choice with:

```shell
git clone https://github.com/thebenb/CF-DDNS.git
```

### 2. Configure

Copy (or rename) the `config_template.json` to `config.json` and edit file to match your credentials. At a bare minimum, your config should look like this:

```json
{
    "config": {
        "api_key": "Your API key for the zone",
        "zone_id": "Your Zone ID",
        "check_interval": 300,
        "discord_webhook": "Put a discord webhook link here or leave it blank to disable the feature"
    }
}
```

If `discord_webhook` is left blank, meaning that no discord notification will be sent

### 3. Run

Assuming you have `docker` installed, just run:

```bash
docker build -t cf-ddns .
docker run --restart always cf-ddns
```

Enjoy!

## Potential upgrades:

-   [ ] Adding more customisation to the discord webhook (Currently details such as name and photo must be done on discord)
-   [ ] Adding the ability to run the script in other ways (Not Docker-compose)

If there's a demand I'll add these features.

## Notes

This is one of my first ever "published" scripts designed for public use/adaptation so some of my implementation may be concerning or strange. This is very much a "set and forget" system so I'm not overly concerned, but any upgrades / advice are welcome and appreciated.

This is also written in a fairly "hands off" and opinionated manner, I encourage you to do a google search if you have trouble with getting info such as your API key, Cloudflare have the most updated documentation on this so I believe that they're the best place to go.
