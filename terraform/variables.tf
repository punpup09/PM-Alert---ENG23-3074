variable "app_name" {
  description = "ชื่อแอปพลิเคชัน"
  type        = string
  default     = "pm-alert"  # เปลี่ยนจาก dustwatch เป็น pm-alert
}

variable "namespace" {
  description = "Kubernetes namespace"
  type        = string
  default     = "dustwatch" 
}

variable "docker_image" {
  description = "Docker image จาก Docker Hub (ชื่อ/image:tag)"
  type        = string
  default     = "tanyathep/pm-alert-app:latest" # เปลี่ยนเป็น Image ของเพื่อนในทีม
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