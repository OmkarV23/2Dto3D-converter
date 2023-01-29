import cv2
import numpy as np

class get_perspectives():
    def __init__(self,image,Hxy,Hyz,Hxz,points):
        self.image = image
        self.Hxy = Hxy
        self.Hyz = Hyz
        self.Hxz = Hxz
        self.points = points
        w,h,_ = self.image.shape
        self.w = w
        self.h = h

    def warped(self):      
        #######################################################################
        ##xz plane
        pointxz_1 = self.points[0] + [1]
        pointxz_2 = self.points[1] + [1]
        pointxz_3 = self.points[3] + [1]
        pointxz_4 = self.points[4] + [1]
        points_xz = [pointxz_1, pointxz_2, pointxz_3, pointxz_4]
        _ = self.correction(points_xz,self.Hxz,1)
        #######################################################################
        ##xy plane
        pointxy_1 = self.points[3] + [1]
        pointxy_2 = self.points[4] + [1]
        pointxy_3 = self.points[5] + [1]
        pointxy_4 = self.points[6] + [1]
        points_xy = [pointxy_1, pointxy_2, pointxy_3, pointxy_4]
        _ = self.correction(points_xy,self.Hxy,2)
        #######################################################################
        ##yz plane
        pointyz_1 = self.points[0] + [1]
        pointyz_2 = self.points[2] + [1]
        pointyz_3 = self.points[3] + [1]
        pointyz_4 = self.points[5] + [1]
        points_yz = [pointyz_1, pointyz_2, pointyz_3, pointyz_4]
        _ = self.correction(points_yz,self.Hyz,3,True)
        #######################################################################

    def get_warped_points(self,points,h_mat):
        new_points = []
        for i in points:
            pt_tmp = np.linalg.inv(h_mat) @ np.array(i)
            new_points.append((round(pt_tmp[0]/pt_tmp[2]), round(pt_tmp[1]/pt_tmp[2])))
        return np.array(new_points)

    def correction(self,points,h_mat,counter,h_flip=False):
        warped_points = self.get_warped_points(points,h_mat)
        if warped_points[:,0].min() < 0:
            h_mat[0,2] = warped_points[:,0].min()-h_mat[0,2]
        if warped_points[:,0].max() > self.h:
            h_mat[0,2] = h_mat[0,2] - (warped_points[:,0].max() - self.h)
        if warped_points[:,1].min() < 0:
            h_mat[1,2] = warped_points[:,1].min()-h_mat[1,2]
        if warped_points[:,1].max() > self.w:
            h_mat[1,2] = h_mat[1,2] - (warped_points[:,1].max() - self.w)

        try:
            calib_pts = self.get_warped_points(points,h_mat)
            per = cv2.warpPerspective(self.image,h_mat,(self.h,self.w),flags=cv2.WARP_INVERSE_MAP)
            per = cv2.flip(per[calib_pts[:,1].min():calib_pts[:,1].max(),
                        calib_pts[:,0].min():calib_pts[:,0].max()],0)
            if h_flip==True:
                per = cv2.flip(per,1)
            # for i in calib_pts:
            #     per = cv2.circle(per, i, 3, (255, 255, 255), 4)
            cv2.imshow("Perspective {}".format(counter),per)
            cv2.imwrite("Perspective {}.jpg".format(counter),per)
            cv2.waitKey(0)
            return h_mat
        except:
            return None
