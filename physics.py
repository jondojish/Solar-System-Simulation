from  math import sqrt

def sign(x):
    if x == 0:
        return 0
    if x > 1:
        return 1
    return -1


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @classmethod
    def sum(cls, v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y)

    @classmethod
    def dot_product(cls, v1, v2):
        return v1.x * v2.x + v1.y * v2.y

    @classmethod
    def are_parallel(cls, v1, v2):
        if v2.x != 0:
            return v2.y * (v1.x / v2.x) == v1.y
        elif v2.y != 0:
            return v2.x * (v1.y / v2.y) == v1.x
        else:
            return v1.x == 0 and v1.y == 0

    @classmethod
    def same_direction(cls, v1, v2):
        if (
            Vector.are_parallel(v1, v2)
            and sign(v1.x * v2.x) in [0, 1]
            and sign(v1.y * v2.y) in [0, 1]
        ):
            return True
        return False

    def to_string(self):
        return f"{self.x}, {self.y}"
    
    def get_unit(self):
        return Vector(self.x, self.y).multiply(1 / self.get_magnitude())
    
    def get_component(self, v):
        v = v.get_unit()
        return v.multiply(
            Vector.dot_product(self, v)
        )  # component of velocity perpandiculare to impulse

    def get_perpandicular(self):
        return Vector(-self.y, self.x)

    def get_tuple(self):
        return (self.x, self.y)

    def negative(self):
        return Vector(-self.x, -self.y)

    def add(self, v):
        self.x += v.x
        self.y += v.y

    def add(self, v):
        self.x += v.x
        self.y += v.y

    def get_magnitude(self):
        return sqrt(self.x**2 + self.y**2)

    

    def multiply(self, x, inplace=False):
        if inplace:
            self.x *= x
            self.y *= x
            return self
        else:
            return Vector(self.x, self.y).multiply(x, inplace=True)


class Body:
    bodies = []
    metres_per_pixel = 1
    G = 6.67 * 10**-11
    x = False
    def __init__(self, radius=1, mass=1, pos=Vector(0, 0), vel=Vector(0, 0), color="white"):
        self.radius = radius
        self.pos = pos
        self.mass = mass
        self.vel = vel
        self.force = Vector(0, 0)
        self.add_body(self)
        self.last_collision = self
        self.display_pos = pos
        self.color = color
    
    @classmethod
    def set_metres_per_pixel(cls, x):
        cls.metres_per_pixel = x

    @classmethod
    def update(cls, dt):
        if not cls.x:
            for b1 in cls.bodies:
                b1.set_force(Vector(0, 0))
                for b2 in cls.bodies:
                    if b1 != b2:
                        if Vector.sum(b1.pos, b2.pos.negative()).get_magnitude()< b1.radius + b2.radius:
                            cls.x = True
                            print("done")
                            print(1/ 0)
                        b1.add_force(cls.get_gravity(b1, b2))
                print("accel", b1.get_accel().multiply(dt).to_string())
                b1.vel.add(b1.get_accel().multiply(dt))
                print("vel", b1.vel.to_string())
                b1.pos.add(b1.vel.multiply(dt))
                b1.display_pos.add(b1.vel.multiply(dt).multiply(1 / cls.metres_per_pixel))
        else:
            cls.x = True
            
            

    @classmethod
    def add_body(cls, body):
        cls.bodies.append(body)

    @classmethod
    def remove_body(cls, body):
        cls.bodies.remove(body)

    def get_gravity(self, body):
        # F = -GMm/(r^2) 
        magnitude = (self.G * self.mass * body.mass) / ((Vector.sum(self.pos, body.pos.negative()).get_magnitude()) ** 2)
        direction = Vector.sum(body.pos, self.pos.negative()).get_unit()
        return direction.multiply(magnitude)

    def set_velocity(self, v):
        self.vel = v

    def get_accel(self):
        return self.force.multiply(1 / self.mass)

    def set_force(self, force: Vector):
        self.force = force

    def add_force(self, force):
        self.force.add(force)

    def get_converted_coords(self, ratio):
        return (self.pos.x * ratio, self.pos.y * ratio)



