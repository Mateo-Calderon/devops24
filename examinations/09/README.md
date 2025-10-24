# Examination 9 - Use Ansible Vault for sensitive information

In the previous examination we set a password for the `webappuser`. To keep this password
in plain text in a playbook, or otherwise, is a huge security hole, especially
if we publish it to a public place like GitHub.

There is a way to keep sensitive information encrypted and unlocked at runtime with the
`ansible-vault` tool that comes with Ansible.

https://docs.ansible.com/ansible/latest/vault_guide/index.html

*IMPORTANT*: Keep a copy of the password for _unlocking_ the vault in plain text, so that
I can run the playbook without having to ask you for the password.

# QUESTION A

Make a copy of the playbook from the previous examination, call it `09-mariadb-password.yml`
and modify it so that the task that sets the password is injected via an Ansible variable,
instead of as a plain text string in the playbook.

# QUESTION B

When the [QUESTION A](#question-a) is solved, use `ansible-vault` to store the password in encrypted
form, and make it possible to run the playbook as before, but with the password as an
Ansible Vault secret instead.

Answer:

---
- name: Configure MariaDB with secure password
  hosts: dbserver
  become: true
  vars_files:
    - vault.yml  # this file will contain the encrypted password
  tasks:
    - name: Ensure MariaDB server is installed
      ansible.builtin.package:
        name: mariadb-server
        state: present

    - name: Ensure MariaDB service is started and enabled
      ansible.builtin.service:
        name: mariadb
        state: started
        enabled: true

    - name: Ensure Python MySQL library is installed
      ansible.builtin.package:
        name: python3-PyMySQL
        state: present

    - name: Create a database called webappdb
      community.mysql.mysql_db:
        name: webappdb
        state: present
        login_unix_socket: /var/lib/mysql/mysql.sock

    - name: Create a user for the web application (password stored securely)
      community.mysql.mysql_user:
        name: webappuser
        password: "{{ webapp_db_password }}"
        priv: 'webappdb.*:ALL'
        host: localhost
        state: present
        login_unix_socket: /var/lib/mysql/mysql.sock

Run with ansible-playbook 09-mariadb-password.yml --ask-vault-pass
output:
Vault password: 

PLAY [Configure MariaDB with secure password] ******************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.32]

TASK [Ensure MariaDB server is installed] **********************************************************************************************
ok: [192.168.121.32]

TASK [Ensure MariaDB service is started and enabled] ***********************************************************************************
ok: [192.168.121.32]

TASK [Ensure Python MySQL library is installed] ****************************************************************************************
ok: [192.168.121.32]

TASK [Create a database called webappdb] ***********************************************************************************************
ok: [192.168.121.32]

TASK [Create a user for the web application (password stored securely)] ****************************************************************
[WARNING]: Option column_case_sensitive is not provided. The default is now false, so the column's name will be uppercased. The default
will be changed to true in community.mysql 4.0.0.
ok: [192.168.121.32]

PLAY RECAP *****************************************************************************************************************************
192.168.121.32             : ok=6    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   