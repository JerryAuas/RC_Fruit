#include"detect_ball.h"
#include<iostream>
#include<opencv2/opencv.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgcodecs/imgcodecs.hpp>
#include<time.h>
#include<string>

using namespace std;
using namespace cv;

Mat Detect_Ball::color_fillter(int color, Mat img) {//yellow=1 white=0
	// imshow("imhhhhh", img);
	if (color) {
		cvtColor(img, img, COLOR_BGR2HLS);
		inRange(img, Scalar(0, 90, 160), Scalar(30, 255, 255), img);
	}
	else {
		inRange(img, Scalar(220, 220, 230), Scalar(255, 255, 255), img);
	}
	return img;
}

vector<Vec3f> Detect_Ball::find_circle(Mat img, int color, int circle_number){
img = color_fillter(color,img);
// cout<<"img depth: "<<img.depth()<<"  img size: "<<img.size()<<endl;
imshow("filtercolor",img);
Mat blurImg;
GaussianBlur(img, blurImg, cv::Size(11, 11), 2, 2);
Mat brightimg;
threshold(blurImg, brightimg, 127, 255, cv::THRESH_BINARY);
Mat kernel,closeimg;
kernel = getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5));
morphologyEx(brightimg, closeimg, cv::MORPH_CLOSE, kernel);
// imshow("closed", closeimg);
Mat element, erodeImg, dilateImg;
element = getStructuringElement(cv::MORPH_RECT, cv::Size(3, 3));
erode(closeimg, erodeImg, element, cv::Point(-1, -1), 3);
dilate(erodeImg, dilateImg, element, cv::Point(-1, -1), 5);
// imshow("dilate", dilateImg);
Canny(dilateImg,img,10,100);
int num = 0;
float r_min = rmin;
vector<Vec3f> circles;
while (num != circle_number && r_min < rmin_threshold) {
	HoughCircles(img,circles,HOUGH_GRADIENT,1,100,100,
		HoughCircles_param2,r_min,rmax);
	if (circles.empty())
		continue;
	num = circles.size();
	// cout << "circle detected" << endl;
}
	return circles;
}

 ResultCircle Detect_Ball::detect_circles(int cam,int color, int circle_number) {
	ResultCircle circleImg;
	cout << "detecting starts"<<endl;
	clock_t start, finish;
	time_t t0 = GetTime();
	start = clock();
	bool detect_fail = 0;
	int sample_time = 0;
	Mat frame;
	int num;
	vector<float> x_table;
	vector<float> y_table;
	vector<float> r_table;
	vector<Vec3f> circles;
	VideoCapture capture(cam);
	while (sample_time < sample_times_circles) {
		detect_fail = 0;
		time_t task_time = GetTime() - t0;
		if (!time_out_en_circles && task_time >= time_out_circles) {
			cout << "time runs out" << endl;
			detect_fail = 1;
			break;
			
		}
		capture >> frame;
		if (frame.empty())
			continue;
		if(waitKey(1) == 27)
			break;
		circles = find_circle(frame, color, circle_number);
		if (circles.empty())
			continue;

		if (circles[0][2] == 0)
			continue;
		num = circles.size();
		sample_time++;
		for (int i = 0;i < num;i++) {
			circle(frame, Point(circles[i][0], circles[i][1]), circles[i][2], Scalar(255, 0, 100), 2);

		}

		/* sort circles*/
		if(num == 2){
			if(circles[0][0] > circles[1][0]){
				Vec3f temp = circles[0];
				circles[0] = circles[0];
				circles[1] = temp;
			}
		}
		x_table.push_back(circles[0][0]);
		y_table.push_back(circles[0][1]);
		r_table.push_back(circles[0][2]);
		imshow("circles", frame);
		// waitKey(1);
	}

	// CvMatImage frameStr;
	// char* frameStr = mattostring(frame);
	// unique_ptr<char> unique_img(frameStr);

	/*select circle*/
	if(detect_fail){
		capture.release();
		Vec3f temp;
		temp[0] = 0;
		temp[1] = 0;
		temp[2] = 0;

		CircleStruct Circle = vec3fToStruct(temp);
		circleImg.circles = Circle;
		circleImg.img = frame;
		return circleImg;
	}else{
		cout<<"x_table: ";
		for(int i=0; i<x_table.size(); i++){
			cout<<"( "<<x_table[i]<<", "<<y_table[i]<<",  "<<r_table[i]<<")"<<endl;
		}
		cout<<endl;
	}

	vector<float> x_select = z_score(x_table, x_select_ref);

	if(!notAny){
		capture.release();
		Vec3f temp;
		temp[0] = 0;
		temp[1] = 0;
		temp[2] = 0;

		CircleStruct Circle = vec3fToStruct(temp);
		circleImg.circles = Circle;
		circleImg.img = frame;
		return circleImg;
	}

	float x_sum =0, y_sum =0, r_sum = 0,real_time = 0;

	for (int i = 0; i < x_select.size(); i++)
	{
		if(x_select[i]){
			x_sum += x_table[i];
			y_sum += y_table[i];
			 r_sum += r_table[i];

			real_time += 1;
		}
	}

	capture.release();

	Vec3f C;
	C[0] = int(x_sum / real_time);
	C[1] = int(y_sum / real_time);
	C[2] = int(r_sum / real_time);
	CircleStruct CS;
	CS = vec3fToStruct(C);
	circleImg.circles = CS;
	circleImg.img = frame;

	finish = clock();
	double   duration;
	duration = (double)(finish - start) / CLOCKS_PER_SEC;
	cout<<"time: "<<duration<<endl;
	destroyAllWindows();
	return circleImg;
}

int Detect_Ball::detect_type(int cam, int mode) {
	double best_match = 0;
	int fruit_type = 0;
	Point left_top;
	Point right_bottom;
	
	// vector<Vec3f> circle;
	time_t t0 = GetTime();
	ResultCircle circleImg;
	Mat img;
	Mat img_roi;
	while (fruit_type == 0) {
		time_t task_time = GetTime() - t0;
		if (!time_out_en && task_time >= time_out_DetectType) {
			cout << "time runs out" << endl;
			break;
		}
		circleImg = detect_circles(cam, 1, 2 - mode);

		// CvMatImage tempImg;
		// char* tempImg = circleImg.img;
		// img = Mat(tempImg.rows, tempImg.cols, tempImg.channels, tempImg.data);
		img = circleImg.img;

		CircleStruct circle;

		circle = circleImg.circles;
		double l_t_x, l_t_y, r_b_x, r_b_y;
		l_t_x = circle.centerX - circle.R;
		l_t_y = circle.centerY - circle.R;
		r_b_x = circle.centerX + circle.R;
		r_b_y = circle.centerY + circle.R;

		if (l_t_x < 0)
			l_t_x = 0;
		if (l_t_y < 0)
			l_t_y = 0;
		if (r_b_x <= 639){
			r_b_x = r_b_x;
		}else{
			r_b_x = 639;
		}

		if (r_b_y <= 479){
			r_b_y = r_b_y;
		}else{
			r_b_y = 479;
		}

		img_roi = img(Rect(l_t_x, l_t_y, r_b_x - l_t_x, r_b_y - l_t_y));

		if (img_roi.empty()) {
			cout << "detect fail" << endl;
			img_roi = img;
		}
		cout << "type detecing starts" << endl;
		for (int i = 1;i < 5;i++) {
			int pic = 0;
			for (int j = 1;j < n_pic_per_type + 1;j++) {
				stringstream str;
				str  << "../template_f/" << i << j << ".jpg";
				cout<<"str: "<<str.str()<<endl;
				Mat templateimg = imread(str.str());
				int temp_h,temp_w;
				temp_h = templateimg.cols;
				temp_w = templateimg.rows;
				int roi_h, roi_w;
				roi_h = img_roi.cols;
				roi_w = img_roi.rows;
				if (temp_h > roi_h || temp_w > roi_w) {
					cout << "err!templ oversizeQAQ" << endl;
					return 0;
				}
				Mat res;
				
				matchTemplate(img_roi,templateimg,res,TM_CCOEFF_NORMED);
				double min_val = 0;
				double max_val = 0;
				Point min_loc, max_loc;
				minMaxLoc(res,& min_val,& max_val,&min_loc,&max_loc);

				if (max_val > best_match) {
					best_match = max_val;
					fruit_type = i;
					left_top = max_loc;
					right_bottom =Point (left_top.x + temp_w, left_top.y + temp_h);
					pic = j;
				}
				cout << "type: " << i << " pic: " << j << " max_val: " << max_val << " max pic: " << pic << " detected type: " << fruit_type << endl;

			}
			rectangle(img_roi, left_top, right_bottom, Scalar(255, 0, 255), 2);
			// string fruitType = "type" + fruit_type;
			// putText(img_roi, fruitType, left_top, FONT_HERSHEY_SIMPLEX, 1, Scalar(0.255, 0), 2);
			imshow("match", img_roi);
			waitKey(50);
		}
	}

	
	destroyAllWindows();
	cout << "fruit type detected as" <<fruit_type<< endl;
	return fruit_type;
}

int Detect_Ball::check_grab(int cam, int color) {
	int count = 0;
	int grab_ok = 0;
	//这个windows和linux不一样,休眠时间的单位好像也不一致
	sleep(.5);
	time_t t0 = GetTime();
	VideoCapture capture(cam);
	while (!grab_ok) {
		count += 1;
		Mat img, ret;
		capture >> img;
		if(img.empty()){
			cout<<"error img!"<<endl;
			break;
		}
		ret = img;
		time_t task_time = GetTime() - t0;
		if (task_time >= 5) {
			cout << "time runs out" << endl;
			break;
		}
		if (ret.empty()) {
			break;
		}else {
			Rect rect(Point(check_grab_roi[2], check_grab_roi[0]), Point(check_grab_roi[3], check_grab_roi[1]));
			Mat img_roi = img(rect);
			img_roi = color_fillter(color, img_roi);
			rectangle(img, rect, Scalar(255, 0, 255), 2);
			imshow("img", img);
			resize(img_roi, img_roi, Size(300, 300));
			imshow("img_roi", img_roi);
			resize(img_roi, img_roi, Size(50, 20));
			waitKey(1);
			int sum = 0, blacksum = 0;
			for (int i = 0; i < img_roi.rows; ++i) {         
				for (int j = 0; j < img_roi.cols; ++j) {
					sum++;
					if (img_roi.at<uchar>(i, j) > 25) {//这是针对单通道图像的写法，bgr是.at<Vec3f>(i,j)[0]~[2]依次判断，colorfilter中对color为0的情况没有转换色彩空间，对color为1时转换成了hls
						blacksum++;
					}
				}
			}

			double black_rate = blacksum / sum;
			cout<<"Rate: "<<black_rate<<endl;
			if (black_rate > 0.8){
				cout << "成功抓取到"<<endl;
				grab_ok = 1;
				waitKey(1000);
			}
		}

	}
	if (!grab_ok)
		cout << "grab fails" << endl;
	
	cout<<"count: "<<count<<endl;
	destroyAllWindows();
	capture.release();

	return grab_ok;
}



extern "C" {

	

	//detect_circles
	detect_circless detect_circles(int Cam,int Color, int Circle_number){
		returndata circleImage;
		Detect_Ball db;
		detect_circless dc;

		circleImage = db.detect_circles(Cam, Color, Circle_number);

		char* imgString = mattostring(circleImage.img);
		unique_ptr<char> un_s(imgString);

		// dc.circles = circleImage.circles;
		dc.img = imgString;
		dc.cols = circleImage.img.cols;
		dc.rows = circleImage.img.rows;
		dc.channels = circleImage.img.channels();
		dc.x = circleImage.circles.centerX;
		dc.y = circleImage.circles.centerY;
		dc.r = circleImage.circles.R;

		return dc;
	}

	//detect_type
	int detect_type_(int cam, int mode){
		Detect_Ball db;
		int rel = db.detect_type(cam, mode);

		return rel;
	}
	//check_grab
	int check_grab_(int cam, int color){
		Detect_Ball db;
		int grab = db.check_grab(cam, color);

		return grab;
	}

}
