import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
from enum import Enum
from datetime import datetime, datetime as dt
import os
import tkinter as tk
from tkinter import ttk, scrolledtext
from prettytable import PrettyTable
import random
import seaborn as sns
import numpy as np
from collections import defaultdict
import json
import subprocess
import webbrowser

# Define enums
class ApplicationType(Enum):
    AV = "Audio-Visual"
    WAP = "Wireless Access Point"
    CUBICLE = "Cubicle"
    OTHER = "Other"

class CableState(Enum):
    SCHEMATICS_PENDING = "Schematics Pending"
    PATH_VERIFICATION = "Path Verification Pending"
    PATH_MEASURED = "Path Measured"
    CABLE_SELECTED = "Cable Selected"
    CABLE_PULLED = "Cable Pulled"
    PATCH_PANEL_INSTALLED = "Patch Panel Installed"
    CABLE_DRESSED = "Cable Dressed"
    CABLE_TONED = "Cable Toned"
    CABLE_TESTED = "Cable Tested"
    CABLE_CERTIFIED = "Cable Certified"
    INSTALLED_TO_COMPLETION = "Installed to Completion"

class ConsumableType(Enum):
    EXECUTIVE_WALL_PLATE = "Executive Wall Plate"
    SIMPLE_WALL_PLATE = "Simple Wall Plate"
    FOUR_PORT_PLATE = "Four Port Plate"
    TWO_PORT_PLATE = "Two Port Plate"
    NONE = "None"

class CableType(Enum):
    CAT6 = "CAT6"
    GAMECHANGER = "GAMECHANGER"
    FIBER = "Fiber"

class FiberMode(Enum):
    SINGLE = "Single"
    MULTI = "Multi"

class DeviceType(Enum):
    DESKTOP = "Desktop"
    CAMERA = "Camera"
    WAP = "WAP"
    OTHER = "Other"

FIBER_STRANDS = [1, 12, 24, 48, 96, 144, 288]

# Load or initialize configuration file
CONFIG_FILE = "config.json"
DEFAULT_COLUMNS = [
    "Cable ID", "Server Room", "Server Termination", "Device Room", "Device Type",
    "Application Type", "Cable Type", "Fiber Mode", "Fiber Strands", "State",
    "Length (Device)", "Length (Procore)", "Schematics Verified", "Path Exists",
    "Patch Panel Installed", "Assigned Team", "Cable Toned", "Cable Tested",
    "Cable Certified", "Deliverable Date", "Consumable", "Tray/Conduit", "Timestamp",
    "Service Loop", "Room Dimensions"
]

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            if set(DEFAULT_COLUMNS).issubset(set(config["columns"])):
                return config
            else:
                print("Warning: config.json missing some default columns. Recreating with DEFAULT_COLUMNS.")
        except Exception as e:
            print(f"Error reading config.json: {e}. Recreating with DEFAULT_COLUMNS.")
    config = {"columns": DEFAULT_COLUMNS}
    save_config(config)
    return config

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

# Store device room measurements (worst-case length to farthest edge)
DEVICE_ROOM_MEASUREMENTS = {}  # Format: {device_room: {"length": float, "dimensions": (width, length)}}

# CableRun class
class CableRun:
    def __init__(self, cable_id, server_room, server_termination, device_room, device_type, application_type, cable_type, fiber_mode=None, fiber_strands=None, deliverable_date=None, consumable=ConsumableType.NONE, tray_conduit=None, service_loop=35.0, room_dimensions=None, **kwargs):
        if not isinstance(application_type, ApplicationType):
            raise ValueError("Invalid application type")
        if not isinstance(cable_type, CableType):
            raise ValueError("Invalid cable type")
        if not isinstance(consumable, ConsumableType):
            raise ValueError("Invalid consumable type")
        if not isinstance(device_type, DeviceType):
            raise ValueError("Invalid device type")
        if cable_type == CableType.FIBER:
            if not isinstance(fiber_mode, FiberMode):
                raise ValueError("Fiber mode must be specified for fiber cables")
            if fiber_strands not in FIBER_STRANDS:
                raise ValueError(f"Fiber strands must be one of {FIBER_STRANDS}")
        if not isinstance(service_loop, (int, float)) or service_loop < 0:
            raise ValueError("Service loop must be a non-negative number")
        if room_dimensions and not (isinstance(room_dimensions, tuple) and len(room_dimensions) == 2 and all(isinstance(d, (int, float)) and d > 0 for d in room_dimensions)):
            raise ValueError("Room dimensions must be a tuple of two positive numbers (width, length)")
        self.cable_id = cable_id
        self.server_room = server_room
        self.server_termination = server_termination
        self.device_room = device_room
        self.device_type = device_type
        self.application_type = application_type
        self.cable_type = cable_type
        self.fiber_mode = fiber_mode
        self.fiber_strands = fiber_strands
        self.state = CableState.SCHEMATICS_PENDING
        self.path_exists = False
        self.path_length_device = None
        self.path_length_procore = None
        self.schematics_verified = False
        self.patch_panel_installed = False
        self.assigned_team = None
        self.cable_toned = False
        self.cable_tested = False
        self.cable_certified = False
        self.deliverable_date = deliverable_date
        self.consumable = consumable
        self.tray_conduit = tray_conduit
        self.service_loop = float(service_loop)
        self.room_dimensions = room_dimensions
        self.timestamp = datetime.now()
        self.custom_fields = kwargs

    def to_tuple(self):
        config = load_config()
        data = [
            self.cable_id,
            self.server_room,
            self.server_termination,
            self.device_room,
            self.device_type.value,
            self.application_type.value,
            self.cable_type.value,
            self.fiber_mode.value if self.fiber_mode else None,
            self.fiber_strands,
            self.state.value,
            self.path_length_device,
            self.path_length_procore,
            self.schematics_verified,
            self.path_exists,
            self.patch_panel_installed,
            self.assigned_team,
            self.cable_toned,
            self.cable_tested,
            self.cable_certified,
            self.deliverable_date,
            self.consumable.value,
            self.tray_conduit,
            self.timestamp,
            self.service_loop,
            f"{self.room_dimensions[0]}x{self.room_dimensions[1]}" if self.room_dimensions else None
        ]
        for col in config["columns"]:
            if col not in DEFAULT_COLUMNS:
                data.append(self.custom_fields.get(col, None))
        return tuple(data)

    def completion_percentage(self):
        total_steps = len(CableState)
        state_order = list(CableState).index(self.state)
        return (state_order + 1) / total_steps * 100

    def pie_chart_data(self):
        deliverables = [
            ("Verify Schematics", self.schematics_verified),
            ("Verify Path Existence", self.path_exists),
            ("Measure Length (Device)", self.path_length_device is not None and self.path_length_device > 0),
            ("Measure Length (Procore)", self.path_length_procore is not None and self.path_length_procore > 0),
            ("Select Cable", self.state in [CableState.CABLE_SELECTED, CableState.CABLE_PULLED, CableState.PATCH_PANEL_INSTALLED, CableState.CABLE_DRESSED, CableState.CABLE_TONED, CableState.CABLE_TESTED, CableState.CABLE_CERTIFIED, CableState.INSTALLED_TO_COMPLETION]),
            ("Install Patch Panel", self.patch_panel_installed),
            ("Assign Team", self.assigned_team is not None),
            ("Tone Cable", self.cable_toned),
            ("Test Cable", self.cable_tested),
            ("Certify Cable", self.cable_certified),
            ("Complete Installation", self.state == CableState.INSTALLED_TO_COMPLETION),
    ]
        labels = [d[0] for d in deliverables]
        values = [0 if d[1] else 1 for d in deliverables]  # 0 for completed, 1 for incomplete
        return labels, values

    def remaining_deliverables(self):
        deliverables = [d[0] for d, completed in [
            ("Verify Schematics", self.schematics_verified),
            ("Verify Path Existence", self.path_exists),
            ("Measure Length (Device)", self.path_length_device is not None and self.path_length_device > 0),
            ("Measure Length (Procore)", self.path_length_procore is not None and self.path_length_procore > 0),
            ("Select Cable", self.state in [CableState.CABLE_SELECTED, CableState.CABLE_PULLED, CableState.PATCH_PANEL_INSTALLED, CableState.CABLE_DRESSED, CableState.CABLE_TONED, CableState.CABLE_TESTED, CableState.CABLE_CERTIFIED, CableState.INSTALLED_TO_COMPLETION]),
            ("Install Patch Panel", self.patch_panel_installed),
            ("Assign Team", self.assigned_team is not None),
            ("Tone Cable", self.cable_toned),
            ("Test Cable", self.cable_tested),
            ("Certify Cable", self.cable_certified),
            ("Complete Installation", self.state == CableState.INSTALLED_TO_COMPLETION),
    ] if not completed]
        return deliverables if deliverables else ["None"]

    def resource_needs(self):
        if self.path_length_device is None:
            return 1
        return min(5, max(1, int(self.path_length_device // 20)))

# CableManager class
class CableManager:
    def __init__(self, csv_file="datacenter_cables.csv"):
        self.cables = []
        self.csv_file = csv_file
        self.load_from_csv()

    def add_cable(self, cable_id, server_room, server_termination, device_room, device_type, application_type, cable_type, fiber_mode=None, fiber_strands=None, deliverable_date=None, consumable=ConsumableType.NONE, tray_conduit=None, service_loop=35.0, room_dimensions=None, **kwargs):
        cable = CableRun(cable_id, server_room, server_termination, device_room, device_type, application_type, cable_type, fiber_mode, fiber_strands, deliverable_date, consumable, tray_conduit, service_loop, room_dimensions, **kwargs)
        self.cables.append(cable)
        self.save_to_csv()
        return cable

    def verify_schematics(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.SCHEMATICS_PENDING:
            cable.schematics_verified = True
            cable.state = CableState.PATH_VERIFICATION
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not in schematics pending state")

    def verify_path(self, cable_id, path_exists, tray_conduit=None):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.PATH_VERIFICATION and cable.schematics_verified:
            cable.path_exists = path_exists
            if path_exists:
                cable.tray_conduit = tray_conduit
                cable.state = CableState.PATH_MEASURED
                cable.timestamp = datetime.now()
                self.save_to_csv()
            else:
                raise ValueError(f"Path for cable {cable_id} does not exist")
        else:
            raise ValueError(f"Cable {cable_id} is not ready for path verification")

    def record_path_length(self, cable_id, length_device, length_procore, room_dimensions=None):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.PATH_MEASURED and cable.path_exists:
            # Check room dimensions
            if room_dimensions:
                if not (isinstance(room_dimensions, tuple) and len(room_dimensions) == 2 and all(isinstance(d, (int, float)) and d > 0 for d in room_dimensions)):
                    raise ValueError("Room dimensions must be a tuple of two positive numbers (width, length)")
                width, length = room_dimensions
                if width > 30 or length > 30:
                    print(f"WARNING: Device room {cable.device_room} dimensions {width}x{length} ft exceed 30x30 ft.")
                cable.room_dimensions = room_dimensions
                DEVICE_ROOM_MEASUREMENTS[cable.device_room] = {"length": length_device, "dimensions": room_dimensions}
            elif cable.device_room in DEVICE_ROOM_MEASUREMENTS:
                length_device = DEVICE_ROOM_MEASUREMENTS[cable.device_room]["length"]
                cable.room_dimensions = DEVICE_ROOM_MEASUREMENTS[cable.device_room]["dimensions"]
                width, length = cable.room_dimensions
                if width > 30 or length > 30:
                    print(f"WARNING: Device room {cable.device_room} dimensions {width}x{length} ft exceed 30x30 ft.")
            else:
                raise ValueError(f"No room dimensions provided for {cable.device_room}, and no prior measurement exists.")

            # Check length against other cables
            device_room_lengths = [
                c.path_length_device for c in self.cables
                if c.device_room == cable.device_room and c.path_length_device is not None and c.cable_id != cable_id
            ]
            if device_room_lengths:
                min_length = min(device_room_lengths)
                max_allowed_length = min_length * 1.35
                if length_device > max_allowed_length:
                    print(f"ERROR: Cable {cable_id} length {length_device} ft exceeds 35% of shortest cable to {cable.device_room} ({min_length} ft). Max allowed: {max_allowed_length:.2f} ft.")
                    return
            if length_procore > 0:
                diff_percent = abs(length_device - length_procore) / length_procore * 100
                if diff_percent > 10:
                    print(f"WARNING: Cable {cable_id} length discrepancy: Device={length_device} ft, Procore={length_procore} ft, Difference={diff_percent:.2f}%")
            if cable.cable_type == CableType.CAT6 and length_device > 290:
                cable.cable_type = CableType.GAMECHANGER
                cable.timestamp = datetime.now()
                print(f"Cable {cable_id} changed to GAMECHANGER due to length {length_device} ft > 290 ft")
            cable.path_length_device = length_device
            cable.path_length_procore = length_procore
            cable.state = CableState.CABLE_SELECTED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for length recording")

    def pull_cable(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.CABLE_SELECTED and cable.path_length_device and cable.assigned_team and cable.schematics_verified:
            cable.state = CableState.CABLE_PULLED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for pulling")

    def install_patch_panel(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.CABLE_PULLED:
            cable.patch_panel_installed = True
            cable.state = CableState.PATCH_PANEL_INSTALLED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for patch panel installation")

    def dress_cable(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.PATCH_PANEL_INSTALLED and cable.patch_panel_installed:
            cable.state = CableState.CABLE_DRESSED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for dressing")

    def tone_cable(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.CABLE_DRESSED:
            cable.cable_toned = True
            cable.state = CableState.CABLE_TONED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for toning")

    def test_cable(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.CABLE_TONED and cable.cable_toned:
            cable.cable_tested = True
            cable.state = CableState.CABLE_TESTED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for testing")

    def certify_cable(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.CABLE_TESTED and cable.cable_tested:
            cable.cable_certified = True
            cable.state = CableState.CABLE_CERTIFIED
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for certification")

    def complete_installation(self, cable_id):
        cable = self._get_cable(cable_id)
        if cable.state == CableState.CABLE_CERTIFIED and cable.cable_certified:
            cable.state = CableState.INSTALLED_TO_COMPLETION
            cable.timestamp = datetime.now()
            self.save_to_csv()
        else:
            raise ValueError(f"Cable {cable_id} is not ready for completion")

    def assign_team(self, cable_id, team_name):
        cable = self._get_cable(cable_id)
        cable.assigned_team = team_name
        self.save_to_csv()

    def update_cable(self, cable_id, deliverable_date=None, consumable=None, service_loop=None, room_dimensions=None, **kwargs):
        cable = self._get_cable(cable_id)
        if deliverable_date:
            try:
                cable.deliverable_date = dt.strptime(deliverable_date, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD")
        if consumable:
            if consumable in [c.value for c in ConsumableType]:
                cable.consumable = ConsumableType(consumable)
            else:
                raise ValueError(f"Invalid consumable type. Choose from {[c.value for c in ConsumableType]}")
        if service_loop is not None:
            if not isinstance(service_loop, (int, float)) or service_loop < 0:
                raise ValueError("Service loop must be a non-negative number")
            cable.service_loop = float(service_loop)
        if room_dimensions:
            if not (isinstance(room_dimensions, tuple) and len(room_dimensions) == 2 and all(isinstance(d, (int, float)) and d > 0 for d in room_dimensions)):
                raise ValueError("Room dimensions must be a tuple of two positive numbers (width, length)")
            cable.room_dimensions = room_dimensions
            if cable.device_room in DEVICE_ROOM_MEASUREMENTS:
                DEVICE_ROOM_MEASUREMENTS[cable.device_room]["dimensions"] = room_dimensions
        for key, value in kwargs.items():
            cable.custom_fields[key] = value
        self.save_to_csv()

    def _get_cable(self, cable_id):
        for cable in self.cables:
            if cable.cable_id == cable_id:
                return cable
        raise ValueError(f"Cable {cable_id} not found")

    def search_cables(self, partial_id=""):
        if not partial_id:
            return self.cables
        return [cable for cable in self.cables if partial_id.lower() in cable.cable_id.lower()]

    def to_dataframe(self):
        config = load_config()
        data = [cable.to_tuple() for cable in self.cables]
        try:
            return pd.DataFrame(data, columns=config["columns"])
        except ValueError as e:
            print(f"Error creating DataFrame: {e}")
            print(f"Expected columns: {config['columns']}")
            print(f"Data columns: {len(data[0]) if data else 0}")
            raise

    def save_to_csv(self):
        df = self.to_dataframe()
        df.to_csv(self.csv_file, index=False)

    def load_from_csv(self):
        if os.path.exists(self.csv_file):
            try:
                df = pd.read_csv(self.csv_file)
                config = load_config()
                for col in config["columns"]:
                    if col not in df.columns:
                        print(f"Warning: Column '{col}' missing in CSV. Adding with default values.")
                        if col == "Service Loop":
                            df[col] = 35.0
                        elif col == "Room Dimensions":
                            df[col] = None
                        else:
                            df[col] = None
                self.cables = []
                for _, row in df.iterrows():
                    kwargs = {col: row[col] for col in config["columns"] if col not in DEFAULT_COLUMNS and pd.notnull(row[col])}
                    try:
                        # Handle NaN or invalid Consumable
                        consumable = row["Consumable"]
                        if pd.isna(consumable) or consumable not in [c.value for c in ConsumableType]:
                            consumable = ConsumableType.NONE
                        else:
                            consumable = ConsumableType(consumable)
                        # Parse room dimensions
                        room_dims = None
                        if pd.notnull(row["Room Dimensions"]):
                            try:
                                width, length = map(float, row["Room Dimensions"].split('x'))
                                room_dims = (width, length)
                            except Exception as e:
                                print(f"Warning: Invalid room dimensions for cable {row.get('Cable ID', 'Unknown')}: {row['Room Dimensions']}")
                        cable = CableRun(
                            cable_id=row["Cable ID"],
                            server_room=row["Server Room"],
                            server_termination=row["Server Termination"],
                            device_room=row["Device Room"],
                            device_type=DeviceType(row["Device Type"]),
                            application_type=ApplicationType(row["Application Type"]),
                            cable_type=CableType(row["Cable Type"]),
                            fiber_mode=FiberMode(row["Fiber Mode"]) if pd.notnull(row["Fiber Mode"]) else None,
                            fiber_strands=int(row["Fiber Strands"]) if pd.notnull(row["Fiber Strands"]) else None,
                            deliverable_date=row["Deliverable Date"],
                            consumable=consumable,
                            tray_conduit=row["Tray/Conduit"] if pd.notnull(row["Tray/Conduit"]) else None,
                            service_loop=float(row["Service Loop"]) if pd.notnull(row["Service Loop"]) else 35.0,
                            room_dimensions=room_dims,
                            **kwargs
                        )
                        cable.state = CableState(row["State"])
                        cable.path_length_device = row["Length (Device)"] if pd.notnull(row["Length (Device)"]) else None
                        cable.path_length_procore = row["Length (Procore)"] if pd.notnull(row["Length (Procore)"]) else None
                        cable.schematics_verified = row["Schematics Verified"] if pd.notnull(row["Schematics Verified"]) else False
                        cable.path_exists = row["Path Exists"] if pd.notnull(row["Path Exists"]) else False
                        cable.patch_panel_installed = row["Patch Panel Installed"] if pd.notnull(row["Patch Panel Installed"]) else False
                        cable.assigned_team = row["Assigned Team"] if pd.notnull(row["Assigned Team"]) else None
                        cable.cable_toned = row["Cable Toned"] if pd.notnull(row["Cable Toned"]) else False
                        cable.cable_tested = row["Cable Tested"] if pd.notnull(row["Cable Tested"]) else False
                        cable.cable_certified = row["Cable Certified"] if pd.notnull(row["Cable Certified"]) else False
                        cable.deliverable_date = pd.to_datetime(row["Deliverable Date"]).date() if pd.notnull(row["Deliverable Date"]) else None
                        cable.timestamp = pd.to_datetime(row["Timestamp"]) if pd.notnull(row["Timestamp"]) else datetime.now()
                        self.cables.append(cable)
                        # Update DEVICE_ROOM_MEASUREMENTS if applicable
                        if cable.device_room not in DEVICE_ROOM_MEASUREMENTS and cable.path_length_device and cable.room_dimensions:
                            DEVICE_ROOM_MEASUREMENTS[cable.device_room] = {
                                "length": cable.path_length_device,
                                "dimensions": cable.room_dimensions
                            }
                    except Exception as e:
                        print(f"Error loading cable {row.get('Cable ID', 'Unknown')}: {e}")
            except Exception as e:
                print(f"Error loading CSV: {e}")
                self.cables = []

    def display_table(self, sort_by=None, display_type="terminal", page=1, page_size=50):
        df = self.to_dataframe()
        if sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by)
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        df_page = df.iloc[start_idx:end_idx]
        
        if display_type == "terminal":
            table = PrettyTable()
            table.field_names = df.columns
            for _, row in df_page.iterrows():
                table.add_row([row[col] for col in df.columns])
            print(f"Page {page} of {(len(df) + page_size - 1) // page_size}")
            print(table)
        else:
            root = tk.Tk()
            root.title(f"Cable List - Page {page}")
            tree = ttk.Treeview(root, columns=list(df.columns), show="headings")
            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, width=100)
            for _, row in df_page.iterrows():
                tree.insert("", tk.END, values=[row[col] for col in df.columns])
            
            frame = tk.Frame(root)
            frame.pack()
            tk.Button(frame, text="Previous", command=lambda: root.destroy() or self.display_table(sort_by, "popup", page-1, page_size) if page > 1 else None).pack(side=tk.LEFT)
            tk.Button(frame, text="Next", command=lambda: root.destroy() or self.display_table(sort_by, "popup", page+1, page_size) if end_idx < len(df) else None).pack(side=tk.LEFT)
            
            tree.pack(expand=True, fill="both")
            root.mainloop()

    def display_remaining_deliverables(self, display_type="terminal", sort_by=None, filter_deliverable=None, page=1, page_size=50, export_csv=False):
        data = []
        for cable in self.cables:
            remaining = cable.remaining_deliverables()
            if filter_deliverable and filter_deliverable not in remaining and remaining != ["None"]:
                continue
            data.append({
                "Cable ID": cable.cable_id,
                "Remaining Deliverables": ", ".join(remaining) if remaining else "None",
                "Num Remaining": len(remaining) if remaining else 0
            })
        
        df = pd.DataFrame(data)
        if sort_by == "Num Remaining":
            df = df.sort_values(by="Num Remaining")
        elif sort_by and sort_by in df.columns:
            df = df.sort_values(by=sort_by)
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        df_page = df.iloc[start_idx:end_idx]
        
        if export_csv:
            df.to_csv("remaining_deliverables.csv", index=False)
            print("Exported to remaining_deliverables.csv")
        
        if display_type == "terminal":
            table = PrettyTable()
            table.field_names = ["Cable ID", "Remaining Deliverables", "Num Remaining"]
            for _, row in df_page.iterrows():
                table.add_row([row["Cable ID"], row["Remaining Deliverables"], row["Num Remaining"]])
            print(f"Page {page} of {(len(df) + page_size - 1) // page_size}")
            print(table)
        else:
            root = tk.Tk()
            root.title(f"Remaining Deliverables - Page {page}")
            tree = ttk.Treeview(root, columns=["Cable ID", "Remaining Deliverables", "Num Remaining"], show="headings")
            for col in ["Cable ID", "Remaining Deliverables", "Num Remaining"]:
                tree.heading(col, text=col)
                tree.column(col, width=200 if col == "Remaining Deliverables" else 100)
            for _, row in df_page.iterrows():
                tree.insert("", tk.END, values=[row["Cable ID"], row["Remaining Deliverables"], row["Num Remaining"]])
            
            frame = tk.Frame(root)
            frame.pack()
            tk.Button(frame, text="Previous", command=lambda: root.destroy() or self.display_remaining_deliverables(display_type, sort_by, filter_deliverable, page-1, page_size, False) if page > 1 else None).pack(side=tk.LEFT)
            tk.Button(frame, text="Next", command=lambda: root.destroy() or self.display_remaining_deliverables(display_type, sort_by, filter_deliverable, page+1, page_size, False) if end_idx < len(df) else None).pack(side=tk.LEFT)
            
            tree.pack(expand=True, fill="both")
            root.mainloop()

    def group_cables_by_room(self):
        groups = defaultdict(list)
        for cable in self.cables:
            if (cable.state == CableState.CABLE_SELECTED and
                cable.assigned_team and
                cable.schematics_verified and
                cable.path_length_device and
                cable.tray_conduit):
                groups[(cable.server_room, cable.device_room)].append(cable)
        return groups

    def schedule_concurrent_pulls(self):
        groups = self.group_cables_by_room()
        if not groups:
            print("No cables ready for concurrent pulling.")
            return
        
        table = PrettyTable()
        table.field_names = ["Server Room", "Device Room", "Cable IDs", "Total Cables", "Total Resources Needed"]
        for (server_room, device_room), cables in groups.items():
            cable_ids = [c.cable_id for c in cables]
            total_resources = sum(c.resource_needs() for c in cables)
            table.add_row([server_room, device_room, ", ".join(cable_ids), len(cables), total_resources])
        
        print("\nConcurrent Pull Schedule by Server Room and Device Room:")
        print(table)
        
        execute = input("Execute these pulls? (y/n): ").lower() == 'y'
        if execute:
            for (server_room, device_room), cables in groups.items():
                for cable in cables:
                    try:
                        self.pull_cable(cable.cable_id)
                        print(f"Pulled cable {cable.cable_id} from {server_room} to {device_room}")
                    except ValueError as e:
                        print(f"Error pulling cable {cable.cable_id}: {e}")

    def flag_blocking_states(self, threshold=10):
        server_room_counts = defaultdict(int)
        for cable in self.cables:
            if not cable.patch_panel_installed:
                server_room_counts[cable.server_room] += 1
        
        blocking_rooms = []
        for room, count in server_room_counts.items():
            if count >= threshold:
                blocking_rooms.append((room, count))
        
        if blocking_rooms:
            print("\nBlocking States: Patch Panel Installation Needed")
            table = PrettyTable()
            table.field_names = ["Server Room", "Cables Without Patch Panel"]
            for room, count in blocking_rooms:
                table.add_row([room, count])
            print(table)
        else:
            print("\nNo server rooms with significant patch panel blocking states.")
    def plot_completion(self):
        deliverables = [
            "Verify Schematics",
            "Verify Path Existence",
            "Measure Length (Device)",
            "Measure Length (Procore)",
            "Select Cable",
            "Install Patch Panel",
            "Assign Team",
            "Tone Cable",
            "Test Cable",
            "Certify Cable",
            "Complete Installation"
    ]
        num_deliverables = len(deliverables)
        segment_height = 1.0 / num_deliverables
        
        cable_ids = [cable.cable_id for cable in self.cables]
        num_cables = len(cable_ids)
        bottom = np.zeros(num_cables)
        
        plt.figure(figsize=(12, 8))
        
        for i, deliverable in enumerate(deliverables):
            heights = []
            colors = []
            for cable in self.cables:
                labels, values = cable.pie_chart_data()
                deliverable_idx = labels.index(deliverable)
                is_completed = values[deliverable_idx] == 0  # 0 means completed
                heights.append(segment_height if is_completed else 0)
                colors.append('C%d' % i if is_completed else 'lightgrey')
            
            plt.bar(cable_ids, heights, bottom=bottom, color=colors, label=deliverable)
            bottom += np.array(heights)
        
        plt.ylim(0, 1)
        plt.xlabel("Cable ID")
        plt.ylabel("Completion Progress")
        plt.title("Cable Completion by Deliverable (0 to 1)")
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_pie_chart(self, cables):
        if not cables:
            print("No cables found for plotting.")
            return
        
        cables_to_plot = cables[:10] if len(cables) > 10 else cables
        if len(cables) > 10:
            print(f"Plotting pie charts for the first 10 of {len(cables)} cables.")
        
        n_cables = len(cables_to_plot)
        ncols = min(n_cables, 5)
        nrows = (n_cables + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols, figsize=(4 * ncols, 4 * nrows), squeeze=False)
        
        for idx, cable in enumerate(cables_to_plot):
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
        plt.show()

    def plot_deliverables_graph(self):
        G = nx.DiGraph()
        
        for cable in self.cables:
            remaining = self.remaining_deliverables()
            G.add_node(cable.cable_id, type="cable")
            for deliverable in remaining:
                G.add_node(deliverable, type="deliverable")
                G.add_edge(cable.cable_id, deliverable)
        
        pos = nx.spring_layout(G)
        plt.figure(figsize=(12, 8))
        
        cable_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "cable"]
        deliverable_nodes = [n for n, d in G.nodes(data=True) if d["type"] == "deliverable"]
        
        nx.draw_networkx_nodes(G, pos, nodelist=cable_nodes, node_color="lightblue", node_shape="o", node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=deliverable_nodes, node_color="lightgreen", node_shape="s", node_size=500)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, pos)
        
        plt.title("Directed Graph of Cables and Remaining Deliverables")
        plt.show()

    def plot_resource_heatmap(self):
        df = self.to_dataframe()
        df["Resource Needs"] = [cable.resource_needs() for cable in self.cables]
        
        plt.figure(figsize=(12, 8))
        pivot_server = df.pivot_table(values="Resource Needs", index="Cable ID", columns="Server Room", aggfunc="max", fill_value=0)
        sns.heatmap(pivot_server, cmap="YlOrRd", annot=True, fmt="d")
        plt.title("Resource Needs Heatmap by Server Room (Hotter = More Resources)")
        plt.xlabel("Server Room")
        plt.ylabel("Cable ID")
        plt.show()
        
        plt.figure(figsize=(12, 8))
        pivot_device = df.pivot_table(values="Resource Needs", index="Cable ID", columns="Device Room", aggfunc="max", fill_value=0)
        sns.heatmap(pivot_device, cmap="YlOrRd", annot=True, fmt="d")
        plt.title("Resource Needs Heatmap by Device Room (Hotter = More Resources)")
        plt.xlabel("Device Room")
        plt.ylabel("Cable ID")
        plt.show()

    def plot_incomplete_cable_diagram(self):
        server_rooms = sorted(set(cable.server_room for cable in self.cables))
        if not server_rooms:
            print("No server rooms found.")
            return
        
        fig, axes = plt.subplots(len(server_rooms), 1, figsize=(10, 5 * len(server_rooms)), squeeze=False)
        
        for idx, server_room in enumerate(server_rooms):
            ax = axes[idx][0]
            G = nx.DiGraph()
            edge_counts = defaultdict(int)
            
            for cable in self.cables:
                if cable.server_room == server_room and cable.state != CableState.INSTALLED_TO_COMPLETION:
                    edge = (server_room, cable.device_room)
                    edge_counts[edge] += 1
                    G.add_edge(server_room, cable.device_room, weight=edge_counts[edge])
            
            if not G.edges:
                ax.text(0.5, 0.5, f'No incomplete cables from {server_room}', horizontalalignment='center', verticalalignment='center')
                ax.axis('off')
                ax.set_title(f"{server_room} Incomplete Cables")
                continue
            
            pos = nx.spring_layout(G)
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color="lightblue", node_size=500)
            
            for edge in G.edges(data=True):
                src, dst, data = edge
                weight = data["weight"]
                nx.draw_networkx_edges(G, pos, edgelist=[(src, dst)], width=weight * 0.5, ax=ax)
            
            nx.draw_networkx_labels(G, pos, ax=ax)
            
            edge_labels = {(u, v): f"{d['weight']} cables" for u, v, d in G.edges(data=True)}
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
            
            ax.set_title(f"{server_room} Incomplete Cables")
        
        plt.tight_layout()
        plt.show()

    def get_room_associations(self, selected_room):
        associations = defaultdict(int)
        is_server_room = any(cable.server_room == selected_room for cable in self.cables)
        
        if is_server_room:
            for cable in self.cables:
                if cable.server_room == selected_room and cable.state != CableState.INSTALLED_TO_COMPLETION:
                    associations[cable.device_room] += 1
        else:
            for cable in self.cables:
                if cable.device_room == selected_room and cable.state != CableState.INSTALLED_TO_COMPLETION:
                    associations[cable.server_room] += 1
        
        return associations

    def generate_task_list(self):
        device_rooms = sorted(set(cable.device_room for cable in self.cables))
        if not device_rooms:
            print("No device rooms found.")
            return
        
        print("\nTask List for Cable Runs by Device Room:")
        for room in device_rooms:
            cables = [c for c in self.cables if c.device_room == room and c.state != CableState.INSTALLED_TO_COMPLETION]
            if not cables:
                continue
            length = DEVICE_ROOM_MEASUREMENTS.get(room, {}).get("length", "Not measured")
            dimensions = DEVICE_ROOM_MEASUREMENTS.get(room, {}).get("dimensions", None)
            dim_str = f"{dimensions[0]}x{dimensions[1]}" if dimensions else "Unknown"
            print(f"\nDevice Room: {room}")
            print(f"Worst-case Length: {length} ft")
            print(f"Dimensions: {dim_str}")
            if dimensions and (dimensions[0] > 30 or dimensions[1] > 30):
                print(f"WARNING: Room dimensions {dim_str} ft exceed 30x30 ft.")
            table = PrettyTable()
            table.field_names = ["Cable ID", "Server Room", "State", "Assigned Team"]
            for cable in cables:
                table.add_row([cable.cable_id, cable.server_room, cable.state.value, cable.assigned_team or "None"])
            print(table)

    def update_column_config(self, new_column):
        config = load_config()
        if new_column not in config["columns"]:
            config["columns"].append(new_column)
            save_config(config)
            print(f"Added new column '{new_column}' to configuration")
            for cable in self.cables:
                cable.custom_fields[new_column] = None
            self.save_to_csv()
        else:
            print(f"Column '{new_column}' already exists")

    def initialize_cables(self, num_cables=500):
        if self.cables:
            return
        app_types = list(ApplicationType)
        consumables = list(ConsumableType)
        cable_types = [CableType.CAT6, CableType.FIBER]
        fiber_modes = list(FiberMode)
        device_types = list(DeviceType)
        teams = ["Team A", "Team B", "Team C", "Team D", None]
        states = list(CableState)
        server_rooms = ["SR1", "SR2"]
        device_rooms = [f"Room {i}" for i in range(1, 11)]
        trays = [f"Tray {i}" for i in range(1, 5)]
        suffixes = ['ap', 'wap', 'desk', 'cam']
        # Predefined room dimensions (width, length) in feet
        room_dimensions = {f"Room {i}": (random.randint(20, 40), random.randint(20, 40)) for i in range(1, 11)}
        
        for i in range(num_cables):
            idf_num = random.randint(1, 5)
            section = random.randint(1, 10)
            rack = random.randint(1, 10)
            port = random.randint(100, 999)
            suffix = random.choice(suffixes)
            cable_id = f"IDF{idf_num}-{section:02d}-{rack:02d}-{port}-{suffix}"
            
            server_room = random.choice(server_rooms)
            server_termination = f"SwitchPort{random.randint(1, 48)}"
            device_room = random.choice(device_rooms)
            device_type = random.choice(device_types)
            app_type = random.choice(app_types)
            cable_type = random.choice(cable_types)
            fiber_mode = random.choice(fiber_modes) if cable_type == CableType.FIBER else None
            fiber_strands = random.choice(FIBER_STRANDS) if cable_type == CableType.FIBER else None
            deliverable_date = f"2025-{random.randint(5, 12):02d}-{random.randint(1, 28):02d}"
            consumable = random.choice(consumables)
            tray_conduit = random.choice(trays)
            service_loop = 35.0
            room_dims = room_dimensions[device_room]
            
            cable = self.add_cable(cable_id, server_room, server_termination, device_room, device_type, app_type, cable_type, fiber_mode, fiber_strands, deliverable_date, consumable, tray_conduit, service_loop, room_dims)
            
            if random.choice([True, False]):
                self.assign_team(cable_id, random.choice(teams) or "Team X")
            
            target_state = random.choice(states)
            try:
                if target_state != CableState.SCHEMATICS_PENDING:
                    self.verify_schematics(cable_id)
                if target_state in states[states.index(CableState.PATH_VERIFICATION):]:
                    self.verify_path(cable_id, True, cable.tray_conduit)
                if target_state in states[states.index(CableState.PATH_MEASURED):]:
                    base_length = random.uniform(100, 300)
                    if device_room not in DEVICE_ROOM_MEASUREMENTS:
                        DEVICE_ROOM_MEASUREMENTS[device_room] = {"length": base_length, "dimensions": room_dims}
                    else:
                        base_length = DEVICE_ROOM_MEASUREMENTS[device_room]["length"]
                    device_room_lengths = [
                        c.path_length_device for c in self.cables
                        if c.device_room == device_room and c.path_length_device is not None
                    ]
                    min_length = min(device_room_lengths) if device_room_lengths else base_length
                    max_allowed_length = min_length * 1.35
                    length = min(base_length, max_allowed_length)
                    procore_length = length * random.uniform(0.85, 1.15)
                    self.record_path_length(cable_id, length, procore_length)
                if target_state in states[states.index(CableState.CABLE_PULLED):] and cable.assigned_team:
                    self.pull_cable(cable_id)
                if target_state in states[states.index(CableState.PATCH_PANEL_INSTALLED):]:
                    self.install_patch_panel(cable_id)
                if target_state in states[states.index(CableState.CABLE_DRESSED):]:
                    self.dress_cable(cable_id)
                if target_state in states[states.index(CableState.CABLE_TONED):]:
                    self.tone_cable(cable_id)
                if target_state in states[states.index(CableState.CABLE_TESTED):]:
                    self.test_cable(cable_id)
                if target_state in states[states.index(CableState.CABLE_CERTIFIED):]:
                    self.certify_cable(cable_id)
                if target_state == CableState.INSTALLED_TO_COMPLETION:
                    self.complete_installation(cable_id)
            except ValueError:
                pass

# Interactive program loop
def main():
    manager = CableManager()
    
    manager.initialize_cables(500)

    deliverables = [
        "Verify Schematics", "Verify Path Existence", "Measure Length (Device)", "Measure Length (Procore)",
        "Select Cable", "Install Patch Panel", "Assign Team",
        "Tone Cable", "Test Cable", "Certify Cable", "Complete Installation"
]

    sort_options = {
        "1": "Cable ID",
        "2": "Server Room",
        "3": "Server Termination",
        "4": "Device Room",
        "5": "Device Type",
        "6": "Application Type",
        "7": "Cable Type",
        "8": "Fiber Mode",
        "9": "Fiber Strands",
        "10": "State",
        "11": "Length (Device)",
        "12": "Length (Procore)",
        "13": "Schematics Verified",
        "14": "Path Exists",
        "15": "Patch Panel Installed",
        "16": "Assigned Team",
        "17": "Cable Toned",
        "18": "Cable Tested",
        "19": "Cable Certified",
        "20": "Deliverable Date",
        "21": "Consumable",
        "22": "Tray/Conduit",
        "23": "Timestamp",
        "24": "Service Loop",
        "25": "Room Dimensions"
    }

    while True:
        print("\nCable Management System")
        print("1. Add new cable")
        print("2. Update cable state")
        print("3. Update deliverable date, consumable, service loop, or room dimensions")
        print("4. Assign team")
        print("5. Plot completion graph")
        print("6. Plot pie charts for cables")
        print("7. Display cable table")
        print("8. Display remaining deliverables")
        print("9. Plot deliverables graph")
        print("10. Plot resource heatmaps")
        print("11. Schedule concurrent cable pulls")
        print("12. Flag blocking states")
        print("13. Add new column to spreadsheet")
        print("14. Plot incomplete cable diagram")
        print("15. Display room associations")
        print("16. Generate task list for cable runs")
        print("17. Launch web interface")
        print("18. Exit")
        choice = input("Enter choice (1-18): ")

        if choice == "1":
            cable_id = input("Enter Cable ID (e.g., IDF1-01-01-111-ap): ")
            server_room = input("Enter Server Room (e.g., SR1): ")
            server_termination = input("Enter Server Termination (e.g., SwitchPort1): ")
            device_room = input("Enter Device Room (e.g., Room 1): ")
            device_type = input(f"Enter Device Type {[t.value for t in DeviceType]}: ")
            app_type = input(f"Enter Application Type {[t.value for t in ApplicationType]}: ")
            cable_type = input(f"Enter Cable Type {[t.value for t in CableType if t != CableType.GAMECHANGER]}: ")
            fiber_mode = None
            fiber_strands = None
            if cable_type == CableType.FIBER.value:
                fiber_mode = input(f"Enter Fiber Mode {[m.value for m in FiberMode]}: ")
                fiber_strands = input(f"Enter Fiber Strands {FIBER_STRANDS}: ")
                try:
                    fiber_strands = int(fiber_strands)
                    if fiber_strands not in FIBER_STRANDS:
                        raise ValueError(f"Fiber strands must be one of {FIBER_STRANDS}")
                except ValueError as e:
                    print(f"Error: {e}")
                    continue
            deliverable_date = input("Enter Deliverable Date (YYYY-MM-DD, or press Enter to skip): ")
            consumable = input(f"Enter Consumable Type {[c.value for c in ConsumableType]} (or press Enter for None): ")
            tray_conduit = input("Enter Tray/Conduit (e.g., Tray 1, or press Enter to skip): ")
            service_loop = input("Enter Service Loop (feet, default 35, or press Enter for default): ")
            room_dims = input("Enter Room Dimensions (width x length in feet, e.g., 25x30, or press Enter to skip): ")
            room_dimensions = None
            if room_dims:
                try:
                    width, length = map(float, room_dims.split('x'))
                    room_dimensions = (width, length)
                except ValueError:
                    print("Error: Room dimensions must be in format 'width x length' (e.g., 25x30)")
                    continue
            config = load_config()
            custom_fields = {}
            for col in config["columns"]:
                if col not in DEFAULT_COLUMNS:
                    value = input(f"Enter value for {col} (or press Enter to skip): ")
                    custom_fields[col] = value if value else None
            try:
                device_type = DeviceType(device_type)
                app_type = ApplicationType(app_type)
                cable_type = CableType(cable_type)
                if cable_type == CableType.GAMECHANGER:
                    raise ValueError("GAMECHANGER cable can only be set automatically for CAT6 cables over 290 feet")
                fiber_mode = FiberMode(fiber_mode) if fiber_mode else None
                consumable = ConsumableType(consumable) if consumable else ConsumableType.NONE
                deliverable_date = deliverable_date if deliverable_date else None
                tray_conduit = tray_conduit if tray_conduit else None
                service_loop = float(service_loop) if service_loop else 35.0
                manager.add_cable(cable_id, server_room, server_termination, device_room, device_type, app_type, cable_type, fiber_mode, fiber_strands, deliverable_date, consumable, tray_conduit, service_loop, room_dimensions, **custom_fields)
                print(f"Cable {cable_id} added")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            cable_id = input("Enter Cable ID to update: ")
            try:
                cable = manager._get_cable(cable_id)
                print(f"Current state: {cable.state.value}, Cable Type: {cable.cable_type.value}")
                if cable.state == CableState.SCHEMATICS_PENDING:
                    manager.verify_schematics(cable_id)
                    print("Schematics verified")
                elif cable.state == CableState.PATH_VERIFICATION:
                    path_exists = input("Does path exist? (y/n): ").lower() == 'y'
                    tray_conduit = input("Enter Tray/Conduit (e.g., Tray 1): ") if path_exists else None
                    manager.verify_path(cable_id, path_exists, tray_conduit)
                    print("Path verified")
                elif cable.state == CableState.PATH_MEASURED:
                    length_device = float(input("Enter length measured to farthest edge of device room (feet): "))
                    length_procore = float(input("Enter length from Procore (feet): "))
                    room_dims = input("Enter Room Dimensions (width x length in feet, e.g., 25x30, or press Enter if already set): ")
                    room_dimensions = None
                    if room_dims:
                        try:
                            width, length = map(float, room_dims.split('x'))
                            room_dimensions = (width, length)
                        except ValueError:
                            print("Error: Room dimensions must be in format 'width x length' (e.g., 25x30)")
                            continue
                    manager.record_path_length(cable_id, length_device, length_procore, room_dimensions)
                    print(f"Path length recorded, Cable Type: {cable.cable_type.value}")
                elif cable.state == CableState.CABLE_SELECTED:
                    manager.pull_cable(cable_id)
                    print("Cable pulled")
                elif cable.state == CableState.CABLE_PULLED:
                    manager.install_patch_panel(cable_id)
                    print("Patch panel installed")
                elif cable.state == CableState.PATCH_PANEL_INSTALLED:
                    manager.dress_cable(cable_id)
                    print("Cable dressed")
                elif cable.state == CableState.CABLE_DRESSED:
                    manager.tone_cable(cable_id)
                    print("Cable toned")
                elif cable.state == CableState.CABLE_TONED:
                    manager.test_cable(cable_id)
                    print("Cable tested")
                elif cable.state == CableState.CABLE_TESTED:
                    manager.certify_cable(cable_id)
                    print("Cable certified")
                elif cable.state == CableState.CABLE_CERTIFIED:
                    manager.complete_installation(cable_id)
                    print("Cable installed to completion")
                else:
                    print("Cable is already installed to completion")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "3":
            cable_id = input("Enter Cable ID to update: ")
            deliverable_date = input("Enter new Deliverable Date (YYYY-MM-DD, or press Enter to skip): ")
            consumable = input(f"Enter new Consumable Type {[c.value for c in ConsumableType]} (or press Enter for None): ")
            service_loop = input("Enter new Service Loop (feet, or press Enter to skip): ")
            room_dims = input("Enter new Room Dimensions (width x length in feet, e.g., 25x30, or press Enter to skip): ")
            room_dimensions = None
            if room_dims:
                try:
                    width, length = map(float, room_dims.split('x'))
                    room_dimensions = (width, length)
                except ValueError:
                    print("Error: Room dimensions must be in format 'width x length' (e.g., 25x30)")
                    continue
            config = load_config()
            custom_fields = {}
            for col in config["columns"]:
                if col not in DEFAULT_COLUMNS:
                    value = input(f"Enter new value for {col} (or press Enter to skip): ")
                    custom_fields[col] = value if value else None
            try:
                deliverable_date = deliverable_date if deliverable_date else None
                consumable = consumable if consumable else None
                service_loop = float(service_loop) if service_loop else None
                manager.update_cable(cable_id, deliverable_date, consumable, service_loop, room_dimensions, **custom_fields)
                print(f"Cable {cable_id} updated")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            cable_id = input("Enter Cable ID to assign team: ")
            team_name = input("Enter team name: ")
            try:
                manager.assign_team(cable_id, team_name)
                print(f"Team {team_name} assigned to Cable {cable_id}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "5":
            try:
                manager.plot_completion()
            except Exception as e:
                print(f"Error plotting completion graph: {e}")

        elif choice == "6":
            partial_id = input("Enter partial Cable ID to search (e.g., IDF1, ap, or press Enter for all cables): ")
            try:
                matching_cables = manager.search_cables(partial_id)
                print(f"Found {len(matching_cables)} matching cables.")
                manager.plot_pie_chart(matching_cables)
            except Exception as e:
                print(f"Error plotting pie charts: {e}")

        elif choice == "7":
            display_type = input("Display table in terminal or popup? (terminal/popup): ").lower()
            if display_type not in ["terminal", "popup"]:
                print("Invalid display type. Using terminal.")
                display_type = "terminal"
            config = load_config()
            print("Sort options:")
            for i, col in enumerate(config["columns"], 1):
                print(f"{i}. {col}")
            sort_choice = input("Enter sort option number (or press Enter for no sorting): ")
            sort_by = config["columns"][int(sort_choice) - 1] if sort_choice and sort_choice.isdigit() and int(sort_choice) <= len(config["columns"]) else None
            page = int(input("Enter page number (1 or higher): ") or 1)
            try:
                manager.display_table(sort_by=sort_by, display_type=display_type, page=page)
            except Exception as e:
                print(f"Error displaying table: {e}")

        elif choice == "8":
            display_type = input("Display remaining deliverables in terminal or popup? (terminal/popup): ").lower()
            if display_type not in ["terminal", "popup"]:
                print("Invalid display type. Using terminal.")
                display_type = "terminal"
            print("Sort options:")
            print("1. Cable ID")
            print("2. Remaining Deliverables")
            print("3. Num Remaining")
            sort_choice = input("Enter sort option number (1-3, or press Enter for no sorting): ")
            sort_by = {"1": "Cable ID", "2": "Remaining Deliverables", "3": "Num Remaining"}.get(sort_choice)
            filter_deliverable = input(f"Enter deliverable to filter by {deliverables} (or press Enter for no filter): ")
            if filter_deliverable and filter_deliverable not in deliverables:
                print(f"Invalid deliverable. Available: {deliverables}")
                filter_deliverable = None
            page = int(input("Enter page number (1 or higher): ") or 1)
            export_csv = input("Export to CSV? (y/n): ").lower() == 'y'
            try:
                manager.display_remaining_deliverables(display_type, sort_by, filter_deliverable, page, export_csv=export_csv)
            except Exception as e:
                print(f"Error displaying remaining deliverables: {e}")

        elif choice == "9":
            try:
                manager.plot_deliverables_graph()
            except Exception as e:
                print(f"Error plotting deliverables graph: {e}")

        elif choice == "10":
            try:
                manager.plot_resource_heatmap()
            except Exception as e:
                print(f"Error plotting resource heatmap: {e}")

        elif choice == "11":
            try:
                manager.schedule_concurrent_pulls()
            except Exception as e:
                print(f"Error scheduling concurrent pulls: {e}")

        elif choice == "12":
            try:
                threshold = int(input("Enter threshold for cables without patch panel (default 10): ") or 10)
                manager.flag_blocking_states(threshold)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "13":
            new_column = input("Enter new column name: ")
            try:
                manager.update_column_config(new_column)
            except Exception as e:
                print(f"Error adding column: {e}")

        elif choice == "14":
            try:
                manager.plot_incomplete_cable_diagram()
            except Exception as e:
                print(f"Error plotting incomplete cable diagram: {e}")

        elif choice == "15":
            room = input("Enter room name (e.g., SR1, Room 1): ")
            try:
                associations = manager.get_room_associations(room)
                if not associations:
                    print(f"No incomplete cable associations found for {room}.")
                else:
                    print(f"\nIncomplete cable associations for {room}:")
                    table = PrettyTable()
                    table.field_names = ["Associated Room", "Number of Cables"]
                    for assoc_room, count in sorted(associations.items()):
                        table.add_row([assoc_room, count])
                    print(table)
            except Exception as e:
                print(f"Error displaying room associations: {e}")

        elif choice == "16":
            try:
                manager.generate_task_list()
            except Exception as e:
                print(f"Error generating task list: {e}")

        elif choice == "17":
            try:
                print("Launching web interface at http://127.0.0.1:5000/")
                subprocess.run(["python", "web_gui.py"])
                webbrowser.open("http://127.0.0.1:5000/")
            except Exception as e:
                print(f"Error launching web interface: {e}")
                print("Ensure web_gui.py is in the same directory and Flask is installed.")

        elif choice == "18":
            print("Exiting...")
            break

        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()