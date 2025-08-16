import asyncio
import platform
import pygame
import random
from collections import defaultdict
from cableManager import CableManager, CableState

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Datacenter Cable Management Game")
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)

# Fonts
font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 16)

# Initialize CableManager
manager = CableManager()

# Node positions (server rooms and device rooms)
nodes = {}
edges = defaultdict(list)  # (server_room, device_room) -> [cable]
node_positions = {}
buttons = []  # Task buttons

def setup():
    global nodes, edges, node_positions, buttons
    # Collect server rooms and device rooms
    server_rooms = set(cable.server_room for cable in manager.cables if cable.state != CableState.INSTALLED_TO_COMPLETION)
    device_rooms = set(cable.device_room for cable in manager.cables if cable.state != CableState.INSTALLED_TO_COMPLETION)
    nodes = {room: "server" for room in server_rooms}
    nodes.update({room: "device" for room in device_rooms})

    # Group cables by (server_room, device_room)
    for cable in manager.cables:
        if cable.state != CableState.INSTALLED_TO_COMPLETION:
            edges[(cable.server_room, cable.device_room)].append(cable)

    # Assign positions to nodes
    num_nodes = len(nodes)
    radius = min(WIDTH, HEIGHT) * 0.3
    center_x, center_y = WIDTH * 0.3, HEIGHT * 0.5
    for i, node in enumerate(nodes):
        angle = 2 * 3.14159 * i / num_nodes
        x = center_x + radius * random.uniform(0.8, 1.2) * (1 if nodes[node] == "server" else -1)
        y = center_y + radius * random.uniform(0.8, 1.2) * (1 if i % 2 == 0 else -1)
        node_positions[node] = (x, y)

    # Create task buttons
    buttons.clear()
    y_offset = 50
    for (server_room, device_room), cables in edges.items():
        deliverables = defaultdict(list)
        total_length = sum(cable.path_length_device or 0 for cable in cables)
        for cable in cables:
            for deliverable in cable.remaining_deliverables():
                deliverables[deliverable].append(cable)
        for deliverable, del_cables in deliverables.items():
            text = f"{device_room} -> {server_room}: {deliverable} ({len(del_cables)} cables, {total_length:.1f} ft)"
            button = {
                "rect": pygame.Rect(WIDTH * 0.6, y_offset, 500, 40),
                "text": text,
                "deliverable": deliverable,
                "cables": del_cables,
                "server_room": server_room,
                "device_room": device_room
            }
            buttons.append(button)
            y_offset += 50

def draw_node(x, y, label, node_type):
    color = BLUE if node_type == "server" else GREEN
    pygame.draw.circle(screen, color, (x, y), 20)
    text = small_font.render(label, True, BLACK)
    screen.blit(text, (x - text.get_width() // 2, y - 30))

def draw_edge(start_pos, end_pos, thickness, tooltip_text, mouse_pos):
    pygame.draw.line(screen, BLACK, start_pos, end_pos, thickness)
    # Check if mouse is near the edge
    line_vec = (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1])
    mouse_vec = (mouse_pos[0] - start_pos[0], mouse_pos[1] - start_pos[1])
    line_len = (line_vec[0]**2 + line_vec[1]**2)**0.5
    if line_len == 0:
        return
    proj = (mouse_vec[0] * line_vec[0] + mouse_vec[1] * line_vec[1]) / line_len
    if 0 < proj < line_len:
        closest_point = (
            start_pos[0] + (proj / line_len) * line_vec[0],
            start_pos[1] + (proj / line_len) * line_vec[1]
        )
        dist = ((mouse_pos[0] - closest_point[0])**2 + (mouse_pos[1] - closest_point[1])**2)**0.5
        if dist < 10:
            text = small_font.render(tooltip_text, True, BLACK)
            pygame.draw.rect(screen, WHITE, (mouse_pos[0], mouse_pos[1], text.get_width() + 10, text.get_height() + 10))
            screen.blit(text, (mouse_pos[0] + 5, mouse_pos[1] + 5))

def draw_button(button, hovered):
    color = GRAY if not hovered else RED
    pygame.draw.rect(screen, color, button["rect"])
    text = font.render(button["text"], True, BLACK)
    screen.blit(text, (button["rect"].x + 10, button["rect"].y + 10))

def update_loop():
    mouse_pos = pygame.mouse.get_pos()
    screen.fill(WHITE)

    # Draw edges
    for (server_room, device_room), cables in edges.items():
        if server_room in node_positions and device_room in node_positions:
            thickness = len(cables) * 2
            tooltip = f"Cables: {', '.join(c.cable_id for c in cables)}, Total Length: {sum(c.path_length_device or 0 for c in cables):.1f} ft"
            draw_edge(node_positions[server_room], node_positions[device_room], thickness, tooltip, mouse_pos)

    # Draw nodes
    for node, node_type in nodes.items():
        if node in node_positions:
            draw_node(node_positions[node][0], node_positions[node][1], node, node_type)

    # Draw buttons
    for button in buttons:
        hovered = button["rect"].collidepoint(mouse_pos)
        draw_button(button, hovered)

    pygame.display.flip()

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    for cable in button["cables"]:
                        try:
                            if cable.state == CableState.SCHEMATICS_PENDING and button["deliverable"] == "Verify Schematics":
                                manager.verify_schematics(cable.cable_id)
                            elif cable.state == CableState.PATH_VERIFICATION and button["deliverable"] == "Verify Path Existence":
                                manager.verify_path(cable.cable_id, True, cable.tray_conduit)
                            elif cable.state == CableState.PATH_MEASURED and button["deliverable"] == "Measure Length (Device)":
                                manager.record_path_length(cable.cable_id, cable.path_length_device or 100, cable.path_length_procore or 100, cable.room_dimensions)
                            elif cable.state == CableState.CABLE_SELECTED and button["deliverable"] == "Select Cable":
                                manager.pull_cable(cable.cable_id)
                            elif cable.state == CableState.CABLE_PULLED and button["deliverable"] == "Install Patch Panel":
                                manager.install_patch_panel(cable.cable_id)
                            elif cable.state == CableState.PATCH_PANEL_INSTALLED and button["deliverable"] == "Tone Cable":
                                manager.dress_cable(cable.cable_id)
                                manager.tone_cable(cable.cable_id)
                            elif cable.state == CableState.CABLE_TONED and button["deliverable"] == "Test Cable":
                                manager.test_cable(cable.cable_id)
                            elif cable.state == CableState.CABLE_TESTED and button["deliverable"] == "Certify Cable":
                                manager.certify_cable(cable.cable_id)
                            elif cable.state == CableState.CABLE_CERTIFIED and button["deliverable"] == "Complete Installation":
                                manager.complete_installation(cable.cable_id)
                        except ValueError as e:
                            print(f"Error updating {cable.cable_id}: {e}")
                    setup()  # Refresh display after task acceptance

async def main():
    setup()
    while True:
        update_loop()
        await asyncio.sleep(1.0 / FPS)

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())