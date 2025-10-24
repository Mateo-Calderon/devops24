# Examination 8 - MariaDB configuration

MariaDB and MySQL have the same origin (MariaDB is a fork of MySQL, because of... Oracle...
it's a long story.) They both work the same way, which makes it possible to use Ansible
collections that handle `mysql` to work with `mariadb`.

To be able to manage MariaDB/MySQL through the `community.mysql` collection, you also
need to make sure the requirements for the collections are installed on the database VM.

See https://docs.ansible.com/ansible/latest/collections/community/mysql/mysql_db_module.html#ansible-collections-community-mysql-mysql-db-module-requirements

HINT: In AlmaLinux, the correct package to install on the VM host is called `python3-PyMySQL`.

# QUESTION A

Copy the playbook from examination 7 to `08-mariadb-config.yml`.

Use the `community.mysql` module in this playbook so that it also creates a database instance
called `webappdb` and a database user called `webappuser`.

Make the `webappuser` have the password "secretpassword" to access the database.

HINT: The `community.mysql` collection modules has many different ways to authenticate
users to the MariaDB/MySQL instance. Since we've just installed `mariadb` without setting
any root password, or securing the server in other ways, we can use the UNIX socket
to authenticate as root:

* The socket is located in `/var/lib/mysql/mysql.sock`
* Since we're authenticating through a socket, we should ignore the requirement for a `~/.my.cnf` file.
* For simplicity's sake, let's grant `ALL` privileges on `webapp.*` to `webappuser`

# Documentation and Examples
https://docs.ansible.com/ansible/latest/collections/community/mysql/index.html

---
- name: Configure MariaDB with database and user
  hosts: dbserver
  become: true
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

    - name: Create a user for the web application
      community.mysql.mysql_user:
        name: webappuser
        password: secretpassword
        priv: 'webappdb.*:ALL'
        host: localhost
        state: present
        login_unix_socket: /var/lib/mysql/mysql.sock


------------------------------------------------------------------------------------------------
❯ ansible-playbook 08-mariadb-config.yml

PLAY [Configure MariaDB with database and user] *******************************************************

TASK [Gathering Facts] ********************************************************************************
ok: [192.168.121.32]

TASK [Ensure MariaDB server is installed] *************************************************************
ok: [192.168.121.32]

TASK [Ensure MariaDB service is started and enabled] **************************************************
ok: [192.168.121.32]

TASK [Ensure Python MySQL library is installed] *******************************************************
changed: [192.168.121.32]

TASK [Create a database called webappdb] **************************************************************
changed: [192.168.121.32]

TASK [Create a user for the web application] **********************************************************
[WARNING]: Option column_case_sensitive is not provided. The default is now false, so the column's
name will be uppercased. The default will be changed to true in community.mysql 4.0.0.
changed: [192.168.121.32]

PLAY RECAP ********************************************************************************************
192.168.121.32             : ok=6    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0