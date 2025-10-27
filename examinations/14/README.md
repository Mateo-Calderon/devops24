# Examination 14 - Firewalls (VG)

The IT security team has noticed that we do not have any firewalls enabled on the servers,
and thus ITSEC surmises that the servers are vulnerable to intruders and malware.

As a first step to appeasing them, we will install and enable `firewalld` and
enable the services needed for connecting to the web server(s) and the database server(s).

# QUESTION A

Create a playbook `14-firewall.yml` that utilizes the [ansible.posix.firewalld](https://docs.ansible.com/ansible/latest/collections/ansible/posix/firewalld_module.html) module to enable the following services in firewalld:

* On the webserver(s), `http` and `https`
* On the database servers(s), the `mysql`

You will need to install `firewalld` and `python3-firewall`, and you will need to enable
the `firewalld` service and have it running on all servers.

When the playbook is run, you should be able to do the following on each of the
servers:

## dbserver

    [deploy@dbserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="mysql"/>
    <forward/>
    </zone>

## webserver

    [deploy@webserver ~]$ sudo cat /etc/firewalld/zones/public.xml
    <?xml version="1.0" encoding="utf-8"?>
    <zone>
      <short>Public</short>
      <description>For use in public areas. You do not trust the other computers on networks to not harm your computer. Only selected incoming connections are accepted.</description>
      <service name="ssh"/>
      <service name="dhcpv6-client"/>
      <service name="cockpit"/>
      <service name="https"/>
      <service name="http"/>
      <forward/>
    </zone>

# Resources and Documentation

https://firewalld.org/

---
- name: Configure firewall on webserver
  hosts: webserver
  become: true
  tasks:

    # Install necessary packages
    - name: Install firewalld and python3-firewall
      ansible.builtin.package:
        name:
          - firewalld
          - python3-firewall
        state: present

    # Ensure firewalld is running and enabled
    - name: Enable and start firewalld
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true

    - name: Allow HTTP service
      ansible.posix.firewalld:
        service: http
        permanent: true
        state: enabled
        immediate: true

    - name: Allow HTTPS service
      ansible.posix.firewalld:
        service: https
        permanent: true
        state: enabled
        immediate: true

- name: Configure firewall on dbserver
  hosts: dbserver
  become: true
  tasks:

    # Install necessary packages
    - name: Install firewalld and python3-firewall
      ansible.builtin.package:
        name:
          - firewalld
          - python3-firewall
        state: present

    # Ensure firewalld is running and enabled
    - name: Enable and start firewalld
      ansible.builtin.service:
        name: firewalld
        state: started
        enabled: true

    - name: Allow MySQL service
      ansible.posix.firewalld:
        service: mysql
        permanent: true
        state: enabled
        immediate: true

------------------------------------------------------------------------------------
❯ ansible-playbook 14-firewall.yml

PLAY [Configure firewall on webserver] *****************************************

TASK [Gathering Facts] *********************************************************
ok: [192.168.121.148]

TASK [Install firewalld and python3-firewall] **********************************
changed: [192.168.121.148]

TASK [Enable and start firewalld] **********************************************
changed: [192.168.121.148]

TASK [Allow HTTP service] ******************************************************
changed: [192.168.121.148]

TASK [Allow HTTPS service] *****************************************************
changed: [192.168.121.148]

PLAY [Configure firewall on dbserver] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [192.168.121.32]

TASK [Install firewalld and python3-firewall] **********************************
changed: [192.168.121.32]

TASK [Enable and start firewalld] **********************************************
changed: [192.168.121.32]

TASK [Allow MySQL service] *****************************************************
changed: [192.168.121.32]

PLAY RECAP *********************************************************************
192.168.121.148            : ok=5    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
192.168.121.32             : ok=4    changed=3    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 