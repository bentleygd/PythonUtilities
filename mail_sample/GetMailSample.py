#!/usr/bin/python
from ldap import initialize, SCOPE_SUBTREE
from random import sample
from csv import DictWriter
from sys import path
path.insert(0, ~/PythonUtilities/lib)
import coreutils


def GetADMailUsers(ldap_url, bind_dn, passw, ous):
    """Retrieves email addresses from AD."""
    mail_list = []
    ldap_obj = initialize(ldap_url)
    ldap_obj.simple_bind_s(bind_dn, passw)
    for ou in ous:
        user_data = (ldap_obj.search_s(ou, SCOPE_SUBTREE, 'mail=*',
                     ['givenName', 'sn', 'mail', 'department'], attrsonly=0))
        for data in user_data:
            mail_list.append(data[1])
    return mail_list


def GetMailSample(population):
    """Returns a 10% sample of users with email address."""
    pop_size = len(population)
    sample_size = int(round(pop_size / 10))
    sample_list = sample(population, sample_size)
    return sample_list


# Setting configuration file.
ml_smpl_cnf = coreutils.GetConfig('mail-sample.cnf')
# Getting GnuPG info
gpghome = ml_smpl_cnf.GPGHome()
gpg_pass = str(open(ml_smpl_cnf.GPGPass(), 'r').read()).strip('\n')

# Setting LDAP Info
l_url = ml_smpl_cnf.LDAP_URL()
l_bdn = ml_smpl_cnf.LDAP_BDN()
l_pass = str(coreutils.DecryptGPG(ml_smpl_cnf.LDAP_Pass(), gpghome, gpg_pass)
             ).strip('\n')
l_ous = ml_smpl_cnf.LDAPSearchOU()

# Getting user data
mail_users = GetADMailUsers(l_url, l_bdn, l_pass, l_ous)
mail_sample = GetMailSample(mail_users)

# Writing data to a CSV file
results_file = ml_smpl_cnf.ResultsFile()
csv_file = open(results_file, 'w+b')
f_names = ['First Name', 'Last Name', 'email', 'Department', 'Region']
writer = DictWriter(csv_file, fieldnames=f_names, dialect='excel')
writer.writeheader()
for user in mail_sample:
    user = dict(user)
    writer.writerow({'First Name': user.get('givenName')[0],
                     'Last Name': user.get('sn')[0],
                     'email': user.get('mail')[0],
                     'Department': user.get('department')[0]})
csv_file.close()
