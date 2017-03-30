import hoomd
from hoomd import md
from hoomd import deprecated
import argparse

# initialize hoomd, including parse (aka, split command line into useful components)
hoomd.context.initialize()
# this gets the string defined in: --user="user_args"
user_args = hoomd.option.get_user()

# Now we use our own argparser on the string: user_args
parser = argparse.ArgumentParser(description='BD Simulation with capture probability pseudo-potential')
parser.add_argument('-T', '--temperature', action='store', type=float, default=1.0, help='Temperature of BD [normalized units]')
parser.add_argument('--phi', action='store', type=float, default=0.01, help='Volume fraction [normalized units]')
args = parser.parse_args(user_args)
input_temperature = args.temperature
input_phi = args.phi
print("Temperature:", input_temperature)
print("volume fraction:", input_phi)

output_base_filename = './output/' + 'T' + str(input_temperature)+'phi'+str(input_phi)

# create 1000 random particles of name A
system = hoomd.deprecated.init.create_random(N=1000, phi_p=input_phi, name='A', min_dist = 1.0)
nl = md.nlist.cell()
# specify Lennard-Jones interactions between particle pairs
lj = md.pair.lj(r_cut=2.5, nlist=nl)
lj.pair_coeff.set('A', 'A', epsilon=1.0, sigma=1.0)

# integrate at constant temperature
all = hoomd.group.all()
md.integrate.mode_standard(dt=0.005)
hoomd.md.integrate.langevin(group=all, kT=input_temperature, seed=5)

#msd
hoomd.deprecated.analyze.msd(filename = output_base_filename + 'msd.csv', groups=[all], period=500)

# dump an xmle file for the structure information
xml = hoomd.deprecated.dump.xml(group=all, filename = output_base_filename + '.xml', vis=True)
# dump a .dcd file for the trajectory
hoomd.dump.dcd(filename = output_base_filename + '.dcd', period=100)

# run 10,000 time steps
hoomd.run(10e2)

#vim: set ft=python:
