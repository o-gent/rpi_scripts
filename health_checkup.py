"""
send an email once a week to:
- keep gmail active (it stops insecure connections if not used)
- send performance report
"""

from startup_email import send_email


def main():
    """
    Main function
    """
    send_email(
        "",
        "rpi checkup", 
        """ 
        This is a checkup email!
        """
        )


if __name__ == "__main__":
    main()