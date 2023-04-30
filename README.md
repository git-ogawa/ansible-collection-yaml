# Yaml collection for Ansible

This collection includes modules for managed yaml on target host.
List of the modules are listed [modules](#modules).

## Requirements

- python >= 3.8
- ansible >= 2.9

The python packages are required.

- ruamel.yaml >= 0.17.21
- jmespath >= 1.0.1


## Installation
To install in ansible default or defined paths use:

```bash
ansible-galaxy collection install git_ogawa.yaml
```

To specify the installation location use `-p`. If specifying a folder, make sure to update the `ansible.cfg` so ansible will check this folder as well.

```bash
ansible-galaxy collection install git_ogawa.yaml -p collections/
```

## modules

To see usage, see the links below.

- [git_ogawa.yaml.update_yaml](docs/git_ogawa.yaml.update_yaml_module.rst)
