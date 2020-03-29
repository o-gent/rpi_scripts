"""
A script for checking if an IP address has changed, if it has send an email with the new address
"""

# STEP 1: Check if address.txt exist
# If it does: 
#       Read it
#       Check against current IP
#       IF new_IP = old_IP:
#           don't send email.
#       ELSE:
#           Update line with new IP
#           Send email
# ELSE:
#       Create file and write new IP to file

import sys
import urllib.request
import smtplib, ssl
import logging
import json
import os


__author__ = ("github.com/o-gent")


def check_in() -> str:
    """ Fetches public IP address """
    ip = urllib.request.urlopen('https://api.ipify.org').read().decode()
    logging.info(ip)
    return ip


def load_credentials(file_name: str = "credentials.json") -> dict:
    """
    Get email credentials from credentials.json
    """
    # try to load existing credentials
    if os.path.isfile(file_name):
        with open(file_name, "r") as f:
            creds = json.load(f)
            return creds

    # else make a new json
    else:
        blank = {"port": 0, "smtp_server": "", "sender_email": "", "receiver_email": "", "password": "", "toaddr": "", "cc": "", "fromaddr": "", "home_path": ""}
        with open(file_name, "w") as f:
            json.dump(blank, f)
            raise FileNotFoundError("Need to have a credentials file!")


def send_email(ip_address: str, subject: str, content: str= "") -> None:
    # fetch user information
    creds = load_credentials()

    # email meta
    message = "From: {}\r\n".format(creds["fromaddr"])
    message += "To: {}\r\n".format(creds["toaddr"])
    message += "CC: {}\r\n".format(creds["cc"])
    message += "Subject: {}\r\n".format(subject)
    message += "\r\n"
    
    if content == "":
        # Email body
        message += """ 
        Hello,

        The IP address has changed again.

        it's {}
        """.format(ip_address)
    else:
        # use the function call vaiable
        message += content

    # Send the email
    context = ssl.create_default_context()
    with smtplib.SMTP(creds["smtp_server"], int( creds["port"] ) ) as server:
        server.starttls(context=context)
        server.login(creds["sender_email"], creds["password"])
        server.sendmail(creds["sender_email"], creds["receiver_email"], message)


if __name__ == "__main__":
    # get user credentials 
    creds = load_credentials()

    # set up the logger
    logging.basicConfig(
    level=logging.INFO,
    format= '%(asctime)s %(levelname)s %(message)s ',
    handlers=[
        logging.FileHandler(creds["home_path"] + "/debug.log"),
        logging.StreamHandler(sys.stdout)
    ])
    logger = logging.getLogger()

    # Get current public IP address
    try:
        ip_address = check_in()
    except:
        logging.warning("IP address could not be read")
        raise
    
    # Compare to the previous IP address
    with open(creds["home_path"] + "/address.txt", "r+") as f:
        try: 
            current = f.readlines()[0]
            logging.info("Recorded ip is " + current)
        except:
            logging.warning("file couldn't be read", stack_info= True)
            current = ""

        if ip_address == current:
            logging.info("IP address has not changed")
            sys.exit()
        else:
            logging.info("IP address has changed, send email")
            f.seek(0,0)
            f.truncate()
            f.write(ip_address)

            try:
                send_email(ip_address, "VPN IP address changed")
                logging.info("email successfully sent")
            except Exception as e:
                logging.warning("email could not be sent..", stack_info=True)
