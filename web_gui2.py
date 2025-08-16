from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
from cableManager import CableManager, CableState
import networkx as nx
from collections import defaultdict
import os
from pathlib import Path

app = Flask(__name__)
manager = CableManager()

# Define HTML template content
TEMPLATES = {
    'index.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Cable Management System</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .section { margin-bottom: 20px; }
        select { width: 300px; }
    </style>
</head>
<body>
    <h1>Cable Management System</h1>
    
    <div class="section">
        <h2>Plot Pie Charts for Cables</h2>
        <form action="/plot_pie" method="POST">
            <label for="cable_ids">Select Cable IDs:</label><br>
            <select name="cable_ids" multiple size="10">
                {% for cable_id in cable_ids %}
                    <option value="{{ cable_id }}">{{ cable_id }}</option>
                {% endfor %}
            </select><br><br>
            <input type="submit" value="Plot Pie Charts">
        </form>
    </div>
    
    <div class="section">
        <h2>Plot Incomplete Cable Diagram</h2>
        <form action="/plot_incomplete" method="POST">
            <label for="room">Select Room:</label><br>
            <select name="room">
                {% for room in rooms %}
                    <option value="{{ room }}">{{ room }}</option>
                {% endfor %}
            </select><br><br>
            <input type="submit" value="Show Diagram and Associations">
        </form>
    </div>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'936f9d817f4544fc',t:'MTc0NTc3MDQ5MS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>''',
    'error.html': '''<!DOCTYPE html>
<html>
<head>
    <title>Error</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
    </style>
</head>
<body>
    <h1>Error</h1>
    <p>{{ message }}</p>
    <a href="/">Back to Home</a>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'936f9d818c846734',t:'MTc0NTc3MDQ5MS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>''',
    'plot.html': '''<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        img { max-width: 100%; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <img src="data:image/png;base64,{{ img_base64 }}" alt="Plot">
    <br><br>
    <a href="/">Back to Home</a>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'936f9d8188e6dd1a',t:'MTc0NTc3MDQ5MS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>''',
    'plot_with_table.html': '''<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        img { max-width: 100%; }
        table { border-collapse: collapse; width: 50%; margin-top: 20px; }
        th, td { border: 1px solid black; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
    </style>
</head>
<body>
    <h1>{{ title }}</h1>
    <img src="data:image/png;base64,{{ img_base64 }}" alt="Plot">
    <h2>Associated Rooms</h2>
    <table>
        <tr>
            <th>Associated Room</th>
            <th>Number of Cables</th>
        </tr>
        {% for room, count in associations %}
            <tr>
                <td>{{ room }}</td>
                <td>{{ count }}</td>
            </tr>
        {% endfor %}
    </table>
    <br><br>
    <a href="/">Back to Home</a>
<script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'936f9d805810bd4e',t:'MTc0NTc3MDQ5MS4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body>
</html>'''
}

# Function to create templates directory and files if they don't exist
def ensure_templates():
    templates_dir = Path('templates')
    templates_dir.mkdir(exist_ok=True)
    
    for filename, content in TEMPLATES.items():
        file_path = templates_dir / filename
        if not file_path.exists():
            with file_path.open('w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created template: {file_path}")

# Ensure templates are created before running the app
ensure_templates()

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
    return render_template('index.html', cable_ids=cable_ids, rooms=rooms)

@app.route('/plot_pie', methods=['POST'])
def plot_pie():
    selected_cable_ids = request.form.getlist('cable_ids')
    if not selected_cable_ids:
        return render_template('error.html', message="No cables selected.")
    
    cables = [cable for cable in manager.cables if cable.cable_id in selected_cable_ids]
    n_cables = len(cables)
    ncols = min(n_cables, 5)
    nrows = (n_cables + ncols - 1) // ncols
    fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows), squeeze=False)
    
    for idx, cable in enumerate(cables):
        row = idx // ncols
        col = idx % ncols
        ax = axes[row, col]
        labels, values = cable.pie_chart_data()
        if sum(values) == 0:
            ax.text(0.5, 0.5, 'All Deliverables Complete', horizontalalignment='center', verticalalignment='center')
            ax.axis('equal')
        else:
            colors = ['red' if v == 1 else 'white' for v in values]  # Red for incomplete, white for complete
            ax.pie(values, labels=labels, colors=colors, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', startangle=90)
            ax.axis('equal')
        ax.set_title(f"Cable {cable.cable_id}")
    
    for idx in range(n_cables, nrows * ncols):
        row = idx // ncols
        col = idx % ncols
        axes[row, col].axis('off')
    
    plt.tight_layout()
    img_base64 = plot_to_base64()
    
    return render_template('plot.html', img_base64=img_base64, title="Pie Charts of Deliverables")

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
            for edge in G.edges(data=True):
                src, dst, data = edge
                weight = data["weight"]
                nx.draw_networkx_edges(G, pos, edgelist=[(src, dst)], width=weight * 0.5, ax=ax)
            nx.draw_networkx_labels(G, pos, ax=ax)
            edge_labels = {(u, v): f"{d['weight']} cables" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
        
        ax.set_title(f"Incomplete Cables to {selected_room}")
        plt.tight_layout()
        img_base64 = plot_to_base64()
        
        associations = manager.get_room_associations(selected_room)
        assoc_data = [(room, count) for room, count in sorted(associations.items())]
    
    return render_template('plot_with_table.html', img_base64=img_base64, title=f"Incomplete Cables for {selected_room}", associations=assoc_data)

if __name__ == "__main__":
    app.run(debug=True)