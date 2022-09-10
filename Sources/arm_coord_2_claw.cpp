#include<iostream>
#include<math.h>
#include<memory>

// #include <arm_coord_2_claw.h>

using namespace std;

#define pi 3.1415926
#define DE2RA pi/180.0
#define RA2DE 180.0/pi


float sight_middle = 175.0;

// 底座坐标系下相机位置参数 单位cm
float y_camera_to_base = 3.7;
float z_camera_to_base = 24.8;
float D_object_to_camera_upper = 24.5;
 float D_object_to_camera_lower = 27.5;

 float f_x_div_dx = 680.0;
 float f_y_div_dy = 680.0;

 float j5_claw_delta_y = 8.5;
float j5_claw_delta_z = 1.15;


typedef struct _rect
{
    float x;
    float y;
    float z;
    float Roll;
    float Pitch;
    float Yaw;
} Rect;

Rect rect;


void arm_coord_2_claw_(float pixel[2]){
    /*
    :param pixel: 像素平面上点的坐标
    :return: 夹爪中心应在底座坐标系下的位置
    */

   double x_image = pixel[0];
   double y_image = pixel[1];

   float D_object_to_camera;

   if(pixel[1] < sight_middle){
        D_object_to_camera = D_object_to_camera_upper;
   }else{
        D_object_to_camera = D_object_to_camera_lower;
   }

   // 相机坐标系
    float x_camera = x_image * D_object_to_camera / f_x_div_dx;
    float y_camera = y_image * D_object_to_camera / f_y_div_dy;

    //# 底座坐标系     车头超前，x正方向指向车身右侧，y正方向指向车头，z正方向竖直向上
    // coord = []  # z y z Roll Pitch Yaw
    double *coord = new double[6];
    unique_ptr<double> unique_coord(coord);

    coord[0] = x_camera;
    coord[1] = D_object_to_camera - y_camera_to_base;
    coord[2] = z_camera_to_base - y_camera;

    float theta = atan2(coord[1], coord[0]);

    if(coord[2] >= 25){
        coord[3] = -80.0;
    }else{
        coord[3] = -100.0;
    }

    coord[4] = 0.0;
    coord[5] = 0.0;

    double l_j5_claw = sqrt(pow(j5_claw_delta_y, 2) + pow(j5_claw_delta_z, 2));

    double pitch_claw = (coord[3] + 180) * DE2RA - atan2(j5_claw_delta_z, j5_claw_delta_y);

    coord[0] = coord[0] - l_j5_claw * sin(pitch_claw) * cos(theta);
    coord[1] = coord[1] - l_j5_claw * sin(pitch_claw) * sin(theta);
    coord[2] = coord[2] + l_j5_claw * cos(pitch_claw);

    rect.x = coord[0];
    rect.y = coord[1];
    rect.z = coord[2];
    rect.Roll = coord[3];
    rect.Pitch = coord[4];
    rect.Yaw = coord[5];

    // delete[] coord;

}


extern "C"{
    Rect *arm_coord_2_claw(float *x, float *y){
        float a[2];
        a[0] = *x;
        a[1] = *y;
        double *re = new double[6];
        unique_ptr<double> unique_re(re);
        arm_coord_2_claw_(a);

        // delete[] re;
        // delete[] x;
        // delete[] y;
    
        return &rect;
    }

}   