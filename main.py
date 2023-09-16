import requests
import time
import json
import CloudFlare


def load_config():
    # Load the JSON configuration file
    with open("config.json", "r") as config_file:
        config = json.load(config_file)

    config = config.get("config", {})

    return config


def get_ip():
    ip = requests.get("https://api.ipify.org").text
    return ip


def send_notification(discord_webhook, summary_data):
    summary = (
        f"Your IP has changed to {summary_data[0]}.\n\n"
        + "**The following has occurred:**\n"
        + "\n".join(["- " + line for line in summary_data[1:]])
    )

    message = {"content": summary}

    message_json = json.dumps(message)

    # Set the headers to specify the content type as JSON
    headers = {"Content-Type": "application/json"}

    # Send a POST request to the Discord webhook URL with the message JSON data
    response = requests.post(discord_webhook, data=message_json, headers=headers)


def find_subdomains(cf, stored_ip, zone_id):
    # Fetch all DNS records for the specified zone
    try:
        dns_records = cf.zones.dns_records.get(zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
        print(f"Error fetching DNS records: {e}")
        exit(1)

    # Find subdomains with the target IP
    matching_subdomains = [
        record["name"] for record in dns_records if record["content"] == stored_ip
    ]

    # Print the matching subdomains
    print(f"Subdomains with IP {stored_ip}:")
    for subdomain in matching_subdomains:
        print(subdomain)

    return matching_subdomains


def set_ip(cf, subdomain, new_ip, zone_id):
    # Get the DNS records for the specified zone
    dns_records = cf.zones.dns_records.get(zone_id)

    for record in dns_records:
        if record["name"] == subdomain:
            record_to_update = record
            break

    if record_to_update is None:
        raise Exception(f"Record not found for {subdomain}")

    record_to_update["content"] = new_ip

    try:
        response = cf.zones.dns_records.put(
            zone_id, record_to_update["id"], data=record_to_update
        )

        print("Updated Record: " + subdomain)
        return f"Successfully updated `{subdomain}`"

    except CloudFlare.exceptions.CloudFlareAPIError as e:
        error = f"Error updating {subdomain}: {e}"
        print(error)
        return error


def main():
    config = load_config()
    api_key = config.get("api_key")
    zone_id = config.get("zone_id")
    discord_webhook = config.get("discord_webhook")

    current_ip = get_ip()

    try:
        with open("ip.txt", "r") as file:
            stored_ip = file.read()
    except:
        stored_ip = current_ip

    with open("ip.txt", "w") as file:
        file.write(current_ip)

    summary_data = [current_ip]

    while True:
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        if current_ip != stored_ip:
            cf = CloudFlare.CloudFlare(token=api_key)

            subdomains = find_subdomains(cf, stored_ip, zone_id)

            for subdomain in subdomains:
                result = set_ip(cf, subdomain, current_ip, zone_id)

                summary_data.append(result)

            stored_ip = current_ip

            if discord_webhook:
                send_notification(discord_webhook, summary_data)

        time.sleep(config.get("check_interval"))


if __name__ == "__main__":
    main()
