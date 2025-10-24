# Examination 12 - Roles

So far we have been using separate playbooks and ran them whenever we wanted to make
a specific change.

With Ansible [roles](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_reuse_roles.html) we
have the capability to organize tasks into sets, which are called roles.

These roles can then be used in a single playbook to perform the right tasks on each host.

Consider a playbook that looks like this:

    ---
    - name: Configure the web server(s) according to specs
      hosts: web
      roles:
        - webserver

    - name: Configure the database server(s) according to specs
      hosts: db
      roles:
        - dbserver

This playbook has two _plays_, each play utilizing a _role_.

This playbook is also included in this directory as [site.yml](site.yml).

Study the Ansible documentation about roles, and then start work on [QUESTION A](#question-a).

# QUESTION A

Considering the playbook above, create a role structure in your Ansible working directory
that implements the previous examinations as two separate roles; one for `webserver`
and one for `dbserver`.

Copy the `site.yml` playbook to be called `12-roles.yml`.

HINT: You can use

    $ ansible-galaxy role init [name]

to create a skeleton for a role. You won't need ALL the directories created by this,
but it gives you a starting point to fill out in case you don't want to start from scratch.

❯ ansible-playbook -i host 12-roles.yml --ask-vault-pass

Vault password: 

PLAY [Configure the web server(s) according to specs] **************************

TASK [Gathering Facts] *********************************************************
ok: [192.168.121.148]

TASK [webserver : Ensure nginx is installed] ***********************************
ok: [192.168.121.148]

TASK [webserver : Ensure nginx is started at boot] *****************************
ok: [192.168.121.148]

TASK [webserver : Copy HTTPS configuration file] *******************************
ok: [192.168.121.148]

TASK [webserver : Ensure the nginx configuration is updated for example.internal] ***
changed: [192.168.121.148]

TASK [webserver : Create web root directory] ***********************************
ok: [192.168.121.148]

TASK [webserver : Upload index.html] *******************************************
ok: [192.168.121.148]

TASK [webserver : Restart nginx only if configuration changed] *****************
changed: [192.168.121.148]

TASK [webserver : Ensure web root exists] **************************************
ok: [192.168.121.148]

TASK [webserver : Upload templated nginx configuration] ************************
changed: [192.168.121.148]

PLAY [Configure the database server(s) according to specs] *********************

TASK [Gathering Facts] *********************************************************
ok: [192.168.121.32]

TASK [dbserver : Ensure MariaDB-server is installed] ***************************
ok: [192.168.121.32]

TASK [dbserver : Ensure MariaDB service is started and enabled at boot] ********
ok: [192.168.121.32]

TASK [dbserver : Ensure Python MySQL library is installed] *********************
ok: [192.168.121.32]

TASK [dbserver : Create a database called webappdb] ****************************
ok: [192.168.121.32]

TASK [dbserver : Create a user for the web application (password stored securely)] ***
[WARNING]: Option column_case_sensitive is not provided. The default is now
false, so the column's name will be uppercased. The default will be changed to
true in community.mysql 4.0.0.
ok: [192.168.121.32]

PLAY RECAP *********************************************************************
192.168.121.148            : ok=10   changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.121.32             : ok=6    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
