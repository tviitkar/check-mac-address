import re
import requests
from flask import Flask, jsonify

# CONSTANTS
# Could probably move some of them into a separate 
# .ini file or something like that to condense the script
HOST = "0.0.0.0"  # Run Flask service on all interfaces
PORT = 5000  # Default port to access Flask APIs
SYMBOLS_TO_REMOVE = "[.:]"  # list of symbols to remove from mac address (used by regex)
MAC_ADDRESS_BIT_LENGTH = 48  # mac addresses consist of 48 bits
MAC_FORMAT_RULES = {0: None, 2: ":", 4: "."}  # rules how to split mac address and which separator symbol to use
MULTICAST_ADDRESS_PREFIX = "01005E"
BROADCAST_ADDRESS = "FFFFFFFFFFFF"

# FUNCTIONS
# api call to get vendor name from macvendors.com via its public api
def get_mac_vendor(mac_address: str) -> str:
    api_call_response = requests.get(f"https://api.macvendors.com/{mac_address}")
    if api_call_response.status_code == 200:
        return api_call_response.text
    return "Not found."

# APPLICATION
app = Flask(__name__)  # initialize flask

@app.route('/verify-mac-address/<address>', methods=["GET"])
def verify_mac_address(address):
    reformatted_macs = []  # empty list for reformatted mac addresses
    mac_vendor = ""  # mac vendor name
    
    # remove group separators (dots, semicolons, etc)
    address_no_grouping = re.sub(SYMBOLS_TO_REMOVE, "", address)

    response = "NOK"  # default response is that user provided value is not mac address
    if len(address_no_grouping) == 12:  # mac addresses are 12 character in length
        hex_to_int_success = False
        address_base16 = 0
                
        # convert hex string into a integer
        try:
            # conversion also catches invalid hex strings that use illegal characters
            address_base16 = int(address_no_grouping, 16)
            hex_to_int_success = True
        except ValueError as error:
            # illegal characters throw a ValueError
            pass
    
        if address_base16.bit_length() <= MAC_ADDRESS_BIT_LENGTH and hex_to_int_success:
            response = "OK"
        
            # convert mac address into three formats supported by this script
            for group_size in MAC_FORMAT_RULES.keys():
                mac_grouping = []  # temporary list to store split mac address
                
                if MAC_FORMAT_RULES[group_size]:
                    # split mac address every n-th character based on the mac format key-value pair
                    for idx in range(0, len(address_no_grouping), group_size):
                        mac_grouping.append(address_no_grouping[idx:idx + group_size])
                
                    # join the previously split mac address into a string
                    reformatted_macs.append(f"{MAC_FORMAT_RULES[group_size]}".join(mac_grouping))
                else:
                    # mac address with no groupings
                    reformatted_macs.append(address_no_grouping)
            
            # get the mac address vendor name
            mac_vendor = get_mac_vendor(mac_address=address_no_grouping)
            
            # catch and overwrite few exceptions (broadcast and multicast mac addresses)
            if address_no_grouping == BROADCAST_ADDRESS:
                mac_vendor = "Broadcast MAC address."
            elif address_no_grouping.startswith(MULTICAST_ADDRESS_PREFIX):
                mac_vendor = "Multicast MAC address."
            else:
                pass
    else:
        pass
        
    # return response in json format
    return jsonify({"result": response,
                    "formats": reformatted_macs,
                    "vendor": mac_vendor})  

if __name__ == "__main__":
    app.run(host=HOST, port=PORT)