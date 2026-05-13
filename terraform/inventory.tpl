[local]
localhost ansible_connection=local

[local:vars]
app_name=${app_name}
namespace=${namespace}
docker_image=${image}
app_port=${port}