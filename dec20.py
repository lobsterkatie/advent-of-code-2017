#with non-zero acceleration, velocity will always be increasing in magnitude,
#so the particle will always be speeding up

#if two particles are accelerating at the same rate, whoever had the slower
#velocity to start will continue to have the slower velocity, meaning the
#faster particle will always overtake the slower one


#assume we're given

#    p0 = <x0, y0, z0>
#    v0 = <vx0, vy0, vz0>
#    a = <ax, ay, az>


#because we add a to v each tick, and v to p each tick, we have

#    v = v0 + t * a
#      = <vx0, vy0, vz0> + t * <ax, ay, az>
#      = <vx0 + t * ax, vy0 + t * ay, vz0 + t * az>

#    p = p0 + t * v
#      = <x0, y0, z0> + t * <vx0 + t * ax, vy0 + t * ay, vz0 + t * az>
#      = <x0 + vx0 * t + ax * t^2,
#         y0 + vy0 * t + ay * t^2,
#         z0 + vz0 * t + az * t^2>


#looked at another way, position at time t is given by

#    p(t) = <f(t), g(t), h(t)>

#where f, g, and h are quadratics


#simplifying step - since we only care how big the coordinates get, not what
#direction they're in, let's flip all parabolas right side up (mult by -1 if
#a < 0)


#this means all coords (and all v's) will eventually be positive (all particles
#will eventually be in the octant where x, y, z are all > 0), and all will be
#heading away from the origin at a faster and faster clip, unless they're not
#accelerating, or still


#still beats constant speed beats speeding up, slower speeds beat faster
#speeds, and slower acceleration beats faster acceleration

#speed = delta_d/delta_t

#if delta_t = 1, speed = delta_d, and we have:

#    old_pos = x0, y0, z0 -> dist = abs(x0) + abs(y0) + abs(z0)
#    new_pos = x0 + vx, y0 + vy, z0 + vz
#       -> dist = abs(x0 + vx) + abs(y0 + vy) + abs(z0 + vz)
#    speed = delta_d = abs(x0 + vx) + abs(y0 + vy) + abs(z0 + vz)
#                      - abs(x0) - abs(y0) - abs(z0)


#if all coords are pos, we can ditch the abs to get:

#    speed = x0 + vx + y0 + vy + z0 + vz - x0 - y0 - z0
#            = vx + vy + vz


#we know that the x-speed at time t is given by:

#    vx(t) = vx0 + ax * t


#same goes for y and z so speed at time t is:

#    v(t) = vx0 + vy0 + vz0 + (ax + ay + az)t


#if all a's are pos, slope of this line is pos, so in the long run the slowest
#speed will be the one with smallest slope


#if there are two with the same smallest slope (sum of a's), the one with the
#lower y-int (which in this case is vx0 + vy0 + vz0) will be less (this is
#still speed we're talking about, so that means it will be slower, and
#slowest = closest to home)


#if there are two with the same slowness (same sum of a's, same sum of v's)
#then...


#at time t, particle P will be at:

#    (Ppx0 + Pvx0 * t + Pax * t^2,
#     Ppy0 + Pvy0 * t + Pay * t^2,
#     Ppz0 + Pvz0 * t + Paz * t^2)

#and particle Q will be at:

#    (Qpx0 + Qvx0 * t + Qax * t^2,
#     Qpy0 + Qvy0 * t + Qay * t^2,
#     Qpz0 + Qvz0 * t + Qaz * t^2)


#same as before, eventually all coords will be positive, so we can get rid of
#the abs in the dist calculation and just add coords

#    P dist =
#        Ppx0 + Ppy0 + Ppz0 + (Pvx0 + Pvy0 + Pvz0)t + (Pax + Pay + Paz)t^2
#    Q dist =
#        Qpx0 + Qpy0 + Qpz0 + (Qvx0 + Qvy0 + Qvz0)t + (Qax + Qay + Qaz)t^2

#we've assumed that the sum of the v's is the same, and the sum of the a's is
#the same, so the tiebreaker is the sum of the p's



class Vector(object):
    """An ordered triple (x, y, z)"""

    __slots__ = ["x", "y", "z"]

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """Provide helpful representation when printing"""

        repr_str = "({x}, {y}, {z})"
        return repr_str.format(x=self.x, y=self.y, z=self.z)

    # def __add__(self, other):
    #     """Allow two vectors to be added, componentwise, using the +
    #        operator."""

    #     new_x = self.x + other.x
    #     new_y = self.y + other.y
    #     new_z = self.z + other.z
    #     return Vector(new_x, new_y, new_z)



class Particle(object):
    """A single particle"""

    def __init__(self, point, velocity, accel):
        self.position = Vector(*point)
        self.velocity = Vector(*velocity)
        self.accel = Vector(*accel)
        self.make_accel_positive()

    def __repr__(self):
        """Provide helpful representation when printing"""

        repr_str = "<Particle p={p} v={v} a={a}>"
        return repr_str.format(p=self.position, v=self.velocity, a=self.accel)

    def make_accel_positive(self):
        """To simplify calculations later on, flip all parabolas representing
           coordinates right side up.

           For example, the x-coord at time t is given by
           x = px0 + vx0*t + ax*t^2
           which forms a parabola. Flip that parabola to concave up by making
           sure a ends up positive."""

        if self.accel.x < 0:
            self.accel.x *= -1
            self.velocity.x *= -1
            self.position.x *= -1

        if self.accel.y < 0:
            self.accel.y *= -1
            self.velocity.y *= -1
            self.position.y *= -1

        if self.accel.z < 0:
            self.accel.z *= -1
            self.velocity.z *= -1
            self.position.z *= -1

    # def get_dist_from_origin(self):
    #     """Calculate the particle's distance from the origin."""

    #     return (abs(self.position.x) + abs(self.position.y) +
    #             abs(self.position.z))

    # def move_once(self):
    #     """Update the particle's velocity using its acceleration, and then its
    #        position using its velocity."""

    #     self.velocity += self.acceleration
    #     self.position += self.velocity


def make_particles(input_file):
    """Given the input file object, return a list of particles."""

    particles = []

    for line in input_file:
        #each line is of the form p=<x,y,z>, v=x,y,z>, a=<x,y,z>
        point_str, velocity_str, accel_str = line.strip("\n").split(", ")
        point = map(int, point_str[3:-1].split(","))
        velocity = map(int, velocity_str[3:-1].split(","))
        accel = map(int, accel_str[3:-1].split(","))
        particle = Particle(point, velocity, accel)
        particles.append(particle)

    return particles


def find_min_sum(particles, candidate_indices, attribute):
    """Given an attribute whose sum to minimize, and a list of the indices of
       possible particles, return a list narrowed down to only those which
       have a minimum sum of the given attribute."""

    filtered_candidate_indices = []
    #grab the sum of the first candidate particle to have something to compare
    #against
    first_candidate_particle = particles[candidate_indices[0]]
    min_sum = (
        getattr(first_candidate_particle, attribute).x +
        getattr(first_candidate_particle, attribute).y +
        getattr(first_candidate_particle, attribute).z)
    #do the comparing
    for candidate_index in candidate_indices:
            candidate_particle = particles[candidate_index]
            sum_of_attrs = (
                getattr(candidate_particle, attribute).x +
                getattr(candidate_particle, attribute).y +
                getattr(candidate_particle, attribute).z)
            #if we find a new minimum
            if sum_of_attrs < min_sum:
                min_sum = sum_of_attrs
                filtered_candidate_indices = [candidate_index]
            #if we tie the old minimum
            elif sum_of_attrs == min_sum:
                filtered_candidate_indices.append(candidate_index)

    return filtered_candidate_indices


def find_biggest_homebody(particles):
    """Given a list of particles, find the one which will be closest to the
       origin in the long run."""

    #find the particle(s) with the smallest sum of a's
    candidate_indices = find_min_sum(particles,
                                     range(len(particles)),
                                     "accel")

    #if we have more than one, compare the sum of v's and pick the one with
    #the lowest value
    if len(candidate_indices) > 1:
        candidate_indices = find_min_sum(particles,
                                         candidate_indices,
                                         "velocity")

    #if we *still* have more than one option, break the tie by comparing sums
    #of p's
    if len(candidate_indices) > 1:
        candidate_indices = find_min_sum(particles,
                                         candidate_indices,
                                         "position")

    #we've now done all the filtering we can - hopefully there's a clear
    #winner
    if len(candidate_indices) == 1:
        return candidate_indices[0]
    else:
        return "more than one option:" + str(candidate_indices)






with open("dec20.txt") as input_file:
    particles = make_particles(input_file)
    print find_biggest_homebody(particles)




































