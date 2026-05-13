output "namespace" {
  description = "Kubernetes namespace created for the app."
  value       = var.namespace
}

output "docker_image" {
  description = "Docker image deployed by Ansible."
  value       = var.docker_image
}

output "replicas" {
  description = "Number of pods requested for the deployment."
  value       = var.replicas
}

output "ansible_inventory" {
  description = "Inventory file generated for Ansible."
  value       = local_file.ansible_inventory.filename
}

output "application_url_command" {
  description = "Run this command to print the Minikube NodePort URL."
  value       = "minikube service ${var.service_name} -n ${var.namespace} --url"
}
