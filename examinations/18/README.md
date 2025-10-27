# Examination 18 - Write an Ansible module (VG)

Ansible modules are types of plugins that execute automation tasks on a 'target'. In the previous
examinations you have used many different modules, written by Ansible developers.

A module in Ansible is a Python script that adheres to a particular convention.

You can see the places where Ansible looks for modules by dumping the Ansible configuration
and then search for `DEFAULT_MODULE_PATH`:

    $ ansible-config dump | grep -i module_path

We will now write our own module, and run it through Ansible.

# QUESTION A

Look at [Developing modules](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
and create a module that

* Is called `anagrammer`
* Takes one parameter, `message`, that is a string.
* Returns two values:
    - `original_message` that is the string that is passed through `message`
    - `reversed_message` that is the `message` string, only backwards (reversed).
* If the `original_message` and `reversed_message` is different, the `changed` parameter should be `True`, otherwise
  it should be `False`.

When you are done, you should be able to do

    $ ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="hello world"' localhost

And it should return

    localhost | CHANGED => {
        "changed": true,
        "original_message": "hello world",
        "reversed_message": "dlrow olleh"
    }

You should also be able to do

    ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="sirap i paris"' localhost

And it should return

    localhost | SUCCESS => {
        "changed": false,
        "original_message": "sirap i paris",
        "reversed_message": "sirap i paris"
    }

If you pass in 'fail me', it should fail like this:

    localhost | FAILED! => {
        "changed": true,
        "msg": "You requested this to fail",
        "original_message": "fail me",
        "reversed_message": "em liaf"
    }

❯ ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="hello world"' localhost

localhost | CHANGED => {
    "changed": true,
    "original_message": "hello world",
    "reversed_message": "dlrow olleh"
}
❯ ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="sirap i paris"' localhost

localhost | SUCCESS => {
    "changed": false,
    "original_message": "sirap i paris",
    "reversed_message": "sirap i paris"
}
❯ localhost | SUCCESS => {
    "changed": false,
    "original_message": "sirap i paris",
    "reversed_message": "sirap i paris"
}

zsh: parse error near `}'
❯ ANSIBLE_LIBRARY=./library ansible -m anagrammer -a 'message="fail me"' localhost

localhost | FAILED! => {
    "changed": true,
    "msg": "You requested this to fail",
    "original_message": "fail me",
    "reversed_message": "em liaf"

# QUESTION B

Study the output of `ansible-config dump | grep -i module_path`. You will notice that there is a directory
in your home directory that Ansible looks for modules in.

Create that directory, and copy the Ansible module you just wrote there, then make a playbook
that uses this module with the correct parameters.

You don't need to worry about FQCN and namespaces in this examination.

❯ ansible-config dump | grep -i module_path

DEFAULT_MODULE_PATH(default) = ['/home/gato/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
❯ mkdir -p ~/.ansible/plugins/modules

❯ cp library/anagrammer.py ~/.ansible/plugins/modules/

# QUESTION C

Create a playbook called `18-anagrammer.yml` that uses this module.

Make the playbook use a default variable for the message that can be overriden by using something like:

    $ ansible-playbook --verbose --extra-vars message='"This is a whole other message"' 18-custom-module.yml

❯ ansible-playbook --verbose --extra-vars message='"This is a whole other message"' 18-anagrammer.yml
Using /home/gato/ansible/ansible.cfg as config file

PLAY [Run custom anagrammer module] ********************************************

TASK [Run the anagrammer module] ***********************************************
changed: [localhost] => {"changed": true, "original_message": "This is a whole other message", "reversed_message": "egassem rehto elohw a si sihT"}

TASK [Show result] *************************************************************
ok: [localhost] => {
    "result": {
        "changed": true,
        "failed": false,
        "original_message": "This is a whole other message",
        "reversed_message": "egassem rehto elohw a si sihT"
    }
}

PLAY RECAP *********************************************************************
localhost                  : ok=2    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

# BONUS QUESTION

What is the relationship between the booleans you can use in Python, and the various "truthy/falsy" values
you most often use in Ansible?

What modules/filters are there in Ansible that can safely test for "truthy/falsy" values, and return something
more stringent?
