import smtplib
from filesharing.common.logger import get_logger


def send_email(
    request_type: str, file_name: str, file_location: str, send_to_email: str
):
    gmail_user = "1thesoftwareengineer1@gmail.com"
    gmail_password = "1developer1"

    sent_from = gmail_user
    to = [send_to_email]
    subject = request_type + ": " + file_name + " is being processed"
    body = (
        "Dear Sir/Madam, \n\n"
        + "A "
        + request_type
        + " request has been initiated for the file: "
        + file_name
        + " to be stored in "
        + file_location
        + " table/collection.\n\n"
    )
    message = "Subject: {}\n\n{}".format(subject, body)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()
        # log.info('Email successfully sent!')
    except:
        # log.error('ERROR: Something went wrong. Email not sent')
        print("email not sent")
