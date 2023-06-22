#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

try:
    import botocore
except ImportError:
    pass
    
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.core import is_boto3_error_code

def find_instance_info(module, client, fail_if_not_found=False):
    name = module.params.get('name')

    try:
        res = client.get_instance(instanceName=name)
    except is_boto3_error_code('NotFoundException') as e:
        if fail_if_not_found:
            module.fail_json_aws(e)
        return None
    except botocore.exceptions.ClientError as e:  
        module.fail_json_aws(e)
    return res['instance']



def attach_ip(module,client):
    name = module.params.get('name')
    instance = module.params.get('instance')

    inst = client.get_instance(instanceName=instance)
    while inst['instance']['state']["name"] != 'running':
        inst = client.get_instance(instanceName=instance)
        if inst['instance']['state']["name"] == 'running':
            break
    try:
        inst = client.attach_static_ip(staticIpName=name,instanceName=instance)
        module.exit_json(changed=True, instance=camel_dict_to_snake_dict(inst))
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e)

def detach_ip(module,client):
    name = module.params.get('name')
    try:
        inst = client.detach_static_ip(staticIpName=name)
        module.exit_json(changed=True, instance=camel_dict_to_snake_dict(inst))
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e)


def get_ip(module,client):
    name = module.params.get('name')
    try:
        inst = client.get_static_ip(staticIpName=name)
        module.exit_json(changed=False, instance=camel_dict_to_snake_dict(inst))
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e)

def allocate_ip(module,client):
    name = module.params.get('name')

    try:
        inst = client.allocate_static_ip(staticIpName=name)
        module.exit_json(changed=False, instance=camel_dict_to_snake_dict(inst))
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e)



def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        instance=dict(type='str'),
        state=dict(type='str', required=True, 
            choices=['new', 'attach','detach','info'])
        )

    module = AnsibleAWSModule(argument_spec=argument_spec)
    client = module.client('lightsail')
    
    state = module.params.get('state')
    if state == 'new':
        allocate_ip(module,client)
    if state == 'attach':
        attach_ip(module,client)
    if state == 'info':
        get_ip(module,client)
    if state == 'detach':
        detach_ip(module,client)


if __name__ == '__main__': 
    main()
