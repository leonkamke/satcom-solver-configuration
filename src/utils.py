import json
import json
from datetime import datetime
import matplotlib.pyplot as plt

SOLUTION_VISUALIZATION_PATH = "./src/output/visualizations/"

def read_problem_instance(instance_path):
    with open(instance_path, 'r') as file:
        data = json.load(file)
        return data[0]


def plotOptimizationResult(serviceTargets, satellitePasses, contacts, optimizer, output_path=SOLUTION_VISUALIZATION_PATH):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Check which nodes have service demand
    nodes_demand = set()
    for serviceTarget in serviceTargets:
        nodes_demand.add(serviceTarget['nodeId'])

    # Loop through each possible satellite pass and plot it if the respective node has service demand
    for satellitePass in satellitePasses:
        node_id = satellitePass['nodeId']
        if node_id in nodes_demand:
            start_time = datetime.fromisoformat(satellitePass['startTime'])
            end_time = datetime.fromisoformat(satellitePass['endTime'])
            ax.plot([start_time, end_time], [node_id, node_id], color='grey', label='Potential contact')

    # Loop through each contact and plot it
    for contact in contacts:
        slot = contact['satellitePass']
        node_id = slot['nodeId']
        start_time = datetime.fromisoformat(slot['startTime'])
        end_time = datetime.fromisoformat(slot['endTime'])

        serviceTarget = contact["serviceTarget"]
        if serviceTarget["requestedOperation"] == 'QKD':
            color = 'red'
            label = 'QKD'
        else:
            color = 'orange'
            label = 'QKD post processing'
        ax.plot([start_time, end_time], [node_id, node_id], color=color, label=label)

    # Remove duplicate labels from the legend
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(unique_labels.values(), unique_labels.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

    # Format the x-axis as dates
    ax.set_xlabel('Time (month-day hour)')
    ax.set_ylabel("Node ID")
    ax.set_title('Planned contacts')
    ax.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    formatted_time = datetime.now().strftime("%d-%m_%H-%M")
    plt.savefig(output_path + formatted_time + "_" + optimizer)
    # plt.show()

    plt.close()

def calculateObjectiveFunction(contacts):
    result = 0
    for contact in contacts:
        satellitePass = contact["satellitePass"]
        serviceTarget = contact["serviceTarget"]
        result += satellitePass["achievableKeyVolume"] + serviceTarget["priority"]
    return result

def read_contacts_from_timefold(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    contacts_from_json = data.get("contacts", [])
    
    contacts = []
    for contact in contacts_from_json:
        service_target = contact.get("serviceTarget", {})
        satellite_pass = contact.get("satellitePass", {})

        contacts.append({
            "serviceTarget": {
                "id": service_target.get("id"),
                "applicationId": service_target.get("applicationId"),
                "priority": service_target.get("priority"),
                "requestedOperation": service_target.get("requestedOperation"),
                "nodeId": service_target.get("nodeId"),
            },
            "satellitePass": {
                "id": satellite_pass.get("id"),
                "nodeId": satellite_pass.get("nodeId"),
                "startTime": datetime(*satellite_pass.get("startTime")).isoformat() if satellite_pass.get("startTime") else None,
                "endTime": datetime(*satellite_pass.get("endTime")).isoformat() if satellite_pass.get("endTime") else None,
                "achievableKeyVolume": satellite_pass.get("achievableKeyVolume"),
                "orbitId": satellite_pass.get("orbitId")
            },
        })
    
    return contacts