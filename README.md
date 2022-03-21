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

### Option 1: docker compose (development only)

Prerequisites

- `docker`
- `docker-compose`

If you want to use HTTPS for IRO, place the certificates into the 'crt' directory. IRO will then automatically pick them up and use them when it starts up.

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

All interactions with kubectl fom inside the VMs require 'sudo'. If you require HTTPS support, enter the VM via 'vagrant ssh' and follow the instructions for Kubernetes. You will then have to redeploy IRO.

### Option 3: Kubernetes (showcase/production)

#### Optional:
For HTTPS deployment, create a kubernetes secret called 'iro-crt-secret' from your certificate and key file via:
```
kubectl create secret tls iro-crt-secret --key /PATHTO/key.pem --cert /PATHTO/cert.pem
```
Alternatively, you can also encode the content of the files as base64 and place them directly into a YAML file, we provide an example in 'iro\_certificate.yml'. Then simply apply the file before you deploy IRO:
```
kubectl apply -f deployment/iro_certificate.yml
```

#### Deployment:
Use Kubernetes with the definition at `deployment/iro_k8s_deploy.yml`.
Deploy with:
```shell
kubectl apply -f deployment/iro_k8s_deploy.yml
```
The IRO pods will then be spawned in the default namespace.



## Changelog

### Upcoming
- Support for HTTPS by placing key.pem and cert.pem into the 'crt' folder (docker-compose) or deploying a secret (Kubernetes)
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
