#pragma once
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/opencv.hpp>
#include<opencv2/imgproc/imgproc.hpp>
#include<time.h>
#include<iostream>
#include<algorithm>
#include<string>
using namespace std;
using namespace cv;


typedef struct returnDate
{
	int flag ;
	Mat image;
}Result_sign;

class Detect_turn {
	float area_threshold = 10000;//minium of size
	int sample_time = 9;//sampling times
	double max_val_threshold = 0.3;//minium similarity
	time_t time_out = 8;
	bool time_out_en = true;

public:
	Point2f pt[4];
	double max_val1;
	double max_val2;
	double max_val3;
	double min_val1;
	double min_val2;
	double min_val3;
	double maxval;
	int times[10];
	Detect_turn()=default;
	~Detect_turn()=default;
	int majorityElement(int* nums, int len);
	string turn_mapping(int turn);
	Result_sign find_sign(int flag,Mat img);
	int match_template(Mat img);
	int detect_turn(int cam);
	
};

int Detect_turn::majorityElement(int* nums, int len) {
	sort(nums, nums + len);

	int i = 0;
	int MaxCount = 1;
	int index = 0;
 
	while (i < len - 1)//遍历
	{
		int count = 1;
		int j ;
		for (j = i; j < len - 1; j++)
		{
			if (nums[j] == nums[j + 1])//存在连续两个数相等，则众数+1
			{
				count++;
			}
			else
			{
				break;
			}
		}
		if (MaxCount < count)
		{
			MaxCount = count;//当前最大众数
			index = j;//当前众数标记位置
		}
		++j;
		i = j;//位置后移到下一个未出现的数字
	}
	return nums[index];
}

string Detect_turn::turn_mapping(int turn) {
	string instructure;
	switch (turn) {
	case 1:instructure = "left";break;
	case 2:instructure = "ahead";break;
	case 3:instructure = "right";break;
	}
	return instructure;
}


int GetTime() {
	time_t t;
	t = time(NULL);
	return t;
}



