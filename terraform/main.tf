terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.0"
    }
  }
}

# ตรวจสอบว่า Minikube รันอยู่
resource "null_resource" "check_minikube" {
  provisioner "local-exec" {
    command = "minikube status || minikube start --driver=docker --force"
  }
}

# สร้าง namespace สำหรับ DustWatch
resource "null_resource" "create_namespace" {
  depends_on = [null_resource.check_minikube]

  provisioner "local-exec" {
    command = "kubectl create namespace ${var.namespace} --dry-run=client -o yaml | kubectl apply -f -"
  }
}

# สร้างไฟล์ inventory สำหรับ Ansible
resource "local_file" "ansible_inventory" {
  depends_on = [null_resource.create_namespace]

  content  = templatefile("${path.module}/inventory.tpl", {
    app_name  = var.app_name
    namespace = var.namespace
    image     = var.docker_image
    port      = var.app_port
  })
  filename = "${path.module}/../ansible/inventory"
}

# รัน Ansible playbook หลังจาก Terraform เสร็จ
resource "null_resource" "run_ansible" {
  depends_on = [local_file.ansible_inventory]

  provisioner "local-exec" {
    command = "ansible-playbook -i ${path.module}/../ansible/inventory ${path.module}/../ansible/playbook.yml"
  }
}
