# Examination 7 - MariaDB installation

To make a dynamic web site, many use an SQL server to store the data for the web site.

[MariaDB](https://mariadb.org/) is an open-source relational SQL database that is good
to use for our purposes.

We can use a similar strategy as with the _nginx_ web server to install this
software onto the correct host(s). Create the playbook `07-mariadb.yml` with this content:

    ---
    - hosts: db
      become: true
      tasks:
        - name: Ensure MariaDB-server is installed.
          ansible.builtin.package:
            name: mariadb-server
            state: present

# QUESTION A

Make similar changes to this playbook that we did for the _nginx_ server, so that
the `mariadb` service starts automatically at boot, and is started when the playbook
is run.

---
- name: Install and enable MariaDB server
  hosts: dbserver
  become: true
  tasks:
    - name: Ensure MariaDB-server is installed
      ansible.builtin.package:
        name: mariadb-server
        state: present

    - name: Ensure MariaDB service is started and enabled at boot
      ansible.builtin.service:
        name: mariadb
        state: started
        enabled: true

state: started: Starts the MariaDB service (if it isn’t already running).
enabled: true: Ensures MariaDB starts automatically every time the system boots.

# QUESTION B

When you have run the playbook above successfully, how can you verify that the `mariadb`
service is started and is running?

you can use ansible dbserver -a "systemctl status mariadb" and you will get status, or if you can ssh into the server and run sudo systemctl status mariadb.

# BONUS QUESTION

How many different ways can use come up with to verify that the `mariadb` service is running?
