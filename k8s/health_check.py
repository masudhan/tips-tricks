import os
import pandas as pd
from kubernetes.client import NetworkingV1Api
from kubernetes import client, config
from kubernetes.dynamic import DynamicClient

# Load Kubernetes config
config.load_kube_config(os.path.expanduser('~/.kube/config'))

# Initialize Kubernetes API clients
v1 = client.CoreV1Api()
networking_v1 = NetworkingV1Api()

def node_health_check():
    result = []
    for node in v1.list_node().items:
        for condition in node.status.conditions:
            if condition.type == "Ready":
                result.append((node.metadata.name, condition.status))
    return "Node Health Check", result

def persistent_volume_check():
    result = []
    pvs = v1.list_persistent_volume()
    for pv in pvs.items:
        result.append((pv.metadata.name, pv.status.phase))
    return "Persistent Volume Check", result

def resource_quotas_and_limits_check():
    result = []
    namespaces = v1.list_namespace()
    for ns in namespaces.items:
        resource_quotas = v1.list_namespaced_resource_quota(ns.metadata.name)
        for quota in resource_quotas.items:
            used = quota.status.used
            hard = quota.status.hard
            result.append((ns.metadata.name, dict(used), dict(hard)))
    return "Resource Quotas and Limits Check", result

def network_policies_check():
    result = []
    network_policy_list = networking_v1.list_network_policy_for_all_namespaces()
    for policy in network_policy_list.items:
        result.append((policy.metadata.namespace, policy.metadata.name))
    return "Network Policies Check", result

def service_exposure_and_lb_status_check():
    result = []
    services = v1.list_service_for_all_namespaces()
    for service in services.items:
        if service.spec.type == "LoadBalancer":
            ingress = service.status.load_balancer.ingress[0] if service.status.load_balancer.ingress else None
            result.append((service.metadata.namespace, service.metadata.name, ingress))
    return "Service Exposures and Load Balancer Status", result

dynamic_client = DynamicClient(client.ApiClient(configuration=config.load_kube_config()))

def custom_resource_validation(group, version, plural):
    result = []
    custom_resources = dynamic_client.resources.get(api_version=f'{group}/{version}', kind=plural)
    for cr in custom_resources.get().items:
        result.append((cr.metadata.name, cr.metadata.namespace, cr.status))
    return "Custom Resource Validation", result
  
def security_checks():
    try:
        networking_v1 = NetworkingV1Api()
        network_policies = networking_v1.list_network_policy_for_all_namespaces()
        policies = [(np.metadata.namespace, np.metadata.name) for np in network_policies.items]
        return "Security Checks - Network Policies", policies if policies else "No Network Policies Found"
    except client.exceptions.ApiException as e:
        return "Error while fetching Network Policies", str(e)

def api_server_health():
    health_status = v1.get_api_resources()
    return "API Server Health", "Healthy" if health_status else "Unhealthy"

def get_cluster_version():
    try:
        version_api = client.VersionApi()
        version_info = version_api.get_code()
        return "Cluster Version", version_info.git_version
    except client.exceptions.ApiException as e:
        return "Error while fetching Cluster Version", str(e)

def format_result(result):
    """Formats complex results into a more readable string."""
    if isinstance(result, list):
        return "; ".join(str(r) for r in result)
    if isinstance(result, dict):
        return "; ".join(f"{k}: {v}" for k, v in result.items())
    return str(result)

# Namespaces
def pod_status_check(namespace):
    result = []
    pods = v1.list_namespaced_pod(namespace)
    for pod in pods.items:
        pod_name = pod.metadata.name
        pod_phase = pod.status.phase
        # Check for detailed container statuses
        if pod.status.container_statuses:
            for container_status in pod.status.container_statuses:
                if container_status.state.waiting:
                    # If there is a waiting state, capture the reason
                    pod_phase = container_status.state.waiting.reason
        result.append((pod_name, pod_phase))
    return "Pod Status Check", result

def cron_jobs_check(namespace):
    try:
        batch_v1 = client.BatchV1Api()
        cron_jobs = batch_v1.list_namespaced_cron_job(namespace)
        jobs_info = [(job.metadata.name, job.status.last_schedule_time) for job in cron_jobs.items]
        return "Cron Jobs Check", jobs_info
    except client.exceptions.ApiException as e:
        return "Error while fetching Cron Jobs", str(e)


def logs_analysis_with_error_check(namespace, pod_name):
    try:
        logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace, since_seconds=600)
        error_lines = [line for line in logs.splitlines() if "Error" in line or "error" in line or "ERROR" in line]
        # Aggregating similar messages
        error_count = {}
        for error in error_lines:
            error_count[error] = error_count.get(error, 0) + 1
        aggregated_errors = [f"{error} (Count: {count})" for error, count in error_count.items()]
        return aggregated_errors if aggregated_errors else "No errors found"
    except client.exceptions.ApiException as e:
        return str(e)    

def configmaps_and_secrets_check(namespace):
    result = []
    configmaps = v1.list_namespaced_config_map(namespace)
    secrets = v1.list_namespaced_secret(namespace)
    result.append(("ConfigMaps", [cm.metadata.name for cm in configmaps.items]))
    result.append(("Secrets", [secret.metadata.name for secret in secrets.items]))
    return "ConfigMaps and Secrets Verification", result


# Define the namespace
namespace = "default"

# Perform checks
node_check = node_health_check()
pod_check = pod_status_check(namespace)
pv_check = persistent_volume_check()
resource_quotas_and_limits_checks = resource_quotas_and_limits_check()
service_exposure_and_lb_status_checks = service_exposure_and_lb_status_check()
configmaps_and_secrets_checks = configmaps_and_secrets_check(namespace)
network_policies_checks = network_policies_check()
logs_analysis_with_error_checks = logs_analysis_with_error_check(namespace, 'error-generator-pod')
security_check = security_checks()
api_server_health_check = api_server_health()
cron_jobs_checks = cron_jobs_check(namespace)
cluster_version_check = get_cluster_version()

check_data = {
    "Check": [
        node_check[0], pod_check[0], pv_check[0], 
        resource_quotas_and_limits_checks[0], service_exposure_and_lb_status_checks[0],
        configmaps_and_secrets_checks[0], network_policies_checks[0],
        logs_analysis_with_error_checks[0], security_check[0], 
        api_server_health_check[0], cron_jobs_checks[0], cluster_version_check[0]
    ],
    "Results": [
        format_result(node_check[1]), format_result(pod_check[1]), format_result(pv_check[1]),
        format_result(resource_quotas_and_limits_checks[1]), format_result(service_exposure_and_lb_status_checks[1]),
        format_result(configmaps_and_secrets_checks[1]), format_result(network_policies_checks[1]),
        format_result(logs_analysis_with_error_checks[1]), format_result(security_check[1]),
        format_result(api_server_health_check[1]), format_result(cron_jobs_checks[1]), format_result(cluster_version_check[1])
    ]
}

# Create a DataFrame and set display options
report = pd.DataFrame(check_data)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)

print(report)
