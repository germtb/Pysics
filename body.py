class Body:

    @property
    def momentum(self):
        return self.mass * self.velocity

    @property
    def angular_momentum(self):
        return self.mass * self.angular_velocity

    @property
    def radius(self):
        return self.position.module

    @property
    def radius2(self):
        return self.position.module2

    @property
    def speed(self):
        return self.velocity.module

    @property
    def speed2(self):
        return self.velocity.module2

    @property
    def direction(self):
        return self.velocity.unit

    @property
    def radial_speed(self):
        return self.velocity.dot(self.position.unit)

    @property
    def angular_velocity(self):
        return self.position.cross(self.velocity)

    @property
    def linear_angular_velocity(self):
        return self.position.cross(self.velocity) / self.radius

    @property
    def linear_angular_speed(self):
        return self.linear_angular_velocity.module

    def __init__(self, position, velocity, mass):
        self.position = position
        self.velocity = velocity
        self.mass = mass

    def copy(self):
        return Body(self.position.copy(), self.velocity.copy(), self.mass)

    def __str__(self):
        return "(position: " + str(self.position) \
               + ", velocity:" + str(self.velocity) \
               + ", mass: " + str(self.mass) + ")"

    def __eq__(self, other):
        return self.position == other.position \
            and self.velocity == other.velocity \
            and self.mass == other.mass


class ShapedBody(Body):

    def __init__(self, position, velocity, mass, area, c_drag, r_nose):
        super().__init__(position, velocity, mass)
        self.area = area
        self.c_drag = c_drag
        self.r_nose = r_nose

    def copy(self):
        return ShapedBody(self.position.copy(),
                          self.velocity.copy(),
                          self.mass,
                          self.area,
                          self.c_drag,
                          self.r_nose)
