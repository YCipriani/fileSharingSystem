import smtplib
from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.carrier.asyncore.dgram import udp
from pysnmp.entity.rfc3413 import ntfrcv
from filesharing.common.logger import get_logger
from filesharing.utils.current_time import get_current_date_and_time
import syslog
from pysnmp.hlapi import *


def send_email(
        request_type: str, file_name: str, file_location: str, send_to_email: str
):
    log = get_logger()
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
        log.info(get_current_date_and_time() + "Email successfully sent!")
    except:
        log.error(get_current_date_and_time() + "Something went wrong. Email not sent")


def log_syslog(message, info):
    if info:
        syslog.syslog(syslog.LOG_INFO, message)
    else:
        syslog.syslog(syslog.LOG_ERR, message)


def cbFun(snmpEngine, stateReference, contextEngineId, contextName,
          varBinds, cbCtx):
    print("Received new Trap message");
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))


def start_snmp_trap_receiver():
    snmpEngine = engine.SnmpEngine()

    TrapAgentAddress = '192.168.1.14'  # Trap listener address
    Port = 163  # trap listener port

    print("Agent is listening SNMP Trap on " + TrapAgentAddress + " , Port : " + str(Port))
    print('--------------------------------------------------------------------------')
    config.addTransport(
        snmpEngine,
        udp.domainName + (1,),
        udp.UdpTransport().openServerMode(('0.0.0.0', Port))
    )

    # Configure community here
    config.addV1System(snmpEngine, 'my-area', 'public')
    ntfrcv.NotificationReceiver(snmpEngine, cbFun)

    snmpEngine.transportDispatcher.jobStarted(1)

    try:
        snmpEngine.transportDispatcher.runDispatcher()
    except:
        snmpEngine.transportDispatcher.closeDispatcher()
        raise


def send_snmp_trap(message):
    next(sendNotification(SnmpEngine(),
                          CommunityData('public'),
                          UdpTransportTarget(('192.168.1.14', 163)),
                          ContextData(),
                          'trap',
                          # sequence of custom OID-value pairs
                          [ObjectType(ObjectIdentity('1.3.6.1.2.1.1.1.0'), OctetString(message))]))
