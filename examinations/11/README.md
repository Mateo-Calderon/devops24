# Examination 11 - Loops

Imagine that on the web server(s), the IT department wants a number of users accounts set up:

    alovelace
    aturing
    edijkstra
    ghopper

These requirements are also requests:

* `alovelace` and `ghopper` should be added to the `wheel` group.
* `aturing` should be added to the `tape` group
* `edijkstra` should be added to the `tcpdump` group.
* `alovelace` should be added to the `audio` and `video` groups.
* `ghopper` should be in the `audio` group, but not in the `video` group.

Also, the IT department, for some unknown reason, wants to copy a number of '\*.md' files
to the 'deploy' user's home directory on the `db` machine(s).

I recommend you use two different playbooks for these two tasks. Prefix them both with `11-` to
make it easy to see which examination it belongs to.

# QUESTION A

Write a playbook that uses loops to add these users, and adds them to their respective groups.

When your playbook is run, one should be able to do this on the webserver:

    [deploy@webserver ~]$ groups alovelace
    alovelace : alovelace wheel video audio
    [deploy@webserver ~]$ groups aturing
    aturing : aturing tape
    [deploy@webserver ~]$ groups edijkstra
    edijkstra : edijkstra tcpdump
    [deploy@webserver ~]$ groups ghopper
    ghopper : ghopper wheel audio

There are multiple ways to accomplish this, but keep in mind _idempotency_ and _maintainability_.

---
- name: Create users and assign groups
  hosts: webserver
  become: true
  tasks:
    - name: Ensure users exist with correct groups
      ansible.builtin.user:
        name: "{{ item.name }}"
        groups: "{{ item.groups | join(',') }}"
        append: true
        state: present
      loop:
        - { name: 'alovelace', groups: ['wheel', 'audio', 'video'] }
        - { name: 'aturing', groups: ['tape'] }
        - { name: 'edijkstra', groups: ['tcpdump'] }
        - { name: 'ghopper', groups: ['wheel', 'audio'] }

# QUESTION B

Write a playbook that uses

    with_fileglob: 'files/*.md5'

to copy all `\*.md` files in the `files/` directory to the `deploy` user's directory on the `db` server(s).

For now you can create empty files in the `files/` directory called anything as long as the suffix is `.md`:

    $ touch files/foo.md files/bar.md files/baz.md


---
- name: Copy all markdown files to deploy user's home directory
  hosts: db
  become: true
  tasks:
    - name: Copy all .md files from files/ to deploy's home
      ansible.builtin.copy:
        src: "{{ item }}"
        dest: "/home/deploy/"
        owner: deploy
        group: deploy
        mode: '0644'
      with_fileglob:
        - "files/*.md"


# BONUS QUESTION

Add a password to each user added to the playbook that creates the users. Do not write passwords in plain
text in the playbook, but use the password hash, or encrypt the passwords using `ansible-vault`.

There are various utilities that can output hashed passwords, check the FAQ for some pointers.

# BONUS BONUS QUESTION

Add the real names of the users we added earlier to the GECOS field of each account. Google is your friend.

# Resources and Documentation

* [loops](https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_loops.html)
* [ansible.builtin.user](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/user_module.html)
* [ansible.builtin.fileglob](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/fileglob_lookup.html)
* https://docs.ansible.com/ansible/latest/reference_appendices/faq.html#how-do-i-generate-encrypted-passwords-for-the-user-module


-----------------------------------------------------------------
❯ ansible-playbook -i host 11-users.yml

PLAY [Create users and assign groups] ******************************************

TASK [Gathering Facts] *********************************************************
ok: [192.168.121.148]

TASK [Ensure users exist with correct groups] **********************************
changed: [192.168.121.148] => (item={'name': 'alovelace', 'groups': ['wheel', 'audio', 'video']})
changed: [192.168.121.148] => (item={'name': 'aturing', 'groups': ['tape']})
changed: [192.168.121.148] => (item={'name': 'edijkstra', 'groups': ['tcpdump']})
changed: [192.168.121.148] => (item={'name': 'ghopper', 'groups': ['wheel', 'audio']})

PLAY RECAP *********************************************************************
192.168.121.148            : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

---------------------------------------------------------------------
❯ ansible-lint 11-copy-md.yml

Passed: 0 failure(s), 0 warning(s) on 1 files. Last profile that met the validation criteria was 'production'.
❯ ansible-playbook -i host 11-copy-md.yml

PLAY [Copy all markdown files to deploy users home directory] ******************

TASK [Gathering Facts] *********************************************************
ok: [192.168.121.32]

TASK [Copy all .md files from files/ to deploys home] **************************
changed: [192.168.121.32] => (item=/home/gato/ansible/files/bar.md)
changed: [192.168.121.32] => (item=/home/gato/ansible/files/foo.md)
changed: [192.168.121.32] => (item=/home/gato/ansible/files/baz.md)

PLAY RECAP *********************************************************************
192.168.121.32             : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 