variable "app_name" {
  description = "Application label used by the deployment scripts."
  type        = string
  default     = "pm-alert"
}

variable "namespace" {
  description = "Kubernetes namespace used for the PM Alert workload."
  type        = string
  default     = "dustwatch"
}

variable "docker_image" {
  description = "Docker image pushed by Jenkins and deployed to Kubernetes."
  type        = string
  default     = "tanyathep/pm-alert-app:latest"
}

variable "app_port" {
  description = "Container port exposed by the Flask application."
  type        = number
  default     = 5000
}

variable "service_port" {
  description = "Kubernetes service port."
  type        = number
  default     = 80
}

variable "node_port" {
  description = "NodePort used to access the app from Minikube."
  type        = number
  default     = 30001

  validation {
    condition     = var.node_port >= 30000 && var.node_port <= 32767
    error_message = "node_port must be between 30000 and 32767."
  }
}

variable "replicas" {
  description = "Number of application pods to run."
  type        = number
  default     = 2
}

variable "deployment_name" {
  description = "Kubernetes Deployment name from k8s/deployment.yaml."
  type        = string
  default     = "pm-alert"
}

variable "service_name" {
  description = "Kubernetes Service name from k8s/service.yaml."
  type        = string
  default     = "pm-alert-service"
}

variable "container_name" {
  description = "Container name inside the application Deployment."
  type        = string
  default     = "pm-alert"
}

variable "minikube_driver" {
  description = "Minikube driver used by local and Jenkins deployments."
  type        = string
  default     = "docker"
}

variable "minikube_start_extra_args" {
  description = "Extra arguments for minikube start. --force helps Jenkins Docker-in-Docker style demos run as root."
  type        = string
  default     = "--force"
}
