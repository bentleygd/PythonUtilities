#!/usr/bin/python
from re import search
from ldap import initialize, SCOPE_SUBTREE


class LDAPConfig:
    """Config class for LDAP stuff"""
    def __init__(self, file_name):
        self.fl = file_name

    def LDAP_URL(self):
        """Get the URL of the LDAP server"""
        config = open(self.fl, 'r+b')
        for line in config:
            lurl = search(r'(^LDAP_URL: )(\S+)', line)
            if lurl:
                return lurl.group(2)
        config.close()

    def LDAP_Pass(self):
        """Password for the user connecting to the LDAP server."""
        config = open(self.fl, 'r+b')
        for line in config:
            ldap_secret = search(r'(^PASS: )(\S+)', line)
            if ldap_secret:
                return ldap_secret.group(2)
        config.close()

    def LDAP_BDN(self):
        """Get the LDAP Bind DN."""
        config = open(self.fl, 'r+b')
        for line in config:
            ldapbdn = search(r'(^BIND_DN: )(.+)', line)
            if ldapbdn:
                return ldapbdn.group(2)
        config.close()

    def LDAPSearchDN(self):
        """Get a list of DNs to search through."""
        config = open(self.fl, 'r+b')
        for line in config:
            ldapsdn = search(r'(^SEARCH_DNS: )(.+)', line)
            if ldapsdn:
                search_dn = ldapsdn.group(2).split('|')
                return search_dn
        config.close()

    def ResultsFile(self):
        """File that results are written to."""
        config = open(self.fl, 'r+b')
        for line in config:
            rf = search(r'(^RESULTS_FILE:\s)(.+)', line)
            if rf:
                return rf.group(2)
        config.close()


# Setting script configurations.
my_ldap_config = LDAPConfig('../etc/ldap.cnf')
ldap_url = my_ldap_config.LDAP_URL()
my_ldap = initialize(ldap_url)
ldap_bind_dn = my_ldap_config.LDAP_BDN()
ldap_bind_secret = my_ldap_config.LDAP_Pass()
my_ldap.simple_bind_s(ldap_bind_dn, ldap_bind_secret)
results_file = open(my_ldap_config.ResultsFile(), 'w')

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
for user in user_list:
    results_file.write(user + '\n')
results_file.close()
