detect_ball
================
默认参数说明
-------------------
float rmin = 30;  

最小霍夫圆检测半径  

float rmax = 90;   

最大霍夫圆检测半径   

float rmin_threshold = 86;   

最小半径自适应的上限   


double HoughCircles_param2 = 18;   

霍夫圆参数，越小，检测到越多近似的圆； 越大，检测到的圆越接近完美的圆形  


int check_grab_roi[4] = { 459, 479, 254, 304 };   

检查抓取情况时的兴趣域 [top bottom left right]  要根据自己设备夹取到球时的实际情况修改  

函数功能说明
----------------
### color_filter   

传入参数：int color, Mat img   

color=1  yellow   
color=0  white  

返回值：Mat img  筛选后的二值图像

函数功能：提取图像中的黄色或白色区域  


### find_circle  

传入参数：Mat img, int color, int circle_number树上应有的果实数量   

返回值：vector<Vec3f> circles 找到的圆  
  
函数功能：通过霍夫圆检测找到果实 
  
  
###  detect_circles

传入参数：int cam,int color, int circle_number,int sample_times=9 默认取样次数为9,time_t time_out=5 默认超时时间为5 ,time_t time_out_en=false 超时标志位为false   

返回值：Return_sign circleImg 
  
  typedef struct returndata{
	Mat img;
	vector<Vec3f> circles;

}Result_sign;  
  
 ### detect_type  
	
传入参数：int cam, int mode 检测模式（0 采摘区 1 放置区）, time_t time_out = 8, time_t time_out_en = false  

返回值：int fruit_type  
	
 1: "蓝莓",  
	  
 2: "红枣",  
	
 3: "草莓",  
	
 4: "无花果"  
	 
函数功能：裁剪出识别到的圆的区域，利用模板匹配识别果实上的贴纸  

### check_grab  
	
传入参数：int cam, int color  
	
函数功能：根据二值化图片中白色区域的占比判断是否抓取成功

