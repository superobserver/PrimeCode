from flask import Flask, render_template, request, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from cableManager import CableManager, CableState, CableType, ApplicationType, DeviceType, ConsumableType, FiberMode
import networkx as nx
from collections import defaultdict
import pandas as pd
import seaborn as sns
import numpy as np
import uuid
import json

app = Flask(__name__)
manager = CableManager()

# Helper to convert plot to base64 image
def plot_to_base64():
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()
    plt.close()
    return img_base64

@app.route('/')
def index():
    cable_ids = sorted(cable.cable_id for cable in manager.cables)
    rooms = sorted(set(cable.server_room for cable in manager.cables) | set(cable.device_room for cable in manager.cables))
    states = [state.value for state in CableState]
    cable_types = [ctype.value for ctype in CableType if ctype != CableType.GAMECHANGER]
    app_types = [atype.value for atype in ApplicationType]
    device_types = [dtype.value for dtype in DeviceType]
    consumables = [ctype.value for ctype in ConsumableType]
    fiber_modes = [fmode.value for fmode in FiberMode]
    fiber_strands = [1, 12, 24, 48, 96, 144, 288]
    return render_template('index.html', cable_ids=cable_ids, rooms=rooms, states=states, 
                         cable_types=cable_types, app_types=app_types, device_types=device_types,
                         consumables=consumables, fiber_modes=fiber_modes, fiber_strands=fiber_strands)

@app.route('/room_deliverables', methods=['POST'])
def room_deliverables():
    selected_room = request.form.get('room')
    if not selected_room:
        return render_template('error.html', message="No room selected.")
    
    cables = [cable for cable in manager.cables if cable.server_room == selected_room or cable.device_room == selected_room]
    data = []
    for cable in cables:
        remaining = cable.remaining_deliverables()
        data.append({
            'Cable ID': cable.cable_id,
            'Remaining Deliverables': ', '.join(remaining) if remaining else 'None',
            'Num Remaining': len(remaining) if remaining else 0
        })
    df = pd.DataFrame(data)
    table_html = df.to_html(index=False, classes='table table-bordered')
    
    return render_template('table.html', title=f"Deliverables for {selected_room}", table_html=table_html)

@app.route('/global_deliverables')
def global_deliverables():
    data = []
    deliverables = [
        "Schematics Verified", "Path Exists", "Length (Device)", "Length (Procore)",
        "Cable Selected", "Patch Panel Installed", "Assigned Team",
        "Cable Toned", "Cable Tested", "Cable Certified", "Installed to Completion"
    ]
    counts = {d: 0 for d in deliverables}
    for cable in manager.cables:
        labels, values = cable.pie_chart_data()
        for label, value in zip(labels, values):
            if value == 1:  # Incomplete
                counts[label] += 1
    
    plt.figure(figsize=(10, 5))
    plt.bar(counts.keys(), counts.values(), color='red')
    plt.xticks(rotation=45)
    plt.xlabel('Deliverables')
    plt.ylabel('Number of Cables')
    plt.title('Global Remaining Deliverables')
    plt.tight_layout()
    img_base64 = plot_to_base64()
    
    return render_template('plot.html', img_base64=img_base64, title="Global Remaining Deliverables")

@app.route('/plot_completion', methods=['POST'])
def plot_completion():
    selected_room = request.form.get('room')
    if not selected_room:
        return render_template('error.html', message="No room selected.")
    
    cables = [cable for cable in manager.cables if cable.server_room == selected_room or cable.device_room == selected_room]
    cables.sort(key=lambda c: c.completion_percentage(), reverse=True)
    
    deliverables = [
        "Schematics Verified", "Path Exists", "Length (Device)", "Length (Procore)",
        "Cable Selected", "Patch Panel Installed", "Assigned Team",
        "Cable Toned", "Cable Tested", "Cable Certified", "Installed to Completion"
    ]
    num_deliverables = len(deliverables)
    segment_height = 1.0 / num_deliverables
    
    cable_ids = [c.cable_id for c in cables]
    num_cables = len(cable_ids)
    bottom = np.zeros(num_cables)
    
    plt.figure(figsize=(12, 8))
    for i, deliverable in enumerate(deliverables):
        heights = []
        colors = []
        for cable in cables:
            labels, values = cable.pie_chart_data()
            deliverable_idx = labels.index(deliverable)
            is_completed = values[deliverable_idx] == 0  # 0 means completed
            heights.append(segment_height if is_completed else 0)
            colors.append(f'C{i}' if is_completed else 'lightgrey')
        
        plt.bar(cable_ids, heights, bottom=bottom, color=colors, label=deliverable)
        bottom += np.array(heights)
    
    plt.ylim(0, 1)
    plt.xlabel("Cable ID")
    plt.ylabel("Completion Progress")
    plt.title(f"Cable Completion in {selected_room} (0 to 1)")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.xticks(rotation=45)
    plt.tight_layout()
    img_base64 = plot_to_base64()
    
    return render_template('plot.html', img_base64=img_base64, title=f"Completion Plot for {selected_room}")

@app.route('/plot_heatmap', methods=['POST'])
def plot_heatmap():
    selected_room = request.form.get('room')
    if not selected_room:
        return render_template('error.html', message="No room selected.")
    
    cables = [c for c in manager.cables if c.server_room == selected_room or c.device_room == selected_room]
    df = pd.DataFrame([{
        'Cable ID': c.cable_id,
        'Resource Needs': sum(1 for _, v in zip(*c.pie_chart_data()) if v == 1)  # Count incomplete deliverables
    } for c in cables])
    
    plt.figure(figsize=(12, 8))
    pivot = df.pivot_table(values='Resource Needs', index='Cable ID', columns=None, aggfunc='max', fill_value=0)
    sns.heatmap(pivot, cmap='YlOrRd', annot=True, fmt='d')
    plt.title(f"Remaining Deliverables Heatmap for {selected_room}")
    plt.xlabel("Deliverables")
    plt.ylabel("Cable ID")
    plt.tight_layout()
    img_base64 = plot_to_base64()
    
    return render_template('plot.html', img_base64=img_base64, title=f"Deliverables Heatmap for {selected_room}")

@app.route('/plot_incomplete', methods=['POST'])
def plot_incomplete():
    selected_room = request.form.get('room')
    if not selected_room:
        return render_template('error.html', message="No room selected.")
    
    server_rooms = sorted(set(cable.server_room for cable in manager.cables))
    is_server_room = selected_room in server_rooms
    
    if is_server_room:
        fig, ax = plt.subplots(figsize=(10, 5))
        G = nx.DiGraph()
        edge_counts = defaultdict(int)
        
        for cable in manager.cables:
            if cable.server_room == selected_room and cable.state != CableState.INSTALLED_TO_COMPLETION:
                edge = (selected_room, cable.device_room)
                edge_counts[edge] += 1
                G.add_edge(selected_room, cable.device_room, weight=edge_counts[edge])
        
        if not G.edges:
            ax.text(0.5, 0.5, f'No incomplete cables from {selected_room}', horizontalalignment='center', verticalalignment='center')
            ax.axis('off')
        else:
            pos = nx.spring_layout(G)
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightblue", node_size=500)
            for edge in G.edges(data=True):
                src, dst, data = edge
                weight = data["weight"]
                nx.draw_networkx_edges(G, pos, edgelist=[(src, dst)], width=weight * 0.5, ax=ax)
            nx.draw_networkx_labels(G, pos, ax=ax)
            edge_labels = {(u, v): f"{d['weight']} cables" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        ax.set_title(f"{selected_room} Incomplete Cables")
        plt.tight_layout()
        img_base64 = plot_to_base64()
        
        associations = manager.get_room_associations(selected_room)
        assoc_data = [(room, count) for room, count in sorted(associations.items())]
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        G = nx.DiGraph()
        edge_counts = defaultdict(int)
        
        for cable in manager.cables:
            if cable.device_room == selected_room and cable.state != CableState.INSTALLED_TO_COMPLETION:
                edge = (cable.server_room, selected_room)
                edge_counts[edge] += 1
                G.add_edge(cable.server_room, selected_room, weight=edge_counts[edge])
        
        if not G.edges:
            ax.text(0.5, 0.5, f'No incomplete cables to {selected_room}', horizontalalignment='center', verticalalignment='center')
            ax.axis('off')
        else:
            pos = nx.spring_layout(G)
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightblue", node_size=500)
            nx.draw_networkx_edges(G, pos, ax=ax)
            nx.draw_networkx_labels(G, pos, ax=ax)
            edge_labels = {(u, v): f"{d['weight']} cables" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        ax.set_title(f"Incomplete Cables to {selected_room}")
        plt.tight_layout()
        img_base64 = plot_to_base64()
        
        associations = manager.get_room_associations(selected_room)
        assoc_data = [(room, count) for room, count in sorted(associations.items())]
    
    return render_template('plot_with_table.html', img_base64=img_base64, title=f"Incomplete Cables for {selected_room}", associations=assoc_data)

@app.route('/add_cable', methods=['POST'])
def add_cable():
    cable_id = request.form.get('cable_id')
    server_room = request.form.get('server_room')
    server_termination = request.form.get('server_termination')
    device_room = request.form.get('device_room')
    device_type = request.form.get('device_type')
    app_type = request.form.get('app_type')
    cable_type = request.form.get('cable_type')
    fiber_mode = request.form.get('fiber_mode') if cable_type == 'Fiber' else None
    fiber_strands = request.form.get('fiber_strands') if cable_type == 'Fiber' else None
    deliverable_date = request.form.get('deliverable_date') or None
    consumable = request.form.get('consumable') or ConsumableType.NONE.value
    tray_conduit = request.form.get('tray_conduit') or None
    service_loop = request.form.get('service_loop') or 35.0
    room_dims = request.form.get('room_dimensions') or None
    
    try:
        if room_dims:
            width, length = map(float, room_dims.split('x'))
            room_dimensions = (width, length)
        else:
            room_dimensions = None
        fiber_strands = int(fiber_strands) if fiber_strands else None
        service_loop = float(service_loop)
        manager.add_cable(
            cable_id, server_room, server_termination, device_room,
            DeviceType(device_type), ApplicationType(app_type), CableType(cable_type),
            FiberMode(fiber_mode) if fiber_mode else None, fiber_strands, deliverable_date,
            ConsumableType(consumable), tray_conduit, service_loop, room_dimensions
        )
        return redirect(url_for('index'))
    except ValueError as e:
        return render_template('error.html', message=str(e))

@app.route('/update_cable', methods=['POST'])
def update_cable():
    cable_id = request.form.get('cable_id')
    action = request.form.get('action')
    
    try:
        cable = manager._get_cable(cable_id)
        if action == 'verify_schematics' and cable.state == CableState.SCHEMATICS_PENDING:
            manager.verify_schematics(cable_id)
        elif action == 'verify_path' and cable.state == CableState.PATH_VERIFICATION:
            tray_conduit = request.form.get('tray_conduit') or cable.tray_conduit
            manager.verify_path(cable_id, True, tray_conduit)
        elif action == 'record_length' and cable.state == CableState.PATH_MEASURED:
            length_device = float(request.form.get('length_device'))
            length_procore = float(request.form.get('length_procore'))
            room_dims = request.form.get('room_dimensions')
            room_dimensions = None
            if room_dims:
                width, length = map(float, room_dims.split('x'))
                room_dimensions = (width, length)
            manager.record_path_length(cable_id, length_device, length_procore, room_dimensions)
        elif action == 'pull_cable' and cable.state == CableState.CABLE_SELECTED:
            manager.pull_cable(cable_id)
        elif action == 'install_patch_panel' and cable.state == CableState.CABLE_PULLED:
            manager.install_patch_panel(cable_id)
        elif action == 'dress_cable' and cable.state == CableState.PATCH_PANEL_INSTALLED:
            manager.dress_cable(cable_id)
        elif action == 'tone_cable' and cable.state == CableState.CABLE_DRESSED:
            manager.tone_cable(cable_id)
        elif action == 'test_cable' and cable.state == CableState.CABLE_TONED:
            manager.test_cable(cable_id)
        elif action == 'certify_cable' and cable.state == CableState.CABLE_TESTED:
            manager.certify_cable(cable_id)
        elif action == 'complete_installation' and cable.state == CableState.CABLE_CERTIFIED:
            manager.complete_installation(cable_id)
        elif action == 'assign_team':
            team_name = request.form.get('team_name')
            manager.assign_team(cable_id, team_name)
        elif action == 'update_details':
            deliverable_date = request.form.get('deliverable_date') or None
            consumable = request.form.get('consumable') or None
            service_loop = float(request.form.get('service_loop')) if request.form.get('service_loop') else None
            room_dims = request.form.get('room_dimensions') or None
            room_dimensions = None
            if room_dims:
                width, length = map(float, room_dims.split('x'))
                room_dimensions = (width, length)
            manager.update_cable(cable_id, deliverable_date, consumable, service_loop, room_dimensions)
        return redirect(url_for('index'))
    except ValueError as e:
        return render_template('error.html', message=str(e))

@app.route('/schedule_concurrent', methods=['POST'])
def schedule_concurrent():
    cable_id = request.form.get('cable_id')
    try:
        selected_cable = manager._get_cable(cable_id)
        if selected_cable.state != CableState.CABLE_SELECTED or not selected_cable.assigned_team:
            return render_template('error.html', message="Selected cable is not ready for pulling.")
        
        groups = manager.group_cables_by_room()
        concurrent_cables = []
        for (server_room, device_room), cables in groups.items():
            if (server_room == selected_cable.server_room and device_room == selected_cable.device_room):
                concurrent_cables.extend([(c.cable_id, c.resource_needs()) for c in cables if c.cable_id != cable_id])
        
        return render_template('concurrent_pulls.html', cable_id=cable_id, 
                             concurrent_cables=concurrent_cables,
                             title=f"Concurrent Pulls with {cable_id}")
    except ValueError as e:
        return render_template('error.html', message=str(e))

@app.route('/flag_blocking', methods=['POST'])
def flag_blocking():
    threshold = int(request.form.get('threshold') or 10)
    server_room_counts = defaultdict(int)
    for cable in manager.cables:
        if not cable.patch_panel_installed:
            server_room_counts[cable.server_room] += 1
    
    blocking_rooms = [(room, count) for room, count in server_room_counts.items() if count >= threshold]
    
    return render_template('blocking_states.html', blocking_rooms=blocking_rooms, 
                         title="Blocking States", threshold=threshold)

@app.route('/add_column', methods=['POST'])
def add_column():
    new_column = request.form.get('new_column')
    try:
        manager.update_column_config(new_column)
        return redirect(url_for('index'))
    except Exception as e:
        return render_template('error.html', message=str(e))

@app.route('/task_list', methods=['POST'])
def task_list():
    device_rooms = sorted(set(cable.device_room for cable in manager.cables))
    task_data = []
    
    for room in device_rooms:
        cables = [c for c in manager.cables if c.device_room == room and c.state != CableState.INSTALLED_TO_COMPLETION]
        if not cables:
            continue
        length = manager.DEVICE_ROOM_MEASUREMENTS.get(room, {}).get('length', 'Not measured')
        dimensions = manager.DEVICE_ROOM_MEASUREMENTS.get(room, {}).get('dimensions', None)
        dim_str = f"{dimensions[0]}x{dimensions[1]}" if dimensions else "Unknown"
        cables_data = [(c.cable_id, c.server_room, c.state.value, c.assigned_team or 'None') for c in cables]
        task_data.append({
            'room': room,
            'length': length,
            'dimensions': dim_str,
            'warning': dimensions and (dimensions[0] > 30 or dimensions[1] > 30),
            'cables': cables_data
        })
    
    return render_template('task_list.html', task_data=task_data, title="Task List by Device Room")

if __name__ == "__main__":
    app.run(debug=True)