# MAC Address Verifier

## Description
This tool verifies MAC addresses by running a series of tests to confirm whether
input provided by the user is a valid or not. It can verify one MAC address at a time.

Supported formats:
1. XX:XX:XX:XX:XX:XX
2. XXXX.XXXX.XXXX
3. XXXXXXXXXXXX

The tool itself utilizes Python and Flask to create a REST API for the end user. The whole thing
is run inside a Docker container and in order to simplify the setup the process Ansible is used to automagically build the Docker image and run it inside a Docker container.

API endpoint is accessible by making the following query 
```
http://<server-address>:5001/verify-mac-address/XX:XX:XX:XX:XX:XX
```

For example when you run this scrip locally on your own computer you can access the API by going to the following address http://localhost:5001/verify-mac-address/00:1b:63:84:45:e6

Response is returned in a JSON format and includes three key-value pairs: formats, result, vendor.
- Formats: Valid MAC address is returned in all three formats supported by the script.
- Results: A simple OK/NOK response
- Vendor: Vendor name of the MAC address (this information provided by macvendor.com and its public API)

```
Example:
{
    "formats":["001b638445e6","00:1b:63:84:45:e6","001b.6384.45e6"],
    "result":"OK",
    "vendor":"Apple, Inc."
}
```

Additionally the Docker image also contains Prometheus and its set to run Node Exporter that  
collects and exposes a wide variety of hardware and kernel-related metrics. It can be accessed by going to the following address.
```
http://localhost:9090/
```


## Installation instructions
***It is assumed that Docker and Ansible are already installed on your system.***

***Make sure the Docker service is running.***

Install Python Docker module. This module allows Ansible to communicate with Docker over its API.
```
python -m pip install docker
```

Run the the Ansible playbook. It automagically creates the Docker image and starts it.
```
ansible-playbook /playbooks/playbook_mac_verifier.yml
```

That's it! You can either check the Docker graphical user-interface or command-line
to confirm that the Docker container is running.
```
docker ps
```

Visit the following website to make your MAC address related queries:
```
http://localhost:5001/verify-mac-address/00:1b:63:84:45:e6
```

Its output should look something like this.
```
{
    "formats":["001b638445e6","00:1b:63:84:45:e6","001b.6384.45e6"],
    "result":"OK",
    "vendor":"Apple, Inc."
}
```

You can also visit the following address to access Prometheus endpoint.
```
http://localhost:9090/
```