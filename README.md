## BIND ApiBank Rest Service
[![codecov](https://codecov.io/bb/INCLUFIN_GIT/bindapi/branch/master/graph/badge.svg?token=BPJHU1ODPL)](https://codecov.io/bb/INCLUFIN_GIT/bindapi)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac9723f2c59940ee8fe7f8ea5c7de545)](https://www.codacy.com?utm_source=bitbucket.org&amp;utm_medium=referral&amp;utm_content=INCLUFIN_GIT/bindapi&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://api.codacy.com/project/badge/Coverage/ac9723f2c59940ee8fe7f8ea5c7de545)](https://www.codacy.com?utm_source=bitbucket.org&amp;utm_medium=referral&amp;utm_content=INCLUFIN_GIT/bindapi&amp;utm_campaign=Badge_Coverage)
---
### Pre-Reqs  
1. Docker: [see offical docs](https://docs.docker.com/install/)
2. Docker compose: [see offical docs](https://docs.docker.com/compose/install/)

3. Development:
    1. Kubernetes (**kubectl**): [see offical docs](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
    2. Minikube: [see offical docs](https://kubernetes.io/docs/tasks/tools/install-minikube/)
    3. Redis Server
    
4. Production & deployment:
    1. AWS user with command line interface (CLI) permission enabled 
    2. AWS CLI (**aws**): [see offical docs](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html)
    2. EKS CLI (**eksctl**): [see offical docs](https://docs.aws.amazon.com/eks/latest/userguide/getting-started-eksctl.html)
---
### Development environment
1. Create a virtual environment: use virtualenv or pyenv 
2. Install requirements file (requirements.txt)
3. Run source:
    
    ##### Dockerized mode:
    1. Edit & copy **sample.env** to **config.env**
    2. Build docker images  
        ```docker-compose build --no-cache```
    3. Run the following command from the source (src) folder:  
        ```docker-compose up``` 
    4. Check your service: ```http://localhost:8080```      
    *Note: **redis** server is already inside*

    ##### Manual mode:
    1. Set env vars:  
        ```export BINDAPI_USERNAME=username@email.com```  
        ```export BINDAPI_PASSWORD=this_is_a_password```  
        ```export BINDAPI_DEFAULT_ACCOUNT=XX-X-XXXXX-X-X```  
    3. Edit your hosts file and add the following line:  
        ```127.0.0.1	redis```
    4. Start your local redis server
    5. Run the following command from the source (src) folder:  
        ```flask run```  
    6. Check your service: ```http://localhost:5000```

---
### Production deployment

1. ##### Before start:
    1. Create an ECR repository [ECR console](https://console.aws.amazon.com/ecr/home)
    2. Build & push your docker image to repository  
        ```$(aws ecr get-login --no-include-email --region [your-region])```  
        ```docker build -t bindapi .```  
        ```docker tag bindapi:latest [ecr-repository-url]/bindapi:[version-tag]```  
        ```docker push [ecr-repository-url]/bindapi:[version-tag]``` 
    2. Edit **deploy/api-service-deployment.yaml** and set your image url:
        ```yaml
        containers: 
          - name: bindapi-service 
            image: [ecr-repository-url]/bindapi:[version-tag]
        ```
2. ##### Deployment
    1. Create cluster:
        ```shell
        eksctl create cluster \
        --name bindapi \
        --version 1.14 \
        --region [your-region] \
        --nodegroup-name standard-workers \
        --node-type t3.medium \
        --nodes 3 \
        --nodes-min 1 \
        --nodes-max 4 \
        --ssh-access \
        --ssh-public-key [your-public-key-path] \
        --managed
       ```
    2. Set envs vars editing **kustomization.yaml**  
        ```nano/vim /src/deploy/kustomization.yaml```
    3. Deploy cluster (step over src/deploy folder):  
        ```kubectl apply -k ./ ```

---
### Testing kubernetes stack locally
Check if all pre-reqs are meet also you will need an image uploaded to ECR repository

1. Start minikube with your installed driver:  
    ```minikube start --vm-driver=<driver_name>```  
    ```minikube addons enable ingress```  
    ```minikube addons configure registry-creds```  
    ```minikube addons enable registry-creds```  
2. Create a deployment  
    ```kubectl create deployment bindapi-test --image=[ecr-repository-url]/bindapi:[version-tag] --cloud-provider=aws```
3. Optional:  
   Edit deployments yamls files and switch/comment & uncomment: 
   **spec.type=LoadBalancer** values for **spec.type=NodePort**
4. Create deployment endpoint  
    ```minikube service frontend --url```
5. Check your local stack using the previous command output in a browser

*Note: for more information about minikube, providers & drivers see [official docs](https://kubernetes.io/docs/setup/learning-environment/minikube/#installation)*

---
### Common used commands

#### Docker:  
List images: ```docker images```   
List containers: ```docker ps```  
Build an image: ```docker build . -t **[name]:[tag]**```  

#### Kubernetes:  
Re-apply a deploy or an images: ```kubectl apply **[-k/-f]** ./```  
List nodes: ```kubectl get nodes```  
List pods: ```kubectl get pods```  
List services: ```kubectl get services```  
Cluster info: ```kubectl get servicescluster-info```  
List contexts: ```kubectl config get-contexts```  
Switch/use context: ```config use-context **[context]**``` 

---
### Code Quality

#### Coverage map (data layers):
![Coverage map](https://codecov.io/bb/INCLUFIN_GIT/bindapi/branch/master/graphs/icicle.svg?token=BPJHU1ODPL "Coverage map grid")

#### Commits graph:
![Commits](https://codecov.io/bb/INCLUFIN_GIT/bindapi/branch/master/graphs/commits.svg?token=BPJHU1ODPL "Commits map")