```
ansible all -m shell -a "free -m" -i inventories/production/services --limit production-server-1
ansible-playbook -u deamonkiller -i inventories/production playbooks/misc.yml --limit monitoring-server --tags addusers
```
