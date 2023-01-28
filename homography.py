import numpy as np

class Projection():
    def __init__(self):
        pass
    def least_squares(self,a,b,dist):
        x,_,_,_ = np.linalg.lstsq(a.T,b.T,rcond=None)
        return x[0]/dist
    @classmethod
    def mat(cls,world_coordinate,ref_coordinates,vanishing_points):
        ref_xyz = []
        dist_xyz = []
        scales = []
        w0 = np.insert(world_coordinate,2,1)
        for i in ref_coordinates:
            r = np.insert(i,2,1)
            ref_xyz.append(r)
            dist_xyz.append(np.linalg.norm(r-w0,2))
        for ref,dist,vp in zip(ref_xyz,dist_xyz,vanishing_points):
            scales.append(cls.least_squares(cls,vp-ref,ref-w0,dist))
        
        projection_mat = np.concatenate([(scales[0]*vanishing_points[0]).T, (scales[1]*vanishing_points[1]).T, 
                                        (scales[2]*vanishing_points[2]).T, w0[None,:].T], axis=1)
        return projection_mat


class Homography():
    def __init__(self):
        pass
    @classmethod
    def mat(cls,world_coordinate,ref_coordinates,vanishing_points):
        projection_mat = Projection.mat(world_coordinate,ref_coordinates,vanishing_points)[:,None,:]
        Hxy = np.concatenate([projection_mat[:,:,0],projection_mat[:,:,1],projection_mat[:,:,3]],axis=1)
        Hyz = np.concatenate([projection_mat[:,:,1],projection_mat[:,:,2],projection_mat[:,:,3]],axis=1)
        Hxz = np.concatenate([projection_mat[:,:,0],projection_mat[:,:,2],projection_mat[:,:,3]],axis=1)
        return Hxy,Hyz,Hxz
    



