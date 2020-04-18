import requests
import logging
from startup_email import send_email, load_credentials
import sys

creds = load_credentials()

url = "https://wss2.cex.uk.webuy.io/v3/boxes/scpuinti73770/detail"

params={

}

req = requests.get(
    url=url,
    params=params
)

stock = req.json()['response']['data']['boxDetails'][0]['outOfStock']


# set up the logger
logging.basicConfig(
level=logging.INFO,
format= '%(asctime)s %(levelname)s %(message)s ',
handlers=[
    logging.FileHandler(creds["home_path"] + "/debug_cex.log"),
    logging.StreamHandler(sys.stdout)
])
logger = logging.getLogger()


if stock != 1:
    #is in stock now

    try:
        send_email('i7 3770 in stock', "i7 3770 in stock")
        logging.info("email successfully sent")
    except Exception as e:
        logging.warning("email could not be sent..", stack_info=True)
else:
    logger.info(f"stock is {stock}")
