output "namespace" {
  description = "Kubernetes namespace ที่สร้าง"
  value       = var.namespace
}

output "app_name" {
  description = "ชื่อแอปพลิเคชัน"
  value       = var.app_name
}

output "docker_image" {
  description = "Docker image ที่ใช้ deploy"
  value       = var.docker_image
}

output "app_port" {
  description = "Port ของ Flask app"
  value       = var.app_port
}
