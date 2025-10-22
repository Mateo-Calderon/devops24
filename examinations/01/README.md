# Examination 1 - Understanding SSH and public key authentication

Connect to one of the virtual lab machines through SSH, i.e.

    $ ssh -i deploy_key -l deploy webserver

Study the `.ssh` folder in the home directory of the `deploy` user:

    $ ls -ld ~/.ssh

Look at the contents of the `~/.ssh` directory:

    $ ls -la ~/.ssh/

## QUESTION A

What are the permissions of the `~/.ssh` directory?

Why are the permissions set in such a way?

## QUESTION B

What does the file `~/.ssh/authorized_keys` contain?

## QUESTION C

When logged into one of the VMs, how can you connect to the
other VM without a password?

### Hints:

* man ssh-keygen(1)
* ssh-copy-id(1) or use a text editor

## BONUS QUESTION

Can you run a command on a remote host via SSH? How?


Uppgift

gato@gato-Precision-T1650:~/devops24/devops24/lab_environment$ ssh -i deploy_key -l deploy lab_environment_webserver
ssh: Could not resolve hostname lab_environment_webserver: Name or service not known
gato@gato-Precision-T1650:~/devops24/devops24/lab_environment$ ssh -i deploy_key -l deploy lab_environment_dbserver
ssh: Could not resolve hostname lab_environment_dbserver: Name or service not known
gato@gato-Precision-T1650:~/devops24/devops24/lab_environment$ sudo virsh net-dhcp-leases vagrant-libvirt 
[sudo] lösenord för gato: 
 Expiry Time           MAC address         Protocol   IP address           Hostname    Client ID or DUID
-------------------------------------------------------------------------------------------------------------
 2025-10-16 11:32:30   52:54:00:14:b7:b4   ipv4       192.168.121.148/24   webserver   01:52:54:00:14:b7:b4
 2025-10-16 11:32:31   52:54:00:69:ac:48   ipv4       192.168.121.32/24    dbserver    01:52:54:00:69:ac:48

gato@gato-Precision-T1650:~/devops24/devops24/lab_environment$ ssh -i deploy_key -l deploy 192.168.121.148/24
ssh: Could not resolve hostname 192.168.121.148/24: Name or service not known
gato@gato-Precision-T1650:~/devops24/devops24/lab_environment$ ssh -i deploy_key -l deploy 192.168.121.148
The authenticity of host '192.168.121.148 (192.168.121.148)' can't be established.
ED25519 key fingerprint is SHA256:CrZjOYfplKroFmioQGGAG3MkEgbIPqUjv+FqunI7b2s.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes 
Warning: Permanently added '192.168.121.148' (ED25519) to the list of known hosts.
[deploy@webserver ~]$ 



## QUESTION A

What are the permissions of the `~/.ssh` directory?
~/.ssh is typically 700 (owner-only access).

Why are the permissions set in such a way?
This protects sensitive SSH keys and configuration files.
Ensures only the owner can read/write/execute within the directory.
Prevents security risks from unauthorized access by other users

## QUESTION B

What does the file `~/.ssh/authorized_keys` contain?
The file ~/.ssh/authorized_keys contains public SSH keys of users or computers that are allowed to log in to the account without using a password.

## QUESTION C

When logged into one of the VMs, how can you connect to the
other VM without a password?

You can connect to the other VM without a password by using SSH key-based authentication.

