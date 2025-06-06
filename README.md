# Intent-based Resilience Orchestrator (IRO)

This repository contains the code of IRO and the instruction for its deployment. 

This development is part of the H2020 European Project Fishy.


## Progress on internal components

- Knowledge base: WIP
- Intent manager: WIP
- Intent compiler: WIP
- Policy configurator: WIP
- Learning and reasoning: WIP


## Progress on integration

- Containerization: Done
- Integration with Fishy sandbox: Done
- Integration with EDC: WIP
- Integration with Central Repository: Done
- Integration with Smart Contracts: Done


## Deployment 

### Option 1: docker compose (development only)

Prerequisites

- `docker`
- `docker-compose`


Run this command once on your machine:
```shell
echo -e "\nvm.max_map_count=524288\n" | sudo tee -a /etc/sysctl.conf && sudo sysctl -w vm.max_map_count=524288
```

Build and deploy with:
```shell
cd deployment/
docker-compose up --build
```


### Option 2: vagrant (development only)

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

### Option 3: Kubernetes (showcase/production)

Use Kubernetes with the definition at `deployment/iro_kubernetes.yml`.
Deploy with:
```shell
kubectl apply -f deployment/iro_kubernetes.yml
```
The IRO pods will then be spawned in the default namespace.



## Changelog

### Upcoming
- Implementation of data exchange with TIM
- Added Virtualbox support for Vagrantfile
- Added host filesystem mount; mapped host's /tmp to container's /edc

### 1.0.5 (22-02-07) 
- Added Classes to define HSLP policies

### 1.0.4 (22-02-03)
- Fixed IP assignment for IRO pod not working

### 1.0.3 (22-02-02)
- Updated elasticsearch to version 7.16.3
- Outsourced the pip requrements into extra file
