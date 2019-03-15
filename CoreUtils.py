from email.mime.text import MIMEText
import smtpblib
import logging


def MailSend():
    """Simple function to send mail."""
    sender = 'sender@domain.com'
    recipients = 'recipients@domain.com'
    mail_body = ('String of varying length to serve as the body of the email')
    msg = MIMEText(mail_body)
    msg['Subject'] = 'Example subject'
    msg['From'] = sender
    msg['To'] = recipients
    s = smtplib.SMTP(gethostbyname('smtpserver.domain.com'), '25')
    s.sendmail(sender, recipients, msg.as_string())
    s.quit


def SysLogSetup():
    """Function to be used to set up simple syslog logging."""
    syslogme = logging.GetLogger('SysLogger')
    syslogme.setLevel(logging.DEBUG)

    # Setting up a syslog handler.  Change the log level and facility
    # if desired.
    sl = logging.SysLogHandler()
    sl.setLevel(logging.INFO)

    # Creating a log formatter.
    sl_format = logging.Formatter('%(asctime)s - %(processName)s - 
                                   %(levelname)s - %(message)s', 
                                  datefmt='%m/%d/%Y %I:%M:%S %p')
    sl.setFormatter(sl_format)
    syslogme.addHandler(sl)


def FileLogSetup():
    """Function to be used to set up simple logging to a file."""
    filelogme = logging.GetLogger('FileLogger')
    filelogme.setLevel(loogging.DEBUG)

    # Setting up a rotating file log handler.
    rfh = logging.RotatingFileHandler('/somelogname', maxBytes=52428800,
                                      backupCount=5)
    rfh.setLevel(logging.DEBUG)
    rfh_format = logging.Formatter('%(asctime)s - %(processName)s - 
                                   %(levelname)s - %(message)s', exc_info,
                                   datefmt='%m/%d/%Y %I:%M:%S %p')
    rfh.setFormatter(rfh_format)
    filelogme.addHandler(rfh)
