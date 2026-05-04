variable "app_name" {
  description = "ชื่อแอปพลิเคชัน"
  type        = string
  default     = "dustwatch"
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "dustwatch"
}

variable "docker_image" {
  description = "Docker image จาก Docker Hub (ชื่อ/image:tag)"
  type        = string
  default     = "yourdockerhub/dustwatch:latest"
}

variable "app_port" {
  description = "Port ที่ Flask app รัน"
  type        = number
  default     = 5000
}

variable "replicas" {
  description = "จำนวน Pod replicas"
  type        = number
  default     = 2
}
