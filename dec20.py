"""--- Day 20: Particle Swarm ---

Suddenly, the GPU contacts you, asking for help. Someone has asked it to
simulate too many particles, and it won't be able to finish them all in time
to render the next frame at this rate.

It transmits to you a buffer (your puzzle input) listing each particle in
order (starting with particle 0, then particle 1, particle 2, and so on). For
each particle, it provides the X, Y, and Z coordinates for the particle's
position (p), velocity (v), and acceleration (a), each in the format <X,Y,Z>.

Each tick, all particles are updated simultaneously. A particle's properties
are updated in the following order:

    Increase the X velocity by the X acceleration.
    Increase the Y velocity by the Y acceleration.
    Increase the Z velocity by the Z acceleration.
    Increase the X position by the X velocity.
    Increase the Y position by the Y velocity.
    Increase the Z position by the Z velocity.

Because of seemingly tenuous rationale involving z-buffering, the GPU would
like to know which particle will stay closest to position <0,0,0> in the long
term. Measure this using the Manhattan distance, which in this situation is
simply the sum of the absolute values of a particle's X, Y, and Z position.

For example, suppose you are only given two particles, both of which stay
entirely on the X-axis (for simplicity). Drawing the current states of
particles 0 and 1 (in that order) with an adjacent a number line and diagram
of current X positions (marked in parenthesis), the following would take
place:

p=< 3,0,0>, v=< 2,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 4,0,0>, v=< 0,0,0>, a=<-2,0,0>                         (0)(1)

p=< 4,0,0>, v=< 1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=< 2,0,0>, v=<-2,0,0>, a=<-2,0,0>                      (1)   (0)

p=< 4,0,0>, v=< 0,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-2,0,0>, v=<-4,0,0>, a=<-2,0,0>          (1)               (0)

p=< 3,0,0>, v=<-1,0,0>, a=<-1,0,0>    -4 -3 -2 -1  0  1  2  3  4
p=<-8,0,0>, v=<-6,0,0>, a=<-2,0,0>                         (0)

At this point, particle 1 will never be closer to <0,0,0> than particle 0, and
so, in the long run, particle 0 will stay closest.

Which particle will stay closest to position <0,0,0> in the long term?

Your puzzle answer was 364.


--- Part Two ---

To simplify the problem further, the GPU would like to remove any particles
that collide. Particles collide if their positions ever exactly match. Because
particles are updated simultaneously, more than two particles can collide at
the same time and place. Once particles collide, they are removed and cannot
collide with anything else after that tick.

For example:

p=<-6,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-4,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-2,0,0>, v=< 1,0,0>, a=< 0,0,0>    (0)   (1)   (2)            (3)
p=< 3,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=<-3,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=<-2,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=<-1,0,0>, v=< 1,0,0>, a=< 0,0,0>             (0)(1)(2)      (3)
p=< 2,0,0>, v=<-1,0,0>, a=< 0,0,0>

p=< 0,0,0>, v=< 3,0,0>, a=< 0,0,0>
p=< 0,0,0>, v=< 2,0,0>, a=< 0,0,0>    -6 -5 -4 -3 -2 -1  0  1  2  3
p=< 0,0,0>, v=< 1,0,0>, a=< 0,0,0>                       X (3)
p=< 1,0,0>, v=<-1,0,0>, a=< 0,0,0>

------destroyed by collision------
------destroyed by collision------    -6 -5 -4 -3 -2 -1  0  1  2  3
------destroyed by collision------                      (3)
p=< 0,0,0>, v=<-1,0,0>, a=< 0,0,0>

In this example, particles 0, 1, and 2 are simultaneously destroyed at the
time and place marked X. On the next tick, particle 3 passes through unharmed.

How many particles are left after all collisions are resolved?

Your puzzle answer was 420.

"""


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

#EDIT:

#...excepppppt it's not quite that simple - t is the correct multiplyer for v0
#but t^2 doesn't work for a


#why? because we're integrating under a stairstep function, not a line,
#probably, and so the answer is a the t-th triangle number rather than the
#square? (no velocity accumulates between lattice points, so it makes some
#sense that t^2 would be an over estimate)


#in any case, we can see the pattern if we look at the first few ticks for x:

#    at time 1:
#        vx1 = vx0 + ax       px1 = x0 + vx1
#                                 = x0 + vx0 + a

#    at time 2:
#        vx2 = vx1 + ax        px2 = px1 + vx2
#            = vx0 + 2ax           = (x0 + vx0 + ax) + (vx0 + 2ax)
#                                  = x0 + 2vx0 + 3ax

#    at time 3:
#        vx3 = vx2 + ax        px3 = px2 + vx3
#            = vx0 + 3ax           = (x0 + 2vx0 + 3ax) + (vx0 + 3ax)
#                                  = x0 + 3vx0 + 6ax

#    at time 4:
#        vx4 = vx3 + ax        px4 = px3 + vx4
#            = vx0 + 4ax           = (x0 + 3vx0 + 6ax) + (vx0 + 4ax)
#                                  = x0 + 4vx0 + 10ax

#    at time t:
#        vxt = vx(t-1) + ax
#            = vx0 + ax * t

#        pxt = px(t-1) + vxt
#            = (x0 + vx0 * (t-1) + ax * T(t-1)) + (vx0 + ax * t)
#            = x0 + vx0 * t + ax * T(t)

#where T(t) is the t-th triangle number, given by t(t+1) / 2


#so in total we have

#    pxt = x0 + vx0 * t + ax * T(t)
#        = x0 + vx0 * t + ax * t * (t+1) / 2
#        = x0 + vx0 * t + (ax * t^2 + ax * t) / 2
#        = x0 + (vx0 + ax/2) * t + ax/2 * t^2

#still a quadratic, just a somewhat more complicated one

#END EDIT


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

#    pxt = x0 + vx0 * t + ax * T(t)
#        = x0 + vx0 * t + ax * t * (t+1) / 2
#        = x0 + vx0 * t + (ax * t^2 + ax * t) / 2
#        = x0 + (vx0 + ax/2) * t + ax/2 * t^2


#at time t, particle P will be at:

#    (Px0 + (Pvx0 + Pax/2) * t + Pax/2 * t^2,
#     Py0 + (Pvy0 + Pay/2) * t + Pay/2 * t^2,
#     Pz0 + (Pvz0 + Paz/2) * t + Paz/2 * t^2)

#and particle Q will be at:

#    (Qx0 + (Qvx0 + Qax/2) * t + Qax/2 * t^2,
#     Qy0 + (Qvy0 + Qay/2) * t + Qay/2 * t^2,
#     Qz0 + (Qvz0 + Qaz/2) * t + Qaz/2 * t^2)


#same as before, eventually all coords will be positive, so we can get rid of
#the abs in the dist calculation and just add coords

#    P dist =
#        Px0 + Py0 + Pz0 +
#        (Pvx0 + Pvy0 + Pvz0 + Pax/2 + Pay/2 + Paz/2) * t +
#        (Pax/2 + Pay/2 + Paz/2) * t^2
#    Q dist =
#        Qx0 + Qy0 + Qz0 +
#        (Qvx0 + Qvy0 + Qvz0 + Qax/2 + Qay/2 + Qaz/2) * t +
#        (Qax/2 + Qay/2 + Qaz/2) * t^2

#we've assumed that the sum of the v's is the same, and the sum of the a's is
#the same, so the tiebreaker is the sum of the original coords


from math import sqrt
from itertools import combinations


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


class Particle(object):
    """A single particle"""

    def __init__(self, point, velocity, accel):
        self.position = Vector(*point)
        self.velocity = Vector(*velocity)
        self.accel = Vector(*accel)

    def __repr__(self):
        """Provide helpful representation when printing"""

        repr_str = "<Particle p={p} v={v} a={a}>"
        return repr_str.format(p=self.position, v=self.velocity, a=self.accel)


class PositiveParticle(Particle):
    """A particle with positive acceleration."""

    def __init__(self, point, velocity, accel):
        super(PositiveParticle, self).__init__(point, velocity, accel)
        self.make_accel_positive()


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



def make_particles(input_file, positive=False):
    """Given the input file object, return a list of particles."""

    particles = []

    for line in input_file:
        #each line is of the form p=<x,y,z>, v=x,y,z>, a=<x,y,z>
        point_str, velocity_str, accel_str = line.strip("\n").split(", ")
        point = map(int, point_str[3:-1].split(","))
        velocity = map(int, velocity_str[3:-1].split(","))
        accel = map(int, accel_str[3:-1].split(","))

        #positive particles all have positive acceleration
        if positive:
            particle = PositiveParticle(point, velocity, accel)
        else:
            particle = Particle(point, velocity, accel)
            particle.destruction_time = None
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


#at time t, particle P will be at:

#    (Px0 + (Pvx0 + Pax/2) * t + Pax/2 * t^2,
#     Py0 + (Pvy0 + Pay/2) * t + Pay/2 * t^2,
#     Pz0 + (Pvz0 + Paz/2) * t + Paz/2 * t^2)

#and particle Q will be at:

#    (Qx0 + (Qvx0 + Qax/2) * t + Qax/2 * t^2,
#     Qy0 + (Qvy0 + Qay/2) * t + Qay/2 * t^2,
#     Qz0 + (Qvz0 + Qaz/2) * t + Qaz/2 * t^2)


#if they collide, that means there's some t where their coords are all equal:

#    Px0 + (Pvx0 + Pax/2) * t + Pax/2 * t^2 =
#    Qx0 + (Qvx0 + Qax/2) * t + Qax/2 * t^2

#    Py0 + (Pvy0 + Pay/2) * t + Pay/2 * t^2 =
#    Qy0 + (Qvy0 + Qay/2) * t + Qay/2 * t^2

#and

#    Pz0 + (Pvz0 + Paz/2) * t + Paz/2 * t^2 =
#    Qz0 + (Qvz0 + Qaz/2) * t + Qaz/2 * t^2


#solving the x equation for t gives:

#    Px0 + (Pvx0 + Pax/2) * t + Pax/2 * t^2 =
#    Qx0 + (Qvx0 + Qax/2) * t + Qax/2 * t^2

#    (Pax/2 - Qax/2) * t^2 + (Pvx0 + Pax/2 - Qvx0 - Qax/2) * t + (Px0 - Qx0) =
#    0

#    t = (-b +- sqrt(b^2 -4ac)) / (2a)

#where

#    a = Pax/2 - Qax/2, b = Pvx0 + Pax/2 - Qvx0 - Qax/2, and c = Px0 - Qx0


#in order for two particles to collide, all three coords must match at the same
#time


def do_quad_formula(a, b, c):
    """Given a, b, and c, solve ax^2 + bx + c = 0 for x, returning the answer
       as a set. Returns an empty set if the solutions are imaginary."""

    #make sure there even are (real) solutions by checking the discriminant
    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return set()

    #if we get here, there are solutions
    solutions = set()
    #note that we don't need to worry about integer division because sqrt
    #always returns a float, even if given a perfect square
    solutions.add((-b + sqrt(discriminant)) / (2 * a))
    solutions.add((-b - sqrt(discriminant)) / (2 * a))

    return solutions


def find_line_x_int(m, b):
    """Given m and b, solve mx + b = 0 for x, returning the answer as a set.
       Returns an empty set if the line has no x-int."""

    #horizontal lines (other than y = 0) have no x-int
    assert m != 0 or b != 0, "y=0 given, solution is all reals"
    if m == 0:
        return set()

    #do the math
    return {-b / float(m)}


def is_int(num):
    """Returns True iff the number is within 1e-09 of the closest int. A way to
       account for the imprecision of float arithmetic."""

    return abs(num - round(num)) < 1e-09


def find_1D_collision_times(particleA, particleB, dimension):
    """Return the set of times at which the given particles' coordinates match.
       If the coordinates always match, return {"always"}."""

    a = (getattr(particleA.accel, dimension) / 2.0 -
         getattr(particleB.accel, dimension) / 2.0)
    b = (getattr(particleA.velocity, dimension) +
         getattr(particleA.accel, dimension) / 2.0 -
         getattr(particleB.velocity, dimension) -
         getattr(particleB.accel, dimension) / 2.0)
    c = (getattr(particleA.position, dimension) -
         getattr(particleB.position, dimension))
    #if they have the same acceleration in this dimension, a will be zero and
    #the quad formula will end up with a div-by-zero error (because we'll
    #really be dealing with a line, not a parabola), so guard against that
    if a != 0:
        solutions = do_quad_formula(a, b, c)
    #if they have the same acceleration *and* velocity in this dimension, the
    #line will be horizontal and not have a single x-int, so guard against that
    elif b != 0:
        solutions = find_line_x_int(b, c)
    #if we're here, a and b both *are* zero (same accel and velocity) so the
    #particles won't intersect if they don't they start out in the same place
    elif c != 0:
        return set()
    #if they do start out in the same place, their coordinates will always
    #match
    else:
        return {"always"}

    #if we get here, we at least in theory could have solutions - filter out
    #any negative or non-integer ones and return the result
    return {s for s in solutions if s >= 0 and is_int(s)}


def find_overall_collision_time(particleA, particleB):
    """Return the earliest time at which the given particles will collide, or
       None if they never will."""

    #figure out if the particle's x-coords will ever match
    x_collision_times = find_1D_collision_times(particleA, particleB, "x")

    #if not, we can stop checking
    if len(x_collision_times) == 0:
        return

    #if so, check for y
    y_collision_times = find_1D_collision_times(particleA, particleB, "y")

    #if the y's never match, we're done
    if len(y_collision_times) == 0:
        return

    #now we know they x's and y's at some point match, so check z
    z_collision_times = find_1D_collision_times(particleA, particleB, "z")

    #if the z's never match, no go
    if len(z_collision_times) == 0:
        return

    #now that we know that all three coordinates at some point match, we need
    #to check that they match at the *same* point

    #find any times that x and y have in common
    if "always" in x_collision_times:
        common_x_y_times = y_collision_times
    elif "always" in y_collision_times:
        common_x_y_times = x_collision_times
    else:
        common_x_y_times = x_collision_times & y_collision_times

    #if there are none, bail
    if not common_x_y_times:
        return None

    #otherwise, see if any of z's times match the x-y times
    if "always" in z_collision_times:
        common_times = common_x_y_times
    else:
        common_times = common_x_y_times & z_collision_times

    #if there are multiple possibilities, pick the earliest one
    if len(common_times) > 1:
        return min(common_times)
    #if there's only one possibility, and it's not "always," return it
    elif len(common_times) == 1 and common_times != {"always"}:
        return common_times.pop()
    #if the positions always match, the particles collide immediately
    elif common_times == {"always"}:
        return 0
    #otherwise, there are no matches - the particles don't collide
    else:
        return None


def count_surviving_particles(particles):
    """Given a list of particles, determine how many never collide with another
       particle."""

    #figure out which particles will intersect, ever, storing the information
    #as a list of tuples of the form (collision time, particleA, particleB)
    collisions = []
    for particleA, particleB in combinations(particles, 2):

        # print "comparing", particleA, particleB

        #figure out if the particles will ever collide, and if so, when
        collision_time = find_overall_collision_time(particleA, particleB)

        #if they do, store this information
        if collision_time:
            # print "collision found:", particleA, particleB, collision_time
            collisions.append((collision_time, particleA, particleB))


    #now that we've figured out all the possible particle collisions, apply
    #them to the particles, in the order in which they happen (this guarantees
    #that if a particle has already been destroyed by an earlier collision,
    #we'll know about it)
    collisions.sort()
    for collision_time, particleA, particleB in collisions:
        #check each of the particles - if either was destroyed before this
        #moment, the collision doesn't count
        if ((particleA.destruction_time and
             particleA.destruction_time < collision_time) or
            (particleB.destruction_time and
             particleB.destruction_time < collision_time)):
            continue

        #otherwise, mark each as having been destroyed in this collision
        particleA.destruction_time = collision_time
        particleB.destruction_time = collision_time

    #finally, count how many particles survive
    return len([particle for particle in particles
                if not particle.destruction_time])





with open("dec20.txt") as input_file:
    particles = make_particles(input_file, positive=True)
    print find_biggest_homebody(particles)

with open("dec20.txt") as input_file:
    particles = make_particles(input_file, positive=False)
    from datetime import datetime
    begin = datetime.now()
    print count_surviving_particles(particles)
    print datetime.now() - begin





###### other thoughts from solving part 2 ############

#figure out which particles will intersect, ever, storing the information
#as a FIGURE OUT HOW!

#need to know all collisions
#need to know all times of collisions - if a colliding particle is
#destroyed before it reaches collision point, collision doesn't count, so
#need sorted list of collision times (also, neg times don't count)
#need to know, at each collision time, which particles are colliding - any
#future collisions they have don't count

#store collision partners on particles, along with time of collision?
#sort in reverse by collision time
#each particle pair, check for collision and add note to both if they'll
#collide
#then go through again, and check each colliding particle's earliest
#collision partner - if parter has earlier collision, remove partner from
#list, note that something's changed (like bubble sort)
#repeat until no changes happen

#quadratic to find collisions
#num collisions nlogn to sort, constant to remove and check earliest vs
#constant to add, linear to remove, linear to check earliest - do this
#quad to check all

#vs

#keep dictionary of particle positions (tuples): particles there
#do moves (linear each tick), removing particles as needed - how to know
#when we're done?

#do non-integer times count? prob not - but then is it safe to check
#equality of int-cast num vs actual num, or should there be a tolerance


