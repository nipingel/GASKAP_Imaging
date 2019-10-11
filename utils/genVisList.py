## script to generate a list of visibilities for CASA task input
SBArr = ['4567', '4570', '4577']
for SB in SBArr:
	for i in range(0, 36):
		if i < 10:
			beamStr = '0' + str(i)
		else:
			beamStr = str(i)
		visList.append('../data/oldSMC/%s/orig/SMC_%s_beam%s.ms' % (SB, SB, beamStr))
