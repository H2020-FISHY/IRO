# IRO README #

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

### Deployment ###
#Install these two packets via your package manager: docker.io docker-compose
#Run this command once on your machine:
echo -e "\nvm.max_map_count=524288\n" | sudo tee -a /etc/sysctl.conf && sudo sysctl -w vm.max_map_count=524288
#Deploy the system like this:
docker-compose up -d elasticsearch
sleep 30
docker-compose up -d iro
