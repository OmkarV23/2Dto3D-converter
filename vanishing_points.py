import numpy as np

class VP():
    def __init__(self):
        pass

    def get_line(self,a):
        st = np.insert(a[0], 2, 1)
        ed = np.insert(a[1], 2, 1)
        return np.cross(st,ed)

    @classmethod
    def points(cls,coordinates):
        vpts = []
        for coordinates_line in coordinates:
            line1 = cls.get_line(cls,coordinates_line[0])
            line2 = cls.get_line(cls,coordinates_line[1])
            vanishing_pt = np.cross(line1,line2)
            vpts.append(vanishing_pt/vanishing_pt[2])
        return np.array(vpts)[:,None,:]