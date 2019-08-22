#!/usr/bin/python
from re import search
from ldap import initialize, SCOPE_SUBTREE, SERVER_DOWN, INVALID_CREDENTIALS
from sys import path
path.insert(0, '../lib')
from coreutils import GetConfig, MailSend


# Setting script configurations.
sender = 'ADUserFailure@domain.com'
rcpt = 'team@domain.com'
m_server = 'smtpserver.domain.com'
try:
    my_ldap_config = GetConfig('../etc/ldap.cnf')
except IOError:
    print 'Unable to open configuration file.  Exiting'
    m_msg = ('Unable to open the configuration file needed to make ' +
             'the LDAP connection.  This is a fatal error and the job ' +
             'has been aborted.  Please check for the existence of the ' +
             'configuration and on file permissions.')
    m_subj = 'GetADUsers Failure - Unable to load config'
    MailSend(sender, rcpt, m_server, m_subj, m_msg)
    exit(1)

ldap_url = my_ldap_config.LDAP_URL()
my_ldap = initialize(ldap_url)
ldap_bind_dn = my_ldap_config.LDAP_BDN()
ldap_bind_secret = my_ldap_config.LDAP_Pass()

try:
    my_ldap.simple_bind_s(ldap_bind_dn, ldap_bind_secret)
except SERVER_DOWN:
    print 'Unable to connect to LDAP server due to network issues.'
    m_subj = 'GetADUsers Failure - LDAP Server Down'
    m_msg = ('Unable to connect to the LDAP server due to networking ' +
             'issues.  Please note that the exception indictated that the' +
             ' server is down and this is not related to credentials.')
    MailSend(sender, rcpt, m_server, m_subj, m_msg)
    exit(1)
except INVALID_CREDENTIALS:
    print 'Unable to connect to LDAP server due to bad credentials.'
    m_subj = 'GetADUsers Failure - Bad Credentials'
    m_msg = ('Unable to connect to the LDAP server due to bad credentials')
    MailSend(sender, rcpt, m_server, m_subj, m_msg)
    exit(1)

try:
    results_file = open(my_ldap_config.ResultsFile(), 'w')
except IOError:
    print 'Unable to open results file.  Exiting'
    m_msg = ('Unable to write to the results file.  This is most likely a' +
             ' permissions issue.')
    m_subj = 'GetADUsers Failure - Unable to write results.'
    MailSend(sender, rcpt, m_server, m_subj, m_msg)
    exit(1)

# Getting users and storing them in a list, and writing that list to a
# file.  Note that the search uses SCOPE_SUBTREE, so the search will
# also run through any sub level OUs.  We are only obtaining the
# SAM Account name value (i.e, the user name).
user_list = []
for dn in my_ldap_config.LDAPSearchDN():
    user_data = (my_ldap.search_s(dn, SCOPE_SUBTREE,
                 'sAMAccountName=*', ['sAMAccountName'], attrsonly=0))
    for data in user_data:
        user_list.append(data[1].get('sAMAccountName')[0].lower())

# Sorting the list due to OCD.
user_list.sort()
# Iterating through the user list and writing the user names to a file.
if len(user_list) > 100:
    for user in user_list:
        results_file.write(user + '\n')
    results_file.close()
else:
    m_msg = 'Determine if searched OUs are valid'
    m_subj = 'GetADUsers Warning - Low User Count.'
    MailSend(sender, rcpt, m_server, m_subj, m_msg)
    for user in user_list:
        results_file.write(user + '\n')
    results_file.close()
