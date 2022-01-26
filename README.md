# Intent-based Resilience Orchestrator (IRO)

This repository contains the code of IRO and the instruction for its deployment. 

This development is part of the H2020 European Project Fishy.


## Progress on internal components

- Knowledge base: WIP
- Intent manager: WIP
- Intent compiler: WIP
- Policy configurator: WIP
- Learning and reasoning: TODO


## Progress on integration

- Containerization: Done
- Integration with Fishy sandbox: Done
- Integration with EDC: WIP
- Integration with TIM: TODO


## Deployment 
(for development only, for showcase, please use Kubernetes with the definition at deployment/iro_kubernetes.yml)

### Option 1: docker compose 

Prerequisites

- `docker`
- `docker-compose`


Run this command once on your machine:
```shell
echo -e "\nvm.max_map_count=524288\n" | sudo tee -a /etc/sysctl.conf && sudo sysctl -w vm.max_map_count=524288
```

Deploy with:
```shell
cd deployment/
docker-compose up -d
```

To rebuild IRO without redeploying Elasticsearch:

```shell
docker-compose up --build -d iro
```

### Option 2: vagrant

Prerequisites

- `vagrant`
- `libvirtd` (kvm hypervisor as provider)

Deploy with:
```shell
cd deployment/
vagrant up
```
A setup containing 3 VMs with a NED instance each and one IRO on the control node will then be created. 

All interactions with kubectl fom inside the VMs require 'sudo'.
