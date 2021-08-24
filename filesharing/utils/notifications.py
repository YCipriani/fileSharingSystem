import smtplib
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from filesharing.common.logger import get_logger
from filesharing.utils.current_time import get_current_date_and_time
import syslog
from pysnmp.hlapi import *

log = get_logger()


def create_email_body(my_request, start):
    if my_request.request_type=="Tx":
        if start:
            return (
                "Dear Sir/Madam, \n\n"
                + "A "
                + my_request.request_type
                + " request has been initiated for the file: "
                + my_request.file_name_and_extension
                + " to be stored in table/collection "
                + my_request.file_location
                + ".\n\n"
            )
        else:
            return (
                "Dear Sir/Madam, \n\n"
                + "The "
                + my_request.request_type
                + " request has been processed. File "
                + my_request.file_name_and_extension
                + " has been stored in table/collection "
                + my_request.file_location
                + ".\n\n"
            )
    else:
        if start:
            return (
                "Dear Sir/Madam, \n\n"
                + "A "
                + my_request.request_type
                + " request has been initiated for the file: "
                + my_request.file_name_and_extension
                + " which will be checked if it exists in collection "
                + my_request.file_location
                + ".\n\n"
            )
        else:
            return (
                "Dear Sir/Madam, \n\n"
                + "The "
                + my_request.request_type
                + " request has been processed. File "
                + my_request.file_name_and_extension
                + " has been verified in table/collection "
                + my_request.file_location
                + ".\n\n"
            )


def send_email(my_request, send_to_email: str, start: bool):
    gmail_user = "1thesoftwareengineer1@gmail.com"
    gmail_password = "1developer1"

    sent_from = gmail_user
    to = [send_to_email]
    if start:
        body = create_email_body(my_request, True)
        subject = (
            my_request.request_type
            + ": "
            + my_request.file_name_and_extension
            + " is being processed"
        )
    else:
        body = create_email_body(my_request, False)
        subject = my_request.request_type + " request has completed"
    message = "Subject: {}\n\n{}".format(subject, body)

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()
        log.info(get_current_date_and_time() + "Email successfully sent!")
    except:
        log.error(get_current_date_and_time() + "Something went wrong. Email not sent")


def log_syslog(message, info=True):
    if info:
        syslog.syslog(syslog.LOG_INFO, message)
    else:
        syslog.syslog(syslog.LOG_ERR, message)


def cbFun(snmpEngine, stateReference, contextEngineId, contextName, varBinds, cbCtx):
    log.info(get_current_date_and_time() + "Received new Trap message")
    for name, val in varBinds:
        log.info("%s = %s" % (name.prettyPrint(), val.prettyPrint()))


def start_snmp_trap_receiver():
    snmpEngine = engine.SnmpEngine()

    TrapAgentAddress = "192.168.1.14"  # Trap listener address
    port = 163  # trap listener port

    log.info(
        get_current_date_and_time()
        + "Agent is listening SNMP Trap on "
        + TrapAgentAddress
        + " , Port : "
        + str(port)
    )
    log.info(
        "--------------------------------------------------------------------------"
    )
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode(("0.0.0.0", port)),
    )

    # Configure community here
    config.addV1System(snmpEngine, "my-area", "public")
    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1)

    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise


def send_snmp_trap(message):
    log.info(get_current_date_and_time() + "New Trap message Sent")
    next(
        sendNotification(
            SnmpEngine(),
            CommunityData("public"),
            UdpTransportTarget(("192.168.1.14", 163)),
            ContextData(),
            "trap",
            [ObjectType(ObjectIdentity("1.3.6.1.2.1.1.1.0"), OctetString(message))],
        )
    )
