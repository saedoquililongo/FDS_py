# -*- coding: utf-8 -*-
"""
This routine writes a basic input to run FDS (Fire Dynamics Simulator) and 
saves it as a .fds file.

Created on Sat Nov 28 17:00:00 2020

@author: Sebastian Aedo
"""

from FDSpy.writeINPUT import write

# =============================================================================
# Parametros generales
# =============================================================================
fname = 'IKEA_cfd'
dirname = 'C:/Users/Sebastian Aedo/Desktop/testeo_IKEA/'
title = 'Malla preliminar'

# =============================================================================
# Dominio espacial
# =============================================================================
t0 = 0 #seconds
tf = 60 #seconds

# =============================================================================
# Geometría general
# =============================================================================
## Mesh properties
dx = 1
dlosa = 0.1

# Primer piso 
x0_1 = 0
x1_1 = 52
y0_1 = 0
y1_1 = 106
z0_1 = 0
z1_1 = 10

# Segundo piso
x0_2 = 0
x1_2 = 114
y0_2 = 0
y1_2 = 106
z0_2 = z1_1
z1_2 = z1_1+10

# Calculo del número de elementos
nx_1 = int((x1_1 - x0_1)/dx)
ny_1 = int((y1_1 - y0_1)/dx)
nz_1 = int((z1_1 - z0_1)/dx)

nx_2 = int((x1_2 - x0_2)/dx)
ny_2 = int((y1_2 - y0_2)/dx)
nz_2 = int((z1_2 - z0_2)/dx)


mesh = [[[x0_1,x1_1,y0_1,y1_1,z0_1,z1_1],[nx_1,ny_1,nz_1]],
        [[x0_2,x1_2,y0_2,y1_2,z0_2,z1_2],[nx_2,ny_2,nz_2]]] 

# =============================================================================
# Materials and surfaces
# =============================================================================
## Materials
matl_id = ['MALT_ID','CONDUCTIVITY','SPECIFIC_HEAT','DENSITY']
matl = [['CONCRETE',1.0,0.88,2100],
        ['CARPET',1.0,0.88,2100]]

## Surfaces
surf_id = ['SURF_ID','MATL_ID','COLOR','HRRPUA','THICKNESS']
surf = [['FIRE','','RED',2500,''], #Fire
        ['WALL','CONCRETE','GRAY','',0.1], #Walls in the domain
        ['FLOOR','CARPET','BROWN','',0.1], #Floor in the domain
        ['BOUNDARY','CONCRETE','KHAKI','',0.1], #Floor boundary
        ['OPEN','','WHITE',0,0]]

# =============================================================================
# Obstructions, holes and vents
# =============================================================================
obst = [[[10,20,50,60,0,3],0], #Incendio
        [[0,27.2,0,13,z0_1,z1_1],3], #O1_1
        [[0,0,19,y1_1,z0_1,z1_1],3], #03_1
        [[0,24.3,75.5,y1_1,z0_1,z1_1],3], #O4_1
        [[0,x1_1,82,y1_1,z0_1,z1_1],3], #O5_1
        [[0,29.9,37,39.1,z0_1,z1_1],1], #W1_1
        [[x0_1,x1_2,y0_1,y1_2,z1_1-dlosa,z1_1+dlosa],1],
        [[0,20.6,0,y1_2,z0_2,z1_2],3], #O1_2
        [[20.6,23.6,17.5,y1_2,z0_2,z1_2],3], #O2_2        
        [[23.6,29.6,55.3,y1_2,z0_2,z1_2],3], #O3_2
        [[0,x1_2,97.6,y1_2,z0_2,z1_2],3], #O4_2
        [[101.9,x1_2,0,24.6,z0_2,z1_2],3], #O5_2
        [[89.5,101.9,0,18.6,z0_2,z1_2],3], #O6_2
        [[62.1,89.5,0,12.2,z0_2,z1_2],3], #O7_2
        [[60.6,62.1,0,5.5,z0_2,z1_2],3], #O8_2 *****
        [[0,60.6,0,3.5,z0_2,z1_2],3], #O8_2
        [[48.2,48.2,36.5,46.5,z0_2,z1_2],1], #W1_2
        [[44.6,54,46.5,46.5,z0_2,z1_2],1], #W2_2
        [[44.6,44.6,46.5,64.3,z0_2,z1_2],1], #W3_2
        [[66,66,34.6,51.2,z0_2,z1_2],1], #W4_2
        [[66,85.4,44.6,51.2,z0_2,z1_2],1], #W5_2
        [[85.4,108.8,48.8,51.2,z0_2,z1_2],1], #W6_2
        [[108.8,x1_2,44.6,58.5,z0_2,z1_2],1], #W7_2
        [[102,x1_2,0,y1_2,z1_2-4,z1_2],3], #Ay_2
        [[0,x1_2,85.6,y1_2,z1_2-4,z1_2],3]] #Ax_2


diag = [[0,6,19,13,z0_1,z1_1,nz_1,3,'up'], #O2_1
        [54,60.6,3.5,5.5,z0_2,z1_2,nz_1,3,'down'], #O18_2
        [60.6,62.1,5.5,12.2,z0_2,z1_2,nz_1,3,'down']] #O19_2

hole = [[39.2,52,19.3,36.5,z1_1-dlosa*1.1,z1_1+dlosa*1.1]]

vent = [[[0,1,36,37,0,0],4]]

# =============================================================================
# Write file
# =============================================================================
FDS_input = dirname,fname,title,t0,tf,mesh,matl,matl_id,surf,surf_id,obst,diag,vent,hole,True

write(FDS_input)

# =============================================================================
# Chequeo preliminar de la malla
# =============================================================================
nx_1 = (x1_1 - x0_1)/dx
ny_1 = (y1_1 - y0_1)/dx
nz_1 = (z1_1 - z0_1)/dx

nx_2 = (x1_2 - x0_2)/dx
ny_2 = (y1_2 - y0_2)/dx
nz_2 = (z1_2 - z0_2)/dx

if int(nx_1)==nx_1 and int(ny_1)==ny_1 and int(nz_1)==nz_1:
    if int(nx_2)==nx_2 and int(ny_2)==ny_2 and int(nz_2)==nz_2:
        nx_1 = int(nx_1) ; ny_1 = int(ny_1) ; nz_1 = int(nz_1)
        nx_2 = int(nx_2) ; ny_2 = int(ny_2) ; nz_2 = int(nz_2)
        print('Input file writen succesfully')
    else:
        print('Error: Second floor discretization does not match')
else:
    print('Error: First floor discretization does not match')