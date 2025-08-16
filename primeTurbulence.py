import numpy as np
from fipy import Grid2D, CellVariable, TransientTerm, DiffusionTerm, Viewer
import random



# Function to generate quasi-random noise based on primes
def prime_quasi_random_noise(size):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Example primes
    noise = np.zeros(size)
    for i in range(size):
        noise[i] = primes[i % len(primes)]
    return noise

# Define the grid and initial conditions
nx = 50
ny = 50
dx = 1.0
dy = 1.0
mesh = Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

# Define the variables (velocity, pressure, etc.)
velocity = CellVariable(name="velocity", mesh=mesh, value=0.0)
pressure = CellVariable(name="pressure", mesh=mesh, value=0.0)

# Adding noise to initial conditions
initial_noise = prime_quasi_random_noise(nx * ny)
velocity.value = initial_noise.reshape((nx, ny))

# Define the equations (simplified example, real equations are more complex)
velocity_eq = TransientTerm() == DiffusionTerm(coeff=1.0)
pressure_eq = TransientTerm() == DiffusionTerm(coeff=1.0)

# Solve the equations
time_step = 0.1
steps = 100
for step in range(steps):
    velocity_eq.solve(var=velocity, dt=time_step)
    pressure_eq.solve(var=pressure, dt=time_step)

    # Visualization (optional)
    if step % 10 == 0:
        viewer = Viewer(vars=(velocity, pressure))
        viewer.plot()