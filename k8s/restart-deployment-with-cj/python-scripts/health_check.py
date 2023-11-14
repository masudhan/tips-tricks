import os
import subprocess
import pandas as pd
from kubernetes import client, config

# Load Kubernetes config
config.load_kube_config(os.path.expanduser('~/.kube/config'))

# Initialize Kubernetes API clients
v1 = client.CoreV1Api()
networking_v1 = client.NetworkingV1Api()

def check_site_reachability(url):
    try:
        response = subprocess.check_output(["curl", "-I", url])
        return "Site is reachable", response.decode()
    except subprocess.CalledProcessError as e:
        return "Site is not reachable", e.output.decode()

def check_ingress(namespace, domain):
    ingress_list = networking_v1.list_namespaced_ingress(namespace)
    for ingress in ingress_list.items:
        for rule in ingress.spec.rules:
            if rule.host == domain:
                return "Ingress found", ingress.metadata.name
    return "Ingress not found", ""

def check_service_to_endpoint(namespace, service_name):
    try:
        service = v1.read_namespaced_service(service_name, namespace)
        endpoints = v1.read_namespaced_endpoints(service_name, namespace)
        return "Service and Endpoints are OK", f"Service: {service.metadata.name}, Endpoints: {len(endpoints.subsets)}"
    except Exception as e:
        return "Service/Endpoints issue", str(e)

def check_pod_logs(namespace, pod_name):
    try:
        logs = v1.read_namespaced_pod_log(pod_name, namespace)
        return "Pod logs are OK", logs[:200]  # Truncated logs for brevity
    except Exception as e:
        return "Issue with Pod logs", str(e)

def perform_nslookup(domain):
    try:
        result = subprocess.check_output(["nslookup", domain])
        return "nslookup successful", result.decode()
    except subprocess.CalledProcessError as e:
        return "nslookup failed", e.output.decode()

# Define the domain and namespace
domain = "yourdomain.com"
namespace = "yournamespace"

# Performing checks
site_check = check_site_reachability(domain)
ingress_check = check_ingress(namespace, domain)
service_check = check_service_to_endpoint(namespace, "your-service")
pod_check = check_pod_logs(namespace, "your-pod")
dns_check = perform_nslookup(domain)

# Create a DataFrame for the report
report = pd.DataFrame({
    "Check": ["Site Reachability", "Ingress Validation", "Service to Endpoint", "Pod Logs", "DNS Lookup"],
    "Status": [site_check[0], ingress_check[0], service_check[0], pod_check[0], dns_check[0]],
    "Details": [site_check[1], ingress_check[1], service_check[1], pod_check[1], dns_check[1]]
})

print(report)
