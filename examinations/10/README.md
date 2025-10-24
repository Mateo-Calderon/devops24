# Examination 10 - Templating

With the installation of the web server earlier in Examination 6, we set up
the `nginx` web server with a static configuration file that listened to all
interfaces on the (virtual) machine.

What we really want is for the webserver to _only_ listen to the external
interface, i.e. the interface with the IP address that we connect to the machine to.

Of course, we can statically enter the IP address into the file and upload it,
but if the IP address of the machine changes, we have to do it again, and if the
playbook is meant to be run against many different web servers, we have to be able
to do this manually.

Make a directory called `templates/` and put the `nginx` configuration file from Examination 6
into that directory, and call it `example.internal.conf.j2`.

If you look at the `nginx` documentation, note that you don't have to enable any IPv6 interfaces
on the web server. Stick to IPv4 for now.

# QUESTION A

Copy the finished playbook from Examination 6 (`06-web.yml`) and call it `10-web-template.yml`.

Make the static configuration file we used earlier into a Jinja template file,
and set the values for the `listen` parameters to include the external IP
address of the virtual machine itself.

Use the `ansible.builtin.template` module to accomplish this task.

---
- name: Configure webserver using template
  hosts: webserver
  become: true
  tasks:
    - name: Ensure web root exists
      ansible.builtin.file:
        path: /var/www/example.internal/html
        state: directory
        owner: root
        group: root
        mode: '0755'

    - name: Upload templated nginx configuration
      ansible.builtin.template:
        src: templates/example.internal.conf.j2
        dest: /etc/nginx/conf.d/example.internal.conf
        owner: root
        group: root
        mode: '0644'

    - name: Restart nginx to apply configuration
      ansible.builtin.service:
        name: nginx
        state: restarted

❯ ansible-playbook -i host 10-web-template.yml

PLAY [Configure webserver using template] **********************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************************
ok: [192.168.121.148]

TASK [Ensure web root exists] **********************************************************************************************************
ok: [192.168.121.148]

TASK [Upload templated nginx configuration] ********************************************************************************************
changed: [192.168.121.148]

TASK [Restart nginx to apply configuration] ********************************************************************************************
changed: [192.168.121.148]

PLAY RECAP *****************************************************************************************************************************
192.168.121.148            : ok=4    changed=2    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   


# Resources and Documentation

* https://docs.ansible.com/ansible/latest/collections/ansible/builtin/template_module.html
* https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_variables.html
* https://nginx.org/en/docs/http/ngx_http_core_module.html#listen
