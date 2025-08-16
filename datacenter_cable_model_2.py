import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv
import os

class Cable:
    def __init__(self, name, cable_type, start_point, segments):
        """
        Initialize a cable with a name, type, starting point, and segments.
        cable_type: 'fiber', 'copper', 'GCcopper'
        segments: List of tuples (direction, length, elevation_change)
        direction: 'N', 'S', 'E', 'W'
        length: Horizontal distance in feet
        elevation_change: Change in z-coordinate (positive for up, negative for down)
        """
        self.name = name
        self.cable_type = cable_type
        self.start_point = np.array(start_point, dtype=float)
        self.segments = segments
        self.points = [self.start_point]

        # Validate cable length based on type
        max_lengths = {'fiber': 1000, 'copper': 299, 'GCcopper': 599}
        min_lengths = {'fiber': 0, 'copper': 0, 'GCcopper': 300}
        total_length = sum(segment[1] for segment in segments)  # Sum of horizontal lengths
        if not (min_lengths[cable_type] <= total_length <= max_lengths[cable_type]):
            raise ValueError(
                f"Invalid length {total_length}' for {cable_type}. "
                f"Must be between {min_lengths[cable_type]}' and {max_lengths[cable_type]}'."
            )

        # Calculate all points along the cable path
        current_point = self.start_point.copy()
        for direction, length, elevation in segments:
            if direction not in ['N', 'S', 'E', 'W']:
                raise ValueError(f"Invalid direction: {direction}")
            if direction == 'N':
                delta = np.array([0, length, elevation])
            elif direction == 'S':
                delta = np.array([0, -length, elevation])
            elif direction == 'E':
                delta = np.array([length, 0, elevation])
            elif direction == 'W':
                delta = np.array([-length, 0, elevation])
            current_point = current_point + delta
            self.points.append(current_point.copy())

        self.points = np.array(self.points)

    def get_plot_data(self):
        """Return x, y, z coordinates for plotting."""
        return self.points[:, 0], self.points[:, 1], self.points[:, 2]

    def get_color(self):
        """Return color based on cable type."""
        colors = {
            'fiber': 'red',      # Red for fiber
            'copper': 'blue',     # Blue for copper
            'GCcopper': 'green'   # Green for GCcopper
        }
        return colors.get(self.cable_type, 'black')

class DatacenterModel:
    def __init__(self):
        self.objects = []
        self.shapes = []

    def add_cable(self, name, cable_type, start_point, segments):
        """Add a cable to the model."""
        if len(segments) > 4:
            raise ValueError("Cable cannot have more than 4 bends")
        cable = Cable(name, cable_type, start_point, segments)
        self.objects.append(cable)

    def add_shape(self, name, vertices):
        """
        Add a 2D shape at a given z-level (base of shape at z=0 unless specified).
        vertices: List of (x, y, z) coordinates, closed loop assumed.
        """
        self.shapes.append({'name': name, 'vertices': np.array(vertices)})

    def load_cables_from_csv(self, csv_file):
        """Load cables from a CSV file."""
        if not os.path.exists(csv_file):
            raise FileNotFoundError(f"CSV file {csv_file} not found.")
        
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            required_columns = ['name', 'cable_type', 'start_x', 'start_y', 'start_z']
            for i in range(1, 5):
                required_columns.extend([f'segment{i}_direction', f'segment{i}_length', f'segment{i}_elevation'])
            for col in required_columns[:5]:
                if col not in reader.fieldnames:
                    raise ValueError(f"Missing required column: {col}")

            for row in reader:
                name = row['name']
                cable_type = row['cable_type'].lower()
                if cable_type not in ['fiber', 'copper', 'GCcopper']:
                    raise ValueError(f"Invalid cable type {cable_type} in CSV for cable {name}")
                
                start_point = [
                    float(row['start_x']),
                    float(row['start_y']),
                    float(row['start_z'])
                ]
                
                segments = []
                for i in range(1, 5):
                    direction = row.get(f'segment{i}_direction', '').strip()
                    if not direction:
                        break  # Stop if no more segments
                    length = float(row[f'segment{i}_length'])
                    elevation = float(row[f'segment{i}_elevation'])
                    segments.append((direction, length, elevation))
                
                if not segments:
                    raise ValueError(f"No segments defined for cable {name}")
                
                self.add_cable(name, cable_type, start_point, segments)

    def plot(self):
        """Visualize the datacenter model in 3D."""
        fig = plt.figure(figsize=(12, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Plot shapes with shaded fill
        for shape in self.shapes:
            vertices = shape['vertices']
            # Close the loop by appending the first vertex
            vertices_closed = np.vstack([vertices, vertices[0]])
            ax.plot(vertices_closed[:, 0], vertices_closed[:, 1], vertices_closed[:, 2], 
                    'b-', alpha=0.8, label=shape['name'])
            # Shade the shape with a light fill
            ax.fill(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
                    'blue', alpha=0.1)

        # Plot cables with index
        for idx, cable in enumerate(self.cables, 1):
            x, y, z = cable.get_plot_data()
            label = f"{idx}: {cable.name} ({cable.cable_type})"
            ax.plot(x, y, z, color=cable.get_color(), label=label, linewidth=2)

        # Set labels and legend
        ax.set_xlabel('X (East-West, feet)')
        ax.set_ylabel('Y (North-South, feet)')
        ax.set_zlabel('Z (Elevation, feet)')
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
        ax.set_title('Datacenter Cable Model')
        
        # Equal scaling
        max_range = np.array([ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]).ptp(axis=1).max()
        mid_x = np.mean(ax.get_xlim())
        mid_y = np.mean(ax.get_ylim())
        mid_z = np.mean(ax.get_zlim())
        ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
        ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
        ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)

        plt.tight_layout()
        plt.show()

def create_pentagon_vertices(center, radius, z=0):
    """Generate vertices for a pentagon shape."""
    angles = np.linspace(0, 2*np.pi, 6)[:-1]  # 5 points
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    z = np.full_like(x, z)
    return np.column_stack((x, y, z))

# Example usage
if __name__ == "__main__":
    model = DatacenterModel()

    # Add a pentagon-shaped room
    pentagon_center = (0, 0)
    pentagon_radius = 10
    pentagon_vertices = create_pentagon_vertices(pentagon_center, pentagon_radius)
    model.add_shape("Pentagon Room", pentagon_vertices)

    # Add a rectangular room
    rect_vertices = [
        (15, 5, 0),
        (15, -5, 0),
        (25, -5, 0),
        (25, 5, 0),
    ]
    model.add_shape("Rectangular Room", rect_vertices)

    # Load cables from CSV
    csv_file = "cables.csv"
    try:
        model.load_cables_from_csv(csv_file)
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found. Please create it with the required format.")
    except Exception as e:
        print(f"Error loading CSV: {e}")

    # Plot the model
    model.plot()