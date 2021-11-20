#!/env/python
'''
Script to prepare new MOD from an existing MOD file in tomoDD-format.
Author: Shoucheng Han @ USTC.
'''

import math
import numpy as np

def eightpoints( r, ri, rr, ir, tr ):
	''' find the location of input point(x,y,z) in each direction '''
	for i in range( len(r) ):
		if ri==r[i]:
			rr.append( r[i] )
			rr.append( r[i] )
			tr.append( 1 )
			ir.append( i )
			ir.append( i )
			tr.append( 1 )
			return rr, ir, tr
		elif ri<r[i]:
			rr.append( r[i-1] )
			rr.append( r[i] )
			tr.append( r[i] - r[i-1] )
			ir.append( i-1 )
			ir.append( i )
			tr.append( 2 )
			return rr, ir, tr


def vel_interp( x, y, z, xp, yp, zp, vo, vel ):
	''' Calculate the velocity of any point(x,y,z) by trilinear interpolation method. '''
	if xp<min(x):
		xp = min(x)
	if yp<min(y):
		yp = min(y)
	if zp<min(z):
		zp = min(z)
	if xp>max(x):
		xp = max(x)
	if yp>max(y):
		yp = max(y)
	if zp>max(z):
		zp = max(z)

	xx=[]; yy=[]; zz=[]
	ix=[]; iy=[]; iz=[]
	dx = 0 ;	dy = 0 ;	dz = 0
	ni = 0 ;	nj = 0 ;	nk = 0

	tmp = [];	eightpoints( x, xp, xx, ix, tmp );	dx = tmp[0];	ni = tmp[1]
	tmp = [];	eightpoints( y, yp, yy, iy, tmp );	dy = tmp[0];	nj = tmp[1]
	tmp = [];	eightpoints( z, zp, zz, iz, tmp );	dz = tmp[0];	nk = tmp[1]

	v = 0
	for k in range(nk):
		for j in range(nj):
			for i in range(ni):
				v = v + vo[ iz[k]*ny+iy[j],ix[i] ] * (1-abs((xp-xx[i])/dx))*\
						          (1-abs((yp-yy[j])/dy))*(1-abs((zp-zz[k])/dz))
	vel.append( v )
	return vel


if __name__=='__main__':
	''' main function begin here. '''
	# read exist MOD file
	i=0 ;   j=-1;   k=-1;
	fid = open('./MOD-USTClitho2.0','r')
	try:
		for line in fid:
			line = line.strip()
			line = line.strip('\n')
			line = line.split()
			i = i + 1
			if i==1:
				bld = float(line[0])
				nx = int(line[1])
				ny = int(line[2])
				nz = int(line[3])
				vpo= np.zeros( (ny*nz,nx) )
				vso= np.zeros( (ny*nz,nx) )
			elif i==2:
				xn = np.array( [ float(xx) for xx in line ] )
			elif i==3:
				yn = np.array( [ float(xx) for xx in line ] )
			elif i==4:
				zn = np.array( [ float(xx) for xx in line ] )
			elif i<(5+nz*ny):
				j = j + 1
				vpo[j,:] = np.array( [float(xx) for xx in line ] )
			else:
				k = k + 1
				vso[k,:] = np.array( [float(xx) for xx in line ] )
	finally:
		fid.close()
	vso = vpo/vso

	# set the coordinates for new MOD
	# ----------------------------------------------
	xi = [ 105, 110, 110.5, 111, 111.5, 112, 112.5, 113, 113.5, 114, 114.5, 115, 120  ]
	yi = [ 30, 35, 35.5, 36, 36.5, 37, 37.5, 38, 38.5, 39, 39.5, 40, 45  ]
	zi = [ -10, -3, 0, 5, 10, 15, 20, 30, 40, 60, 100 ]

	nxi = len(xi)
	nyi = len(yi)
	nzi = len(zi)

	vp  = np.zeros( (nzi*nyi,nxi) )
	vs  = np.zeros( (nzi*nyi,nxi) )

	tvp = 0. ;	tvs = 0.
	for k in range(nzi):
		for j in range(nyi):
			for i in range(nxi):
				tvp = [];	vel_interp( xn, yn, zn, xi[i], yi[j], zi[k], vpo, tvp )
				vp[ k*nyi+j,i ] = tvp[0]
				tvs = [];	vel_interp( xn, yn, zn, xi[i], yi[j], zi[k], vso, tvs )
				vs[ k*nyi+j,i ] = tvs[0]

	# output new MOD to file
	# -----------------------------------------------------------------------
	fid = open('MOD','w')
	print >> fid, "%g %d %d %d" % ( bld, nxi, nyi, nzi )

	for i in range(nxi):
		print >> fid, "%g" % ( xi[i] ),
	print >> fid, ""

	for j in range(nyi):
		print >> fid, "%g" % ( yi[j] ),
	print >> fid, ""

	for k in range(nzi):
		print >> fid, "%g" % ( zi[k] ),
	print >> fid, ""

	for k in range(nzi):
		for j in range(nyi):
			for i in range(nxi):
				print >> fid, "%.3f" % ( vp[k*nyi+j,i] ),
			print >> fid , ""
	for k in range(nzi):
		for j in range(nyi):
			for i in range(nxi):
				print >> fid, "%.3f" % ( vp[k*nyi+j,i]/vs[k*nyi+j,i] ), ;
			print >> fid , ""
	fid.close()
