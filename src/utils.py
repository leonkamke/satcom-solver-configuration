import json
import os
import json
from datetime import datetime
import matplotlib.pyplot as plt

PROBLEM_INSTANCE_PATH = "./src/input/data/problem_instances.json"
SOLUTION_VISUALIZATION_PATH = "./src/output/visualizations/"

def readProblemInstance(input_path=PROBLEM_INSTANCE_PATH):
    with open(input_path, 'r') as file:
        data = json.load(file)

        service_targets = data[0]['service_targets']
        satellite_passes = data[0]['satellite_passes']

        return {
            "satellite_passes": satellite_passes,
            "service_targets": service_targets
        }


def plotOptimizationResult(serviceTargets, satellitePasses, contacts, optimizer, output_path=SOLUTION_VISUALIZATION_PATH):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Check which nodes have service demand
    nodes_demand = set()
    for serviceTarget in serviceTargets:
        nodes_demand.add(serviceTarget['nodeId'])
    # print("----------------------------------")
    # print("Nodes with service demand:\n" + str(sorted(list(nodes_demand))))

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
        color = 'orange'
        label = 'Serving optical-only service targets'

        serviceTarget = contact["serviceTarget"]
        if serviceTarget["requestedOperation"] == 'QKD' or serviceTarget["requestedOperation"] == 0:
            color = 'red'
            label = 'Serving at least one quantum service target'
        ax.plot([start_time, end_time], [node_id, node_id], color=color, label=label)

    # Remove duplicate labels from the legend
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(unique_labels.values(), unique_labels.keys(), bbox_to_anchor=(1.05, 1), loc='upper left')

    # Format the x-axis as dates
    ax.set_xlabel('Time (month-day hour)')
    ax.set_ylabel("Node ID")
    ax.set_title('Planned contacts for the next 12 orbits')
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