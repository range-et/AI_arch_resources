"""Host wrapper around the adapted Viquerat D2Q9/TRT routines.

Coordinates and velocity use lattice units. The GH adapter supplies a solid mask.
This small laminar channel model serves a classroom demonstration.
"""
import numpy as np
import lbm_core as core

C=np.array([[0,0],[1,0],[-1,0],[0,1],[0,-1],[1,1],[-1,-1],[-1,1],[1,-1]])
OPP=np.array([0,2,1,4,3,6,5,8,7])
W=np.array([4/9]+[1/9]*4+[1/36]*4)


def solve(solid, steps=1800, inlet=0.03, tau=0.65):
    solid=np.asarray(solid,dtype=bool)
    nx,ny=solid.shape
    if nx<16 or ny<16 or nx>320 or ny>160:
        raise ValueError('Grid must be between 16 x 16 and 320 x 160')
    if not 1<=steps<=12000 or not 0<inlet<=0.06 or not .55<=tau<=1.2:
        raise ValueError('Use 1..12000 steps, 0<inlet<=0.06, and .55<=tau<=1.2')
    if solid[[0,-1],:].any() or solid[:,[0,-1]].any():
        raise ValueError('Footprints must stay inside the domain')
    rho=np.ones((nx,ny));u=np.zeros((2,nx,ny))
    g=np.zeros((9,nx,ny));eq=np.zeros_like(g);post=np.zeros_like(g)
    eta=np.arange(ny)/(ny-1)
    profile=inlet*4*eta*(1-eta)
    u[0]=profile[None,:]
    u[:,solid]=0
    core.nb_equilibrium(u,C,W,rho,g)
    left=np.zeros((2,ny));left[0]=profile
    top=np.zeros((2,nx));bottom=top.copy();right=np.zeros((2,ny));pressure=np.ones(ny)
    # Each entry is a fluid node and a direction leading into a solid node.
    links=[]
    for q in range(1,9):
        neighbor=np.roll(solid,(-int(C[q,0]),-int(C[q,1])),axis=(0,1))
        ii,jj=np.where((~solid)&neighbor)
        links.extend((int(i),int(j),q) for i,j in zip(ii,jj))
    boundary=np.array(links,dtype=int).reshape((-1,3))
    tau_minus=.25/(tau-.5)+.5
    rho_error=0.0;maximum_speed=0.0
    for it in range(steps):
        rho[:]=g.sum(axis=0)
        u[0]=np.einsum('q,qxy->xy',C[:,0],g)/rho
        u[1]=np.einsum('q,qxy->xy',C[:,1],g)/rho
        u[:,solid]=0;rho[solid]=1
        core.nb_equilibrium(u,C,W,rho,eq)
        core.nb_col_str(g,eq,post,1/tau,1/tau_minus,C,OPP,nx,ny,nx-1,ny-1)
        core.nb_bounce_back_obstacle(False,boundary,OPP,C,None,post,g,u,None)
        core.nb_zou_he_left_wall_velocity(nx-1,ny-1,u,left,rho,g)
        core.nb_zou_he_right_wall_pressure(nx-1,ny-1,u,pressure,right,rho,g)
        core.nb_zou_he_top_wall_velocity(nx-1,ny-1,u,top,rho,g)
        core.nb_zou_he_bottom_wall_velocity(nx-1,ny-1,u,bottom,rho,g)
        core.nb_zou_he_bottom_left_corner_velocity(nx-1,ny-1,u,rho,g)
        core.nb_zou_he_top_left_corner_velocity(nx-1,ny-1,u,rho,g)
        core.nb_zou_he_bottom_right_corner_velocity(nx-1,ny-1,u,rho,g)
        core.nb_zou_he_top_right_corner_velocity(nx-1,ny-1,u,rho,g)
        g[:,solid]=W[:,None]
        if it%100==0:
            if not np.isfinite(g).all() or rho[~solid].min()<=0:
                raise RuntimeError('The solver became unstable')
            maximum_speed=max(maximum_speed,float(np.hypot(u[0],u[1]).max()))
            rho_error=max(rho_error,float(np.abs(rho[~solid]-1).max()))
            if maximum_speed>.16 or rho_error>.15:
                raise RuntimeError('Speed or density exceeded the demo limits')
    rho=g.sum(axis=0)
    ux=np.einsum('q,qxy->xy',C[:,0],g)/rho
    uy=np.einsum('q,qxy->xy',C[:,1],g)/rho
    ux[solid]=0;uy[solid]=0
    speed=np.hypot(ux,uy)
    assert np.isfinite(speed).all()
    report={'method':'D2Q9 TRT, adapted from jviquerat/lbm','grid':[nx,ny],
            'steps':int(steps),'inlet_peak':float(inlet),'tau_plus':float(tau),
            'tau_minus':float(tau_minus),'solid_cells':int(solid.sum()),
            'max_speed':float(speed.max()),'mean_fluid_speed':float(speed[~solid].mean()),
            'max_checked_density_deviation':rho_error,'finite':bool(np.isfinite(g).all()),
            'positive_density':bool((rho[~solid]>0).all()),
            'boundary':'parabolic left inlet, right pressure, no-slip top/bottom, halfway obstacle bounce-back',
            'scope':'2D laminar channel in lattice units. No atmospheric boundary layer or vertical flow. No grid convergence study.'}
    return ux,uy,rho,report
