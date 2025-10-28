#!/usr/bin/env python3
from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(dict(message=dict(type='str', required=True)), supports_check_mode=True)
    msg = module.params['message']
    rev = msg[::-1]

    if msg == "fail me":
        module.fail_json(msg="You requested this to fail", changed=True, original_message=msg, reversed_message=rev)

    module.exit_json(changed=(msg != rev), original_message=msg, reversed_message=rev)

if __name__ == "__main__":
    main()
