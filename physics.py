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
        self.name = ""
    
    @classmethod
    def set_metres_per_pixel(cls, x):
        cls.metres_per_pixel = x

    # @classmethod
    # def update(cls, dt):
    #     for b1 in cls.bodies:
    #         b1.set_force(Vector(0, 0))
    #         for b2 in cls.bodies:
    #             if b1 != b2:
    #                 # if Vector.sum(b1.pos, b2.pos.negative()).get_magnitude()< b1.radius + b2.radius:
    #                 #     cls.handle_collision(b1, b2)
    #                 # b1.add_force(cls.get_gravity(b1, b2))
    #                 b1.add_force(b1.get_gravity(b2))
    #         b1.vel.add(b1.get_accel().multiply(dt))
    #         b1.pos.add(b1.vel.multiply(dt))
    #         b1.display_pos.add(b1.vel.multiply(dt).multiply(1 / cls.metres_per_pixel))
    
    @classmethod
    def update_all(cls, dt, unit):
        # unit is the resolution of time
        # added unit to make it so prevent accuracy loss at higher play speeds because without 'unit as
        # play speed increases 'dt' increases essentially decreasing the resolusion of the position - time graph
        # turning a curved line into a series of lines
        # having a unit too small will result in a loss of performance
        # having a unit too large will result in inaccuracy of position, and velocity at higher play speeds
        while dt > 0:
            for b1 in cls.bodies:
                b1.update(unit)
            dt -= unit
            
    @classmethod
    def get_by_name(cls, name):
        for b in cls.bodies:
            if b.name == name:
                return b

    @classmethod
    def handle_collision(cls, b1, b2):
        print("jijijijii")
        new_radius = (b1.radius**2 + b2.radius**2)**(1/2)
        new_mass = b1.mass + b2.mass
        if b1.mass > b2.mass:
            new_pos = b1.pos
            new_display_pos = b1.display_pos
            new_color = b1.color
        else:
            new_color = b2.color
            new_display_pos = b2.display_pos
            new_pos = b2.pos
        new_vel = Vector.sum(b1.vel.multiply(b1.mass), b2.vel.multiply(b2.mass)).multiply(1 / new_mass)
        b3 = Body(radius=new_radius, mass=new_mass, pos=new_pos, vel=new_vel, color=new_color)
        b3.display_pos =  new_display_pos  
        print(b3.display_pos.to_string())
        print(b3.radius)
        b1.remove_body() 
        b2.remove_body()
        
    @classmethod
    def add_body(cls, body):
        cls.bodies.append(body)
    
    def set_name(self, name):
        self.name = name

    def update(self, dt):
        if self.color != "orange":
            self.set_force(Vector(0, 0))
            for body in self.bodies:
                if self != body:
                    # if Vector.sum(b1.pos, b2.pos.negative()).get_magnitude()< b1.radius + b2.radius:
                    #     cls.handle_collision(b1, b2)
                    # b1.add_force(cls.get_gravity(b1, b2))
                    self.add_force(self.get_gravity(body))
            self.vel.add(self.get_accel().multiply(dt))
            self.pos.add(self.vel.multiply(dt))
            self.display_pos.add(self.vel.multiply(dt).multiply(1 / self.metres_per_pixel))

    def remove_body(self):
        self.bodies.remove(self)

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




