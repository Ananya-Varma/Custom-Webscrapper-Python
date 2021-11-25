from flask import Flask
from flask import request
from utils import *

app = Flask(__name__)

DIN_URL = "https://www.mca.gov.in/mcafoportal/showEnquireDIN.do"
SRN_URL = "https://www.mca.gov.in/mcafoportal/trackPaymentStatus.do"

# def main():
#     get_din_details("https://www.mca.gov.in/mcafoportal/showEnquireDIN.do", "08479774", "enquireDIN_0")
#     get_srn_details("https://www.mca.gov.in/mcafoportal/trackPaymentStatus.do", "T38324786", "trackPaymentStatus_0",
#                     "srnDetailsTab1", "srnDetailsTab2")


@app.route('/details/din', methods=['GET'])
def retrieve_din():
    din_number = request.args.get("din_number")
    return get_din_details(DIN_URL, din_number, "enquireDIN_0")


@app.route('/details/srn', methods=['GET'])
def retrieve_srn():
    srn_number = request.args.get("srn_number")
    return get_srn_details(SRN_URL, srn_number, "trackPaymentStatus_0",
                    "srnDetailsTab1", "srnDetailsTab2")


if __name__ == "__main__":
    app.run()