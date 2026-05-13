[local]
localhost ansible_connection=local

[local:vars]
app_name=${app_name}
namespace=${namespace}
docker_image=${docker_image}
app_port=${app_port}
service_port=${service_port}
node_port=${node_port}
replicas=${replicas}
deployment_name=${deployment_name}
service_name=${service_name}
container_name=${container_name}
minikube_driver=${minikube_driver}
minikube_start_extra_args=${minikube_start_extra_args}
