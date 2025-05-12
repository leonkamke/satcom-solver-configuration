import json
import json
from datetime import datetime
import matplotlib.pyplot as plt

SOLUTION_VISUALIZATION_PATH = "./src/output/visualization/"


def read_problem_instance(instance_path):
    with open(instance_path, "r") as file:
        data = json.load(file)
        return data[0]


def plotOptimizationResult(
    serviceTargets,
    satellitePasses,
    contacts,
    optimizer,
    output_path=SOLUTION_VISUALIZATION_PATH,
):
    fig, ax = plt.subplots(figsize=(14, 6))

    # Check which nodes have service demand
    nodes_demand = set()
    for serviceTarget in serviceTargets:
        nodes_demand.add(serviceTarget["nodeId"])

    # Loop through each possible satellite pass and plot it if the respective node has service demand
    for satellitePass in satellitePasses:
        node_id = satellitePass["nodeId"]
        if node_id in nodes_demand:
            start_time = datetime.fromisoformat(satellitePass["startTime"])
            end_time = datetime.fromisoformat(satellitePass["endTime"])
            ax.plot(
                [start_time, end_time],
                [node_id, node_id],
                color="grey",
                label="Potential contact",
            )

    # Loop through each contact and plot it
    for contact in contacts:
        slot = contact["satellitePass"]
        node_id = slot["nodeId"]
        start_time = datetime.fromisoformat(slot["startTime"])
        end_time = datetime.fromisoformat(slot["endTime"])

        serviceTarget = contact["serviceTarget"]
        if serviceTarget["requestedOperation"] == "QKD":
            color = "red"
            label = "QKD"
        else:
            color = "orange"
            label = "QKD post processing"
        ax.plot([start_time, end_time], [node_id, node_id], color=color, label=label)

    # Remove duplicate labels from the legend
    handles, labels = ax.get_legend_handles_labels()
    unique_labels = dict(zip(labels, handles))
    ax.legend(
        unique_labels.values(),
        unique_labels.keys(),
        bbox_to_anchor=(1.05, 1),
        loc="upper left",
    )

    # Format the x-axis as dates
    ax.set_xlabel("Time (month-day hour)")
    ax.set_ylabel("Node ID")
    ax.set_title("Planned contacts")
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

        priority = serviceTarget["priority"]
        achievableKeyVolume = satellitePass["achievableKeyVolume"]
        operationMode = 1 if serviceTarget["requestedOperation"] == "QKD" else 0
        result += priority * (1 + achievableKeyVolume * operationMode)
    return result


def read_contacts_from_timefold(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)

    contacts = []
    for contact in data:
        service_target = contact.get("serviceTarget", {})
        satellite_pass = contact.get("satellitePass", {})

        contacts.append(
            {
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
                    "startTime": (
                        datetime(*satellite_pass.get("startTime")).isoformat()
                        if satellite_pass.get("startTime")
                        else None
                    ),
                    "endTime": (
                        datetime(*satellite_pass.get("endTime")).isoformat()
                        if satellite_pass.get("endTime")
                        else None
                    ),
                    "achievableKeyVolume": satellite_pass.get("achievableKeyVolume"),
                    "orbitId": satellite_pass.get("orbitId"),
                },
            }
        )

    return contacts


# Validates satcom schedules
def verify_contacts_solution(contacts, T_min=60):
    used_passes = set()
    used_targets = set()
    pass_times = {}
    application_times = {}

    # Extract and validate contact assignments
    for contact in contacts:
        sp = contact["satellitePass"]
        st = contact["serviceTarget"]
        pass_id = sp["id"]
        target_id = st["id"]
        node_pass = sp["nodeId"]
        node_target = st["nodeId"]

        # Constraint: matching nodeId
        if node_pass != node_target:
            print(f"Node mismatch: pass {pass_id} and target {target_id}")
            return False

        # Constraint: o[i]==1 and m[j]==1 not allowed
        if sp["achievableKeyVolume"] == 0.0 and st["requestedOperation"] == "QKD":
            print(f"Invalid QKD contact: pass {pass_id} has zero volume")
            return False

        # Constraint: Each satellite pass assigned at most once
        if pass_id in used_passes:
            print(f"Satellite pass {pass_id} used more than once")
            return False
        used_passes.add(pass_id)

        # Constraint: Each service target assigned at most once
        if target_id in used_targets:
            print(f"Service target {target_id} used more than once")
            return False
        used_targets.add(target_id)

        start_time = datetime.fromisoformat(sp["startTime"])
        end_time = datetime.fromisoformat(sp["endTime"])
        pass_times[pass_id] = (start_time, end_time)

        # Group contact times by application for sequencing
        app_id = st["applicationId"]
        if app_id not in application_times:
            application_times[app_id] = {"QKD": [], "PP": []}
        if st["requestedOperation"] == "QKD":
            application_times[app_id]["QKD"].append(start_time)
        else:
            application_times[app_id]["PP"].append(start_time)

    # Constraint: No overlapping satellite passes with less than T_min separation
    sorted_times = sorted(pass_times.items(), key=lambda x: x[1][0])
    for i in range(len(sorted_times) - 1):
        _, (start1, end1) = sorted_times[i]
        _, (start2, _) = sorted_times[i + 1]
        if (start2 - end1).total_seconds() < T_min:
            print(f"Passes overlap or are too close: {end1} vs {start2}")
            return False

    # Constraint: QKD must come before Post-Processing for each application
    for app_id, times in application_times.items():
        if times["PP"] and times["QKD"]:
            if min(times["PP"]) < max(times["QKD"]):
                print(f"App {app_id}: Post-Processing before QKD")
                return False

    return True
