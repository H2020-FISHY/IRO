# README #

This README would normally document whatever steps are necessary to get your application up and running.

### intent Example ###

User one can not access to domain y at Night.

### Develepment Tasks ###

* Implementation of Elasticsearch [Done]
* Implementation of flask_classful [Done]
* intent Requirement check [Done]
* translate intent to Grammer (Policybuilder) [Done]
* intent Options check/get Value [Done]
* intent Parser [Done]
* changing intent reading system to ibt + commands [Done]
* solving conflict on push [Done]
* Code refactor (functions/solution improve) [Done]
* Improve Options Solution [Done]
* Add yaml-based IP configuration [Done]
* Add data interface to Kubernetes definition [TODO]

### Deployment (via Docker compose)
Install these two packets via your package manager: docker.io docker-compose
Run this command once on your machine:\
`echo -e "\nvm.max_map_count=524288\n" | sudo tee -a /etc/sysctl.conf && sudo sysctl -w vm.max_map_count=524288`

Deploy the system like this from inside the deployment directory:\
`docker-compose up -d elasticsearch
sleep 30
docker-compose up -d iro`

To later rebuild the IRO without redeploying Elastic (for example when you made some code changes), use this command (-d is optional):\
`docker-compose up --build -d iro`

### Deployment (as VMs)
IRO can be deployed using the Sandbox environment. To deploy this environment, you will need to have a functioning libvirt (KVM hypervisor) installation, along with the frontend Vagrant. Virtualbox is not fully supported yet due to lack of parallel starting of VMs. Simply 'cd' into the deployment directory and perform a "vagrant up". A setup containing 3 VMs with a NED instance each and one IRO on the control node will then be created. All interactions with kubectl fom inside the VMs require a leading 'sudo'.
