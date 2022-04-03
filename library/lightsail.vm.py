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

def find_instance_info(module, client, instance_name, fail_if_not_found=False):
    try:
        res = client.get_instance(instanceName=instance_name)
    except is_boto3_error_code('NotFoundException') as e:
        if fail_if_not_found:
            module.fail_json_aws(e)
        return None
    except botocore.exceptions.ClientError as e: 
        module.fail_json_aws(e)
    return res['instance']

def create_vm(module,client,instance_name):
    create_params = {'instanceNames': [instance_name],
                    'availabilityZone': module.params.get('zone'),
                    'blueprintId': module.params.get('blueprint_id'),
                    'bundleId': module.params.get('bundle_id'),
                    'userData': module.params.get('user_data'),
                    'ipAddressType': module.params.get('ip_type')}

    key_pair_name = module.params.get('key_pair_name')

    if key_pair_name:
        create_params['keyPairName'] = key_pair_name
    try:
        client.create_instances(**create_params)
    except botocore.exceptions.ClientError as e:
        module.fail_json_aws(e)

    inst = find_instance_info(module, client, instance_name, fail_if_not_found=True)
    module.exit_json(changed=False, instance=camel_dict_to_snake_dict(inst))

def change_state_vm(module,client,instance_name):
    state = module.params.get('state')

    if state == 'delete':
        try: 
            inst = client.delete_instance(instanceName=instance_name,forceDeleteAddOns=True)
            module.exit_json(changed=True, instance=camel_dict_to_snake_dict(inst))
        except botocore.exceptions.ClientError as e:
            module.fail_json_aws(e)

    if state == 'reboot':
        try:
            inst = client.reboot_instance(instanceName=instance_name)
            module.exit_json(changed=True, instance=camel_dict_to_snake_dict(inst))
        except botocore.exceptions.ClientError as e:
            module.fail_json_aws(e)

    if state == 'stop':
        try:
            inst = client.stop_instance(instanceName=instance_name)
            module.exit_json(changed=True, instance=camel_dict_to_snake_dict(inst))
        except botocore.exceptions.ClientError as e:
            module.fail_json_aws(e)

    if state == 'run':
        try:
            inst = client.start_instance(instanceName=instance_name)
            module.exit_json(changed=True, instance=camel_dict_to_snake_dict(inst))
        except botocore.exceptions.ClientError as e:
            module.fail_json_aws(e)
            
    if state == 'info':
        inst = find_instance_info(module, client, instance_name, fail_if_not_found=True)
        module.exit_json(changed=False, instance=camel_dict_to_snake_dict(inst))

def main():
    argument_spec = dict(
        name=dict(type='str', required=True),
        state=dict(
            type='str', required=True,  
            choices=['new', 'stop', 'reboot','run','delete','info']),
        zone=dict(type='str'),
        blueprint_id=dict(type='str'),
        bundle_id=dict(type='str'),
        key_pair_name=dict(type='str'),
        user_data=dict(type='str', default=''),
        ip_type=dict(type='str', default='dualstack')
        )

    module = AnsibleAWSModule(argument_spec=argument_spec)
    
    client = module.client('lightsail')
    state = module.params.get('state')
    name = module.params['name']

    if state == 'new':
        inst = create_vm(module,client,name)
    else: 
        inst = change_state_vm(module,client,name)

if __name__ == '__main__': 
    main()

