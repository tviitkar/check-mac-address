# MAC Address Verifier

## Description
As the name says MAC Address Verifier verifies MAC addresses by running a series of tests to confirm whether
input provided by user is a valid or not. It can verify one MAC address at a time.

Supported formats:
1. XX:XX:XX:XX:XX:XX
2. XXXX.XXXX.XXXX
3. XXXXXXXXXXXX

The tool itself utilizes Python and Flask to create a REST API which can be accessed through CLI or a web browser. Application is run inside a Docker container and in order to simplify the setup the process Ansible is used to automagically build the Docker image and run it inside a Docker container.

API is accessible via the following address:
```
http://<server-address>:5001/verify-mac-address/XX:XX:XX:XX:XX:XX
```

As an example, when you run this script locally on your own computer you can access the API by visiting http://localhost:5001/verify-mac-address/00:1b:63:84:45:e6

Response is returned in a JSON format and includes three key-value pairs: formats, result, vendor.
- Formats: Valid and verified MAC address is returned in all three formats supported by the script.
- Result: A simple OK/NOK response
- Vendor: Vendor name of the MAC address (information provided by macvendors.com by utilizing its public API)

Example:
```

{
    "formats":["001b638445e6",
               "00:1b:63:84:45:e6",
               "001b.6384.45e6"],
    "result":"OK",
    "vendor":"Apple, Inc."
}
```

Additionally, the Docker image also contains Prometheus (open-source monitoring system) and its set to run Node Exporter that collects and exposes a wide variety of hardware and kernel-related metrics. It can be accessed by visiting the following address.
```
http://localhost:9090/
```

## Folder structure
```
├── Dockerfile
├── README.md
├── misc
│   ├── prometheus.yml
│   └── run_services.sh
├── playbooks
│   └── playbook_mac_verifier.yml
└── python
    ├── mac_verifier.py
    └── requirements.txt
```
- misc - contains shell scripts and configuration files that are copied to Docker image and are used once the container is run
- playbooks - Ansible playbook is stored here
- python - main application code (script) is stored here alongside with a list of Python package requirements

## Installation instructions

### Pre-requirements (assumptions)
1. Docker and Ansible are already installed on your system.
2. Docker service is running.
3. Python 3 is available since Ansible is written in Python and you can't have one without the other.

### Instructions
I've written these instructions from the perspective of Linux and MacOS. There might be slight variations depending on your exact working conditions, but the overall gist should be as described below.

Let's go!

Clone this Git repository to your computer. If you don't know how to use Git, then have a look at this tutorial: https://github.com/git-guides/install-git
```
git clone https://github.com/tviitkar/check-mac-address.git
```

Once the repository has been cloned to your computer move into the new folder.
```
cd check-mac-address/
```

Check if you have pip (Python package manager) available.
```
pip3 --version
```

If pip isn't available and you get an error message ***-bash: /usr/bin/pip3: No such file or directory*** then you can install the package manager by running the following command. Otherwise skip over to the next step.
```
sudo apt install python3-pip
```

Install Python Docker module. This module allows Ansible to communicate with Docker over its API. Without it, its not possible to run Ansible playbooks to create and manage Docker images, containers, etc.
```
python -m pip install docker
```

Run the the Ansible playbook. It automagically creates the Docker image and starts it. ***Give it a few minutes!*** If you want to have a better look at what's happening then run the the following command in verbose mode by appending -vvvv at the end of the command following command.
```
ansible-playbook playbooks/playbook_mac_verifier.yml
```

That's it!

Check Docker image list. You should see a file that is called ***"verify_mac_address"***.
```
docker image ls
```

Check Docker GUI or use the CLI to verify that the ***"verify_mac_address"*** container is running.
```
docker ps
```

Visit the following website to make your MAC address query.
```
http://localhost:5001/verify-mac-address/00:1b:63:84:45:e6
```

Or make your query through CLI.
```
curl http://localhost:5001/verify-mac-address/00:1b:63:84:45:e6
```

Output should look something like this.
```
{
    "formats":[
        "001b638445e6",
        "00:1b:63:84:45:e6",
        "001b.6384.45e6"],
    "result":"OK",
    "vendor":"Apple, Inc."
}
```

Prometheus is accessible at the following address.
```
http://localhost:9090/
```

## Known-issues

### urllib3 v2 incompatibility
Depending on your working environment (Python, Python package versions, etc) you might run into an issue where running the provided Ansible playbook fails and you are greeted with an error message ***docker.errors.DockerException: Error while fetching server API version: request() got an unexpected keyword argument 'chunked'.***

Apparently there's compability issue (bug) between some Python packages and its a fairily new, but known issue.

Link to the thread where this topic is discussed: https://github.com/docker/docker-py/issues/3113

As per recommendation(s) from the thread above, I reverted my Python requests module back to version 2.29 and that fixed the issue.
```
python3 -m pip install requests==2.29
```