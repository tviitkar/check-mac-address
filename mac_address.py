import re
import requests
from flask import Flask, jsonify

# todo - could move these two separate configuration file
SYMBOLS_TO_REMOVE = "[.:]"  # easy to update, for example add dash (-)
MAC_ADDRESS_BIT_LENGTH = 48  # mac addresses consist of 48 bits
MAC_FORMATS = {0: None, 2: ":", 4: "."}  # key represents group size, value represents group separator


app = Flask(__name__)  # initialize flask

@app.route('/verify-mac-address/<address>', methods=["GET"])
def verify_mac_address(address):
    reformatted_macs = []  # list for reformatted mac addresses
    mac_vendor = ""
    
    # remove group separators (dot, semicolon, dash, etc)
    address_no_grouping = re.sub(SYMBOLS_TO_REMOVE, "", address)  # substitute can be easily updated

    response = "NOK"  # default assumption is that input value is invalid
    if len(address_no_grouping) == 12:  # mac addresses are 12 character in length

        # convert string into a hex format
        address_base16 = int(address_no_grouping, 16)  # todo: catch error!
    
        # todo: reserved and/or special case mac addresses (e.g. broadcast)
        if address_base16.bit_length() <= MAC_ADDRESS_BIT_LENGTH:
            response = "OK"
        
            for group_size in MAC_FORMATS.keys():
                mac_grouping = []  # temporary list to store mac split mac address
                
                if MAC_FORMATS[group_size]:
                    # split mac address every n-th character based on the mac format key-value pair
                
                    for idx in range(0, len(address_no_grouping), group_size):
                        mac_grouping.append(address_no_grouping[idx:idx + group_size])
                
                    # join the previously split mac address list into a string
                    reformatted_macs.append(f"{MAC_FORMATS[group_size]}".join(mac_grouping))
                else:
                    # one mac address doesn't need any formatting
                    reformatted_macs.append(address_no_grouping)
            
            # api call to get vendor
            # todo: idea - create a separate function and instead call it here (?)
            api_call_response = requests.get(f"https://api.macvendors.com/{address_no_grouping}")
            if api_call_response.status_code == 200:
                mac_vendor = api_call_response.text
            else:
                mac_vendor = "Not found"
    else:
        pass
        
    # return response in json format
    return jsonify({"result": response,
                    "formats": reformatted_macs,
                    "vendor": mac_vendor})  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)