import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

class Cable:
    def __init__(self, name, start_point, segments):
        """
        Initialize a cable with a name, starting point, and list of segments.
        segments: List of tuples (direction, length, elevation_change)
        direction: 'N', 'S', 'E', 'W'
        length: Horizontal distance in units
        elevation_change: Change in z-coordinate (positive for up, negative for down)
        """
        self.name = name
        self.start_point = np.array(start_point, dtype=float)
        self.segments = segments
        self.points = [self.start_point]

        # Calculate all points along the cable path
        current_point = self.start_point.copy()
        for direction, length, elevation in segments:
            if direction == 'N':
                delta = np.array([0, length, elevation])
            elif direction == 'S':
                delta = np.array([0, -length, elevation])
            elif direction == 'E':
                delta = np.array([length, 0, elevation])
            elif direction == 'W':
                delta = np.array([-length, 0, elevation])
            else:
                raise ValueError(f"Invalid direction: {direction}")
            current_point = current_point + delta
            self.points.append(current_point.copy())

        self.points = np.array(self.points)

    def get_plot_data(self):
        """Return x, y, z coordinates for plotting."""
        return self.points[:, 0], self.points[:, 1], self.points[:, 2]

class DatacenterModel:
    def __init__(self):
        self.cables = []
        self.shapes = []

    def add_cable(self, name, start_point, segments):
        """Add a cable to the model."""
        if len(segments) > 4:
            raise ValueError("Cable cannot have more than 4 bends")
        cable = Cable(name, start_point, segments)
        self.cables.append(cable)

    def add_shape(self, name, vertices):
        """
        Add a 2D shape at a given z-level (base of shape at z=0 unless specified).
        vertices: List of (x, y, z) coordinates, closed loop assumed.
        """
        self.shapes.append({'name': name, 'vertices': np.array(vertices)})

    def plot(self):
        """Visualize the datacenter model in 3D."""
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Plot shapes
        for shape in self.shapes:
            vertices = shape['vertices']
            # Close the loop by appending the first vertex
            vertices = np.vstack([vertices, vertices[0]])
            ax.plot(vertices[:, 0], vertices[:, 1], vertices[:, 2], 'b-', alpha=0.5, label=shape['name'])

        # Plot cables
        colors = plt.cm.tab10(np.linspace(0, 1, len(self.cables)))
        for cable, color in zip(self.cables, colors):
            x, y, z = cable.get_plot_data()
            ax.plot(x, y, z, color=color, label=cable.name, linewidth=2)

        # Set labels and legend
        ax.set_xlabel('X (East-West)')
        ax.set_ylabel('Y (North-South)')
        ax.set_zlabel('Z (Elevation)')
        ax.legend()
        ax.set_title('Datacenter Cable Model')
        
        # Equal scaling
        max_range = np.array([ax.get_xlim(), ax.get_ylim(), ax.get_zlim()]).ptp(axis=1).max()
        mid_x = np.mean(ax.get_xlim())
        mid_y = np.mean(ax.get_ylim())
        mid_z = np.mean(ax.get_zlim())
        ax.set_xlim(mid_x - max_range/2, mid_x + max_range/2)
        ax.set_ylim(mid_y - max_range/2, mid_y + max_range/2)
        ax.set_zlim(mid_z - max_range/2, mid_z + max_range/2)

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

    # Add a pentagon-shaped room (like the Pentagon building)
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

    # Add some example cables
    model.add_cable(
        "Fiber1",
        start_point=[0, 0, 1],
        segments=[
            ('E', 5, 0),      # Move 5 units East
            ('N', 3, 2),      # Move 3 units North, up 2 units
            ('W', 4, 0),      # Move 4 units West
            ('S', 2, -1),     # Move 2 units South, down 1 unit
        ]
    )

    model.add_cable(
        "Power1",
        start_point=[15, 0, 1],
        segments=[
            ('N', 4, 0),
            ('E', 10, 3),
            ('S', 3, 0),
        ]
    )

    # Plot the model
    model.plot()