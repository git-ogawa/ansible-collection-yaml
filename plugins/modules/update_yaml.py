#!/usr/bin/python

# Copyright: (c) 2023, git-ogawa <stu1232541964@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.git_ogawa.yaml.plugins.module_utils.parse import (
    ParserError,
    YamlParser,
)

__metaclass__ = type


DOCUMENTATION = r"""
---
module: update_yaml
version_added: "1.0.0"
short_description: Update values in yaml on target host
description:
    - Update values corresponding the specified key in yaml.
    - nested fields (such as nested dict and list) are supported.
    - Add the key and value if a key are missing in yaml when set option.
    - Mapping of values can be specified directly for readability.
options:
    path:
        description: Path of the yaml to be update.
        required: true
        type: str
    update:
        description: List of pairs of key-value to be updated.
        type: list
        elements: dict
        suboptions:
            key:
                description: The key.
                type: str
                required: false
            value:
                description: The Value.
                type: any
                required: false
            added:
                description: Set true to add the key that corresponding to the value are missing.
                default: false
                type: bool
            removed:
                description: Set true to remove the existing key if exists.
                default: false
                type: bool
    values:
        description: Mapping of values to be updated. See the examples below.
        required: false
        type: dict
    overwrite:
        description: If set true, allow values to be overwritten by the different type from the original type (dict to list or dict to list).
        default: False
        type: bool
requirements:
    - ruamel.yaml>=0.17.21
    - jmespath>=1.0.1
author:
    - git-ogawa
"""

EXAMPLES = r"""
# Update value of two keys
- name: Update value of two keys in /tmp/manifest.yml
  git_ogawa.yaml.update_yaml:
    path: /tmp/manifest.yml
    update:
      - key: user.name
        value: myname
      - key: user.age
        value: 20

# Update value in list. Add if the keys dose not exist.
- name: Update values
  git_ogawa.yaml.update_yaml:
    path: /tmp/manifest.yml
    update:
      - key: user_list[1].name
        value: testuser
        added: true
      - key: user_list[-1].age
        value: 20
        added: true

# Remove the existing keys
# If the keys are missing, there is no change.
- name: Remove the specified keys
  git_ogawa.yaml.update_yaml:
    path: /tmp/pod.yml
    update:
      - key: user_list[1].name
        removed: true
      - key: user.age
        removed: true

# Update some values in kubernetes manifest.
# for example https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/simple-pod.yaml
- name: Download manifest to remote host
  ansible.builtin.get_url:
    src: https://raw.githubusercontent.com/kubernetes/website/main/content/en/examples/pods/simple-pod.yaml
    dest: /tmp/pod.yml

- name: Update name and image version.
  git_ogawa.yaml.update_yaml:
    path: /tmp/pod.yml
    update:
      - key: metadata.name
        value: my-nginx
      - key: spec.containers[0].image
        value: nginx:latest

# User can set complex mapping of values directly in `values`.
# If the specified keys does not exist, it is automatically added.
- name: Update name and image version and add new container.
  git_ogawa.yaml.update_yaml:
    path: /tmp/pod.yml
    values:
      metadata:
        namespace: default
      spec:
        template:
          spec:
            containers:
              - name: hello2
                image: busybox:latest
              - name: nginx
                image: nginx:latest

# To change the type of field from dict to list (or list to dict) will be failed by default.
# If user want to do so, set overwrite to true.
# The below example changes the type of containers from list to dict.
- name: Update name and image version and add new container.
  git_ogawa.yaml.update_yaml:
    path: /tmp/pod.yml
    overwrite: true
    values:
      spec:
      template:
        spec:
        containers:
          mykey: myvalue
"""

RETURN = r"""
msg:
    description: The message showing the error details when task is failed.
    type: str
    returned: failed
updated_values:
    description: The mapping of values after the original values are updated.
    type: dict
    returned: changed
"""


def run_module():
    module_args = dict(
        path=dict(type="path", required=True),
        update=dict(
            type="list",
            required=False,
            options=dict(
                key=dict(type="str", required=False),
                values=dict(type="str", required=False, default={}),
                added=dict(type="bool", required=False, default=False),
                removed=dict(type="bool", required=False, default=False),
            ),
        ),
        values=dict(type="dict", required=False, default={}),
        overwrite=dict(type="bool", required=False, default=False),
    )

    result = dict(changed=False, updated_values=None)

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    if module.check_mode:
        module.exit_json(**result)

    parser = YamlParser(
        path=module.params["path"],
        update=module.params["update"],
        values=module.params["values"],
        overwrite=module.params["overwrite"],
    )
    try:
        parser.read()
        parser.run()
    except (FileNotFoundError, IndexError, TypeError, ParserError) as e:
        module.fail_json(msg=str(e), **result)

    result["updated_values"] = parser.yaml_data
    if parser.changed is True:
        parser.save()
        result["changed"] = True

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
