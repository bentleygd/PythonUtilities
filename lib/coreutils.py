from email.mime.text import MIMEText
from socket import gethostbyname
from re import search
from gnupg import GPG
from smtplib import SMTP


# The below object is a configuration object that can be modified to
# suit your needs.  Simply change the functions to whatever would be
# appropriate for your script as well as the RegEx.
class GetConfig:
    """A configuration class"""
    def __init__(self, file_location):
        self.fl = file_location

    def GPGHome(self):
        """Gets gpg's home dir from config file."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            gpg_rgx = search(r'(^GNUPGHOME = )(.+)', line)
            if gpg_rgx:
                return gpg_rgx.group(2).strip()
        config_file.close()

    def GPGPass(self):
        """Gets the location of the gpg password."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            gpg_pass_rgx = search(r'(^GPGPASS = )(.+)', line)
            if gpg_pass_rgx:
                return gpg_pass_rgx.group(2).strip()
        config_file.close()

    def LDAP_BDN(self):
        """Gets an LDAP Bind DN from the config file."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            bdn_rgx = search(r'(^LDAP_BDN: )(.+)', line)
            if bdn_rgx:
                return bdn_rgx.group(2).strip()
        config_file.close()

    def LDAP_URL(self):
        """Gets the LDAP URL to connect to."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            lurl_rgx = search(r'(^LDAP_URL: )(.+)', line)
            if lurl_rgx:
                return lurl_rgx.group(2).strip()
        config_file.close()

    def LDAP_Pass(self):
        """Gets the password for an LDAP connection."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            pass_rgx = search(r'(^PASS_FILE: )(.+)', line)
            if pass_rgx:
                return pass_rgx.group(2).strip()
        config_file.close()

    def LDAPSearchOU(self):
        """Gets a list of OUs to search through."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            ou_rgx = search(r'(^SEARCH_OUs: )(.+)', line)
            if ou_rgx:
                search_ou = ou_rgx.group(2).split('|')
                return search_ou
        config_file.close()

    def ResultsFile(self):
        """Gets the location of the results file."""
        config_file = open(self.fl, 'r+b')
        for line in config_file:
            rf_rgx = search(r'(RESULTS_CSV: )(.+)', line)
            if rf_rgx:
                results_file = rf_rgx.group(2)
                return results_file
        config_file.close()


def MailSend(mail_sender, mail_recipients, mail_server, mail_body):
    """Simple function to send mail."""
    # Defining mail properties.
    msg = MIMEText(mail_body)
    msg['Subject'] = 'MSFT IP Scrape'
    msg['From'] = mail_sender
    msg['To'] = mail_recipients
    # Obtaining IP address of SMTP server host name.  If using an IP
    # address, omit the gethostbyname function.
    s = SMTP(gethostbyname(mail_server), '25')
    # Sending the mail.
    s = SMTP(gethostbyname(mail_server), '25')
    s.sendmail(mail_sender, mail_recipients, msg.as_string())


def DecryptGPG(cipher_file, gpghome, p_phrase):
    """Simple decrypt."""
    # Specifying where the encrypted data is.
    cipher_data = str(open(cipher_file, 'r').read()).strip('\n')
    # Initializing GPG.
    g = GPG(gnupghome=gpghome)
    # Decrypting the cipher text to clear text.
    cipher_data = str(open(cipher_file, 'r').read()).strip('\n')
    g = GPG(gnupghome=gpghome)
    clear_data = g.decrypt(cipher_data, passphrase=p_phrase)
    return clear_data
