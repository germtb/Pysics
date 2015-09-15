from math import sqrt

MASS_0 = 100  # [kg]
dt = 0.1
mass = MASS_0
distance = 0

max_distance = 5000    # [m]
total_distance = max_distance
temperature = 300  # [K]
molecular_mass = 0.044  # [kg]
ideal_gas_constant = 8.31  # [?]
exhaust_velocity = sqrt(temperature * ideal_gas_constant / molecular_mass)

speed = 120 * 1000 / 3600  # [m/s]
duration = total_distance / speed

for _ in range(0, 100000):
    distance += dt * speed
    min_thrust = 3.2 * mass  # [N]
    delta_mass = min_thrust / exhaust_velocity
    mass -= delta_mass * dt
    print("delta mass: " + str(delta_mass) + " kg / s")

    if distance >= max_distance:
        print("Simulation succesful")
        break

    if mass <= 0:
        raise Exception("Mass smaller than 0")

    if _ == 99999:
        raise Exception("Not enough iterations")

print("Exhaust velocity: " + str(exhaust_velocity) + " m/s")
print("delta mass: " + str(delta_mass) + " kg / s")

print("Propellant mass: " + str(MASS_0 - mass) + " kg")
print("Payload mass: " + str(mass))
