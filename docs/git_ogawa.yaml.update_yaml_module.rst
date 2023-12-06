.. _git_ogawa.yaml.update_yaml_module:


**************************
git_ogawa.yaml.update_yaml
**************************

**Update values in yaml on target host**


Version added: 1.0.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Update values corresponding the specified key in yaml.
- nested fields (such as nested dict and list) are supported.
- Add the key and value if a key are missing in yaml when set option.
- Mapping of values can be specified directly for readability.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ruamel.yaml>=0.17.21
- jmespath>=1.0.1


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>overwrite</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>If set true, allow values to be overwritten by the different type from the original type (dict to list or dict to list).</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path of the yaml to be update.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>update</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>List of pairs of key-value to be updated.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>added</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set true to add the key that corresponding to the value are missing.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The key.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>removed</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Set true to remove the existing key if exists.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>value</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">any</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The Value.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>values</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Mapping of values to be updated. See the examples below.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>msg</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>failed</td>
                <td>
                            <div>The message showing the error details when task is failed.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>updated_values</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>changed</td>
                <td>
                            <div>The mapping of values after the original values are updated.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- git-ogawa
