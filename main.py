import boto3
from openpyxl import Workbook

eks_client = boto3.client('eks', region_name="us-east-1")
ec2_client = boto3.client('ec2', region_name="us-east-1")

def getClusters():
    # retrieve eks cluster response
    global eks_client
    response = eks_client.list_clusters()
    clusters = response['clusters']
    return clusters


def getClusterInfo(cluster):
    # retrieve relevant eks cluster details
    global eks_client
    cluster_info = eks_client.describe_cluster(name=cluster)
    cluster_version = cluster_info['cluster']['version']
    appID = cluster_info['cluster']['tags']['AppID'] if "AppID" in cluster_info['cluster']['tags'].keys() else "N/A"

    return {"EKS Cluster Version": cluster_version,
            "AppID": appID}

def getWorkerNodeInfo(workerNode):
    # retrieve relevant worker node details
    instance = workerNode['Instances'][0]
    instanceID = instance.get("InstanceId", "N/A")
    instanceType = instance.get("InstanceType", "N/A")
    os = instance.get("PlatformDetails", "N/A")

    find_owner = ec2_client.describe_tags(Filters=[{"Name": "resource-id",
                                                    "Values": [instanceID]},
                                                    {"Name": "key",
                                                    "Values": ["Owner"]}])

    owner = find_owner["Tags"][0]["Value"]

    return {
        "Worker Node Instance ID" : instanceID,
        "Owner" : owner,
        "Worker Node Instance Type": instanceType,
        "Worker Node Instance OS": os
    }

def main():

    # Create workbook and set the headers
    wb = Workbook()
    ws = wb.active
    ws.title = "Worker Node Details"
    headers = ["Cluster Name", "Cluster Version", "AppID", "Worker Node Instance ID", "Worker Node Instance OS", "Owner"]
    ws.append(headers)

    clusters = getClusters()

    # For each worker node, append the relevant data to the excel sheet
    for cluster in clusters:
        cluster_info = getClusterInfo(cluster)

        # Gets all the EC2 instances running the cluster
        worker_nodes = ec2_client.describe_instances(Filters=[{'Name':'tag:Cluster', 'Values':[cluster]}])
        worker_nodes = worker_nodes['Reservations']

        if len(worker_nodes) > 0:
            for node in worker_nodes:
                worker_node_info = getWorkerNodeInfo(node)
                # Writes in data to excel
                ws.append([cluster, cluster_info["EKS Cluster Version"], 
                        cluster_info["AppID"], worker_node_info["Worker Node Instance ID"],
                        worker_node_info["Worker Node Instance OS"],  worker_node_info["Owner"]])
        else:
            ws.append([cluster, cluster_info["EKS Cluster Version"], 
                        cluster_info["AppID"], "N/A", "N/A", "N/A"])

    # Save the excel file
    wb.save('worker_nodes_details.xlsx')

if __name__ == "__main__":
    main()
