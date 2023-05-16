import re
from flask import Flask, jsonify

MAC_ADDRESS_BIT_LENGTH = 48  # mac addresses consist of 48 bits

app = Flask(__name__)  # initialize flask

@app.route('/verify-mac-address/<address>', methods=["GET"])
def verify_mac_address(address):
    
    # remove group separators (dot, semicolon, dash, etc)
    address_no_grouping = re.sub('[.:]', "", address)  # substitute can be easily updated

    # convert string into a hex format
    address_base16 = int(address_no_grouping, 16)
    
    response = "OK"
    if not address_base16.bit_length() <= MAC_ADDRESS_BIT_LENGTH:
        response = "NOK"
    
    # return response in json format
    return jsonify({"result": response})  

if __name__ == "__main__":
    app.run()