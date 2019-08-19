#!/usr/bin/python
from ldap import initialize, SERVER_DOWN, INVALID_CREDENTIALS
from os.path import exists
from re import search
from sys import path
path.insert(0, '../lib')
from coreutils import GetConfig


# This class is a series of checks that validates that the config file
# is formatted correctly.  It does not check to see if the values are
# correct; that is handled either by separate tests or during the
# execution of the script itself.
class TestLDAPConfig:
    def __init__(self, file_name):
        self.fl = file_name

    def TestLDAPUrl(self):
        """Tests config for LDAP URL"""
        config = open(self.fl, 'r+b')
        try:
            for line in config:
                lurl = search(r'(^LDAP_URL: )(\S+)$', line)
                if lurl:
                    if lurl.group():
                        lurl_status = 'Pass'
            return lurl_status
        except UnboundLocalError:
            lurl_status = 'Fail'
            return lurl_status
        config.close()

    def TestLDAPPass(self):
        """Tests config for the LDAP Password"""
        config = open(self.fl, 'r+b')
        try:
            for line in config:
                ldap_secret = search(r'(^PASS: )(\S+)', line)
                if ldap_secret:
                    if ldap_secret.group():
                        ldappass_status = 'Pass'
            return ldappass_status
        except UnboundLocalError:
            ldappass_status = 'Fail'
            return ldappass_status
        config.close()

    def TestLDAPBDN(self):
        """Tests config for the LDAP Bind DN"""
        config = open(self.fl, 'r+b')
        try:
            for line in config:
                ldapbdn = search(r'(^BIND_DN: )(.+)', line)
                if ldapbdn:
                    if ldapbdn.group():
                        ldapbdn_status = 'Pass'
            return ldapbdn_status
        except UnboundLocalError:
            ldapbdn_status = 'Fail'
            return ldapbdn_status
        config.close()

    def TestLDAPSDN(self):
        """Tests config for the Search DNs"""
        config = open(self.fl, 'r+b')
        try:
            for line in config:
                ldapsdn = search(r'(^SEARCH_DNS: )(.+)', line)
                if ldapsdn:
                    if ldapsdn.group():
                        ldapsdn_status = 'Pass'
            return ldapsdn_status
        except UnboundLocalError:
            ldapsdn_status = ' Fail'
            return ldapsdn_status
        config.close()

    def TestResultsFile(self):
        """Tests config for results file."""
        config = open(self.fl, 'r+b')
        try:
            for line in config:
                rf = search(r'(^RESULTS_FILE:\s)(.+)', line)
                if rf:
                    if rf.group():
                        results_file_status = 'Pass'
            return results_file_status
        except UnboundLocalError:
            results_file_status = 'Fail'
            return results_file_status
        config.close()


# This fucntion tests the ability to connect to LDAP using the values
# provided in the configuration file.
def TestLDAPConnection(ldap_url, bind_dn, bind_secret):
    test_con = initialize(ldap_url)
    try:
        if test_con.simple_bind_s(bind_dn, bind_secret):
            conn_status = 'Pass'
    except SERVER_DOWN:
        print 'Unable to connect, check server name.'
        conn_status = 'Fail, unable to connect.'
        exit(1)
    except INVALID_CREDENTIALS:
        print 'Unable to connect, bad credentials.'
        conn_status = 'Fail, bad credentials.'
        exit(1)
    return conn_status


# Testing to see if the configuration file exists.  Change the location
# of the configuration to wherever it may reside.  If the file does not
# exist, we raise an exception and exit since future checks would be
# futile.
config_file = '../etc/ldap.cnf'
try:
    if exists(config_file):
        config_status = 'Exists'
    else:
        raise IOError
except IOError:
    print 'ERROR: The config file does not exist.'
    exit(1)
# Checking to see if the configuration file is correclty formatted.
ldap_test_config = TestLDAPConfig(config_file)
LDAP_URL_Status = ldap_test_config.TestLDAPUrl()
LDAP_Pass_Status = ldap_test_config.TestLDAPPass()
LDAP_BDN_Status = ldap_test_config.TestLDAPBDN()
LDAP_SDN_Status = ldap_test_config.TestLDAPSDN()
Results_File_Status = ldap_test_config.TestResultsFile()
# Checking to see if we can connect to LDAP with information provided
# in the configuration file.  We check the results of each check to
# see if any checks fail before making a connection attempt.
config_list = [LDAP_URL_Status, LDAP_Pass_Status, LDAP_BDN_Status,
               LDAP_SDN_Status, Results_File_Status]
if 'Fail' not in config_list:
    ldap_config = GetConfig(config_file)
    l_url = ldap_config.LDAP_URL()
    lbdn = ldap_config.LDAP_BDN()
    lpass = ldap_config.LDAP_Pass()
    LDAP_Conn_Status = TestLDAPConnection(l_url, lbdn, lpass)
    # Providing test output.
    print 'LDAP configs status is: ', config_status
    print 'LDAP URL configuration status is: ', LDAP_URL_Status
    print 'LDAP Password configuration status is: ', LDAP_Pass_Status
    print 'LDAP Bind DN configfuration status is: ', LDAP_BDN_Status
    print 'LDAP Search DN configruation status is: ', LDAP_SDN_Status
    print 'LDAP Results file configuration status is: ', Results_File_Status
    print 'LDAP Connection Status is: ', LDAP_Conn_Status
else:
    print 'LDAP configs status is: ', config_status
    print 'LDAP URL configuration status is: ', LDAP_URL_Status
    print 'LDAP Password configuration status is: ', LDAP_Pass_Status
    print 'LDAP Bind DN configfuration status is: ', LDAP_BDN_Status
    print 'LDAP Search DN configruation status is: ', LDAP_SDN_Status
    print 'LDAP Results file configuration status is: ', Results_File_Status
    print 'Did not make an LDAP connection attempt due to bad config.'
