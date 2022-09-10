#pragma once
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/opencv.hpp>
#include<opencv2/imgcodecs/imgcodecs.hpp>
#include<time.h>
#include<iostream>
#include<algorithm>
#include<string>
#include"detect_turn.h"
using namespace std;
using namespace cv;

returnDate Result;

Mat convertTo3Channels(const Mat& binImg)
{
    Mat three_channel = Mat::zeros(binImg.rows,binImg.cols,CV_8UC3);
    vector<Mat> channels;
    for (int i=0;i<3;i++)
    {
        channels.push_back(binImg);
    }
    merge(channels,three_channel);
    return three_channel;
}


returnDate Detect_turn::find_sign(int flag,Mat img) {
	
	Mat mask, copy;
	img.copyTo(copy);//image pretreatment
	cvtColor(img, mask, cv::COLOR_BGR2HSV);
	inRange(mask, Scalar(100, 100, 50), Scalar(124, 255, 200), mask);
	// imshow("mask", mask);
	Mat blurImg;
	GaussianBlur(mask, blurImg, cv::Size(11, 11), 2, 2);
	Mat brightimg;
	threshold(blurImg, brightimg, 80, 150, cv::THRESH_BINARY);

	// imshow("erzhi", brightimg);
	Mat kernel;
	kernel = getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5));
	morphologyEx(brightimg, mask, cv::MORPH_CLOSE, kernel);
	Mat element, erodeImg, dilateImg;
	erode(mask, erodeImg, kernel, cv::Point(-1, -1), 3);
	dilate(erodeImg, dilateImg, kernel, cv::Point(-1, -1), 5);

	// imshow("dilate", dilateImg);
	vector<vector<Point> >contours;//find&draw contours
	vector<Vec4i> hierarchy;
	findContours(dilateImg.clone(), contours,hierarchy, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE, Point());
	// for (int i = 0; i < (int)contours.size(); i++)
	// {
	// drawContours(img, contours, i, Scalar(0, 0, 255), 3, 8);
	// }
	// imshow("drawContours", img);
	// cout <<"contours size: "<< contours.size()<<endl;

	//筛选剔除掉面积小于area_threshold的轮廓
	vector <vector<Point>>::iterator iter = contours.begin();
	for (; iter != contours.end();){
		double g_dConArea = contourArea(*iter);
		if (g_dConArea < area_threshold){
			iter = contours.erase(iter);
		}else{
			++iter;
		}
	}

	drawContours(copy, contours, -1, Scalar(0,0,255), 3);
	imshow("copy", copy);
	
	Point2f l_t, r_b;	
	for (int i = 0; i < (int)contours.size(); i++){
		RotatedRect rect = minAreaRect(contours[i]);
		// The order is bottomLeft, topLeft, topRight, bottomRight.
		rect.points(pt);
		l_t = pt[1];
		r_b = pt[3];
		// cout<<l_t.x<<"     "<<l_t.y<<"r       "<<r_b.x<<"    "<<r_b.y<<endl;
		Mat img_src = img(cv::Rect(l_t, r_b));
		// cout<<"imgsize: "<<img_src.size()<<endl;
		// resize(img_src, img_src, Size(30, 30));
		imshow("sign", img_src);
		resize(img_src, img_src, Size(30, 30));
		flag =1;

		Result.flag = flag;
		Result.image = img_src;

		// imshow("test", Result.image);

		break;
	}
	return Result;
}



int Detect_turn::match_template(Mat img) {
	Mat res_right, res_left, res_ahead;

	Mat template_left = imread("../template_t/left.jpg");
	Mat template_right = imread("../template_t/right.jpg");
	Mat template_ahead = imread("../template_t/ahead.jpg");

	matchTemplate(img, template_left, res_left, TM_CCOEFF_NORMED);
	
	matchTemplate(img, template_right, res_right, TM_CCOEFF_NORMED);
	matchTemplate(img, template_ahead, res_ahead, TM_CCOEFF_NORMED);
	minMaxLoc(res_left, &min_val1, &max_val1);
	minMaxLoc(res_right, &min_val2, &max_val2);
	minMaxLoc(res_ahead, &min_val3, &max_val3);
	double maxval = max(max_val1, max_val2);
	maxval = max(maxval, max_val3);

	cout<<"max_val1: "<<max_val1<<"  max_val2: "<<max_val2<<"  m ax_val3: "<<max_val3<<"max: "<<maxval<<endl;
	if (maxval < max_val_threshold){
			return 0;
	}else if (maxval == (max_val1)){
		return 1;
	}else if (maxval == (max_val2)){
		return 2;
	}else if(maxval == (max_val3)){
		return 3;
	}

	waitKey(0);
}

int Detect_turn::detect_turn(int cam) {
	int majorElement = 2;//default=straight
	int turn_current;
	int count = 0;//statistics sampling times

	 
	VideoCapture capture(cam);
	
	cout << "Detecting starts" << endl;
	time_t t0 = GetTime();
	while (1) {
		time_t task_time = GetTime() - t0;
		if (!time_out_en && task_time >= time_out) {
			cout << "Time runs out" << endl;
			break;
		}
		else {
			Mat frame;
			capture >> frame;
			// cout<<"imgsize: "<<frame.size()<<endl;
			if (frame.empty())
				continue;
			// imshow("vedio", frame);
			waitKey(1);
			int flag =0;
			Result = find_sign(flag,frame);
			


			flag = Result.flag;
			frame = Result.image;
			// cout<<"flag: "<<flag<<"   s ize: "<<frame.size()<<endl;

			// imshow("123", Result.image);
			if (flag) {
				turn_current = match_template(frame);
				cout<<"turn_current: "<<turn_current<<endl;
			}
			else continue;
			if (turn_current) {
				times[count] = turn_current;
				count++;
			}
			if (count == sample_time) {
				majorElement = majorityElement(times, count);
				// for(int i=0; i<count; i++){
				// 	cout<<times[i]<<"  ";
				// }
				cout<<endl;
				// cout<<"majorElement: "<<majorElement<<endl;
				// cout << "Detecting is over,the next step is" << turn_mapping(majorElement) << endl;
				break;
			}
		}
	}
	destroyAllWindows();
	return majorElement;
}

extern "C"{
	int detect_turn(int cam){
		Detect_turn try1;

		int major = try1.detect_turn(cam);

		return major;
	}

	
}
