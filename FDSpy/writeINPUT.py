# -*- coding: utf-8 -*-
"""
This routine writes a basic input to run FDS (Fire Dynamics Simulator) and 
saves it as a .fds file.

Created on Sat Nov 28 17:00:00 2020

@author: Sebastian Aedo
"""

def StagDiagWall(x0,x1,y0,y1,z0,z1,n,sid,surf):
    """
    This function creates a staggered sequence of blocks to represent a
    diagonal obstruction in the x-y plane of the  domain. A threshold value is
    incorporated to ensure that the obstruction is completely sealed. The 
    diagonal must be parametrized from left to right.

    Parameters
    ----------
    x0 : [float] Starting x coordinate of the diagonal (left side)
    x1 : [float] Ending x coordinate of the diagonal (right side)
    y0 : [float] Starting y coordinate of the diagonal
    y1 : [float] Ending y coordinate of the diagonal
    z0 : [float] Starting z coordinate of the diagonal
    z1 : [float] Ending z coordinate of the diagonal    
    n : [int] Number of elements representing the diagonal
    sid : [int] Surface ID of the obstruction

    """
    th = 2 #[int]
    x_nodes = [x0 + i*(x1-x0)/n for i in range(n+1)]
    y_nodes = [y0 + (x-x0)*(y1-y0)/(x1-x0) for x in x_nodes]
    for i in range(n):
        diag = str([x_nodes[i],x_nodes[i+1],y_nodes[i],y_nodes[i+1]*th-y_nodes[i],z0,z1])[1:-1]
        file.write('&OBST XB='+diag+', SURF_ID='+"'"+surf[sid][0]+"'"+' /\n')
    return

def StagDiagWall_fill(x0,x1,y0,y1,z0,z1,n,sid,surf,aux):
    x_nodes = [x0 + i*(x1-x0)/n for i in range(n+1)]
    y_nodes = [y0 + (x-x0)*(y1-y0)/(x1-x0) for x in x_nodes]
    for i in range(n):
        if aux == 'down':
            diag = str([x_nodes[i],x_nodes[i+1],y0,y_nodes[i+1],z0,z1])[1:-1]
        elif aux =='up':
            diag = str([x_nodes[i],x_nodes[i+1],y_nodes[i],y1,z0,z1])[1:-1]
        file.write('&OBST XB='+diag+', SURF_ID='+"'"+surf[sid][0]+"'"+' /\n')
    return

def writeMESH(mesh):
    file.write('!! Computational domain\n')
    for i in range(len(mesh)):
        file.write('&MESH XB='+str(mesh[i][0])[1:-1]+', IJK='+str(mesh[i][1])[1:-1]+' /\n')
    file.write('\n')
    return

def writeGeneralConf(fname,title,t0,tf):
    file.write('!! General configuration\n')
    file.write('&HEAD CHID='+"'"+fname+"'"+' TITLE='+"'"+title+"' /\n")
    file.write('&TIME T_BEGIN='+str(t0)+' /\n')
    file.write('&TIME T_END='+str(tf)+' /\n')
    file.write('\n')
    file.write("&REAC ID = 'propane reaction', SOOT_YIELD=0.03, CO_YIELD=0.05, FUEL='PROPANE'/\n")
    file.write('\n')
    return

def writeProperties(matl,matl_id,surf,surf_id):
    file.write('!! Properties\n')
    for i in range(len(matl)):
        file.write('&MATL ID='+"'"+matl[i][0]+"'")
        for j in range(1,len(matl_id)):
            if type(matl[i][j])==str:
                if matl[i][j]!='':
                    file.write(', '+matl_id[j]+'='+"'"+matl[i][j]+"'")
            else:
                file.write(', '+matl_id[j]+'='+str(matl[i][j]))
        file.write(' /\n')
    file.write('\n')
    
    for i in range(len(surf)):
        file.write('&SURF ID='+"'"+surf[i][0]+"'")
        for j in range(1,len(surf_id)):
            if type(surf[i][j])==str:
                if surf[i][j]!='':
                    file.write(', '+surf_id[j]+'='+"'"+surf[i][j]+"'")
            else:
                if surf[i][j]!=0:
                    file.write(', '+surf_id[j]+'='+str(surf[i][j]))
        file.write(' /\n')
    file.write('\n')
    return

def writeSolidGeom(obst,diag,vent,hole,surf,fill):
    file.write('!! Solid geometry\n')
    #Obstacles
    if len(obst[0])!=0:
        for i in range(len(obst)):
            file.write('&OBST XB='+str(obst[i][0])[1:-1]+', SURF_ID='+"'"+surf[obst[i][1]][0]+"'"+' /\n')
        file.write('\n')
        
    #Diagonal obstacles
    if fill == True:
        if len(diag[0])!=0:
            for i in range(len(diag)):
                x0,x1,y0,y1,z0,z1,n,sid,aux = diag[i]
                StagDiagWall_fill(x0,x1,y0,y1,z0,z1,n,sid,surf,aux)
            file.write('\n')
    else:
        if len(diag[0])!=0:
            for i in range(len(diag)):
                x0,x1,y0,y1,z0,z1,n,sid = diag[i]
                StagDiagWall(x0,x1,y0,y1,z0,z1,n,sid,surf)
            file.write('\n')
    
    # Vents
    if len(vent[0])!=0:
        for i in range(len(vent)):
            file.write('&VENT XB='+str(vent[i][0])[1:-1]+', SURF_ID='+"'"+surf[vent[i][1]][0]+"'"+' /\n')
        file.write('\n')
    
    # Holes
    if len(hole[0])!=0:
        for i in range(len(hole)):
            file.write('&HOLE XB='+str(hole[i])[1:-1]+' /\n')
        file.write('\n')
    return

def write(FDS_input):
    dirname,fname,title,t0,tf,mesh,matl,matl_id,surf,surf_id,obst,diag,vent,hole,fill = FDS_input
    
    ## 0. Open file
    global file
    file = open(dirname+fname+'.fds','wt')
    
    ## 1. General configuration
    writeGeneralConf(fname,title,t0,tf)
    
    ## 2. Computational domain
    writeMESH(mesh)
    
    ## 3. Properties
    writeProperties(matl,matl_id,surf,surf_id)
    
    ## 4. Solid geometry
    writeSolidGeom(obst,diag,vent,hole,surf,fill)
    
    file.write('&TAIL /')
    file.close()
    return