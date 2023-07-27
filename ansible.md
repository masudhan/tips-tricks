```
ansible all -m shell -a "free -m" -i inventories/production/services --limit production-server-1
ansible-playbook -u deamonkiller -i inventories/production playbooks/misc.yml --limit monitoring-server --tags addusers
```

```
- name: Get DEB architecture
  shell: dpkg --print-architecture
  register: deb_architecture

- name: Print DEB architecture
  debug:
    msg: "deb_architecture.stdout: {{ deb_architecture.stdout }}"
```

**Bastion to private instance from local? Add below code in inventory file**

`ansible_ssh_common_args="-o ProxyCommand='ssh -i /home/deamonkillerM/.ssh/id_rsa -W %h:%p madhu@111.22.12.29'"`
