terraform {
  required_version = ">= 1.0"

  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }

    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
  }
}

locals {
  ansible_inventory_path = "${path.module}/../ansible/inventory"
  ansible_playbook_path  = "${path.module}/../ansible/playbook.yml"
}

resource "null_resource" "minikube" {
  triggers = {
    driver     = var.minikube_driver
    extra_args = var.minikube_start_extra_args
  }

  provisioner "local-exec" {
    command = "minikube status || minikube start --driver=${var.minikube_driver} ${var.minikube_start_extra_args}"
  }
}

resource "null_resource" "namespace" {
  depends_on = [null_resource.minikube]

  triggers = {
    namespace = var.namespace
  }

  provisioner "local-exec" {
    command = "kubectl create namespace ${var.namespace} --dry-run=client -o yaml | kubectl apply -f -"
  }
}

resource "local_file" "ansible_inventory" {
  filename = local.ansible_inventory_path

  content = templatefile("${path.module}/inventory.tpl", {
    app_name                  = var.app_name
    namespace                 = var.namespace
    docker_image              = var.docker_image
    app_port                  = var.app_port
    service_port              = var.service_port
    node_port                 = var.node_port
    replicas                  = var.replicas
    deployment_name           = var.deployment_name
    service_name              = var.service_name
    container_name            = var.container_name
    minikube_driver           = var.minikube_driver
    minikube_start_extra_args = var.minikube_start_extra_args
  })
}

resource "null_resource" "ansible_deploy" {
  depends_on = [
    local_file.ansible_inventory,
    null_resource.namespace
  ]

  triggers = {
    inventory_hash  = local_file.ansible_inventory.content_md5
    playbook_hash   = filesha256(local.ansible_playbook_path)
    deployment_hash = filesha256("${path.module}/../k8s/deployment.yaml")
    service_hash    = filesha256("${path.module}/../k8s/service.yaml")
    image           = var.docker_image
    replicas        = tostring(var.replicas)
  }

  provisioner "local-exec" {
    command = "ansible-playbook -i \"${local_file.ansible_inventory.filename}\" \"${local.ansible_playbook_path}\""
  }
}
