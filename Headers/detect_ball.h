#pragma once
#include<iostream>
#include<opencv2/opencv.hpp>
#include<opencv2/highgui/highgui.hpp>
#include<opencv2/imgcodecs/imgcodecs.hpp>
#include<vector>
#include<time.h>
// #include<seeta/Common/Struct.h>
#include<unistd.h>
#include<string>

using namespace std;
using namespace cv;


//img to string imgsize
int rows_ = 640;
int cols_ = 480;


struct CvMatImage{
    //cv图片结构体
    int rows;
    int cols;
    int channels;
    uchar *data;
};

struct CircleStruct
{
	float centerX;
	float centerY;
	float R;
};


typedef struct returndata{ 
	Mat img;
	CircleStruct circles;

}ResultCircle;

struct detect_circless
{
	int rows;
	int cols;
	int channels;
	char* img;

	float x;
	float y;
	float r;
	// CircleStruct circles;
};


class Detect_Ball {
	float rmin = 30;
	float rmax = 90;
	float rmin_threshold = 86;
	double HoughCircles_param2 = 18;
	int check_grab_roi[4] = { 459, 479, 254, 304 };
	double x_select_ref = 0.8;  //数据标准化参考值

	int n_pic_per_type = 3;
	// double best_match = 0;
	int sample_times=9;

	/* detect_circles*/
	int sample_times_circles = 20;
	time_t time_out_circles = 10;
	time_t time_out_en_circles=false;

	time_t time_out=5;
	time_t time_out_DetectType = 8;
	time_t time_out_en=false;

	/* detect_type*/
	


public:
	Detect_Ball() = default;
	~Detect_Ball() = default;
	Mat color_fillter(int color, Mat img);
	vector<Vec3f> find_circle(Mat img, int color, int circle_number);
	ResultCircle detect_circles(int cam, int color, int circle_number);
	int detect_type(int cam, int mode);
	int check_grab(int cam, int color);
	int GetTime();
	string fruit_mapping(int type);



};

int Detect_Ball:: GetTime() {
	time_t t;
	t = time(NULL);
	return t;
}

string Detect_Ball::fruit_mapping(int type) {
	string fruit;
	switch (type) {
	case 1:fruit = "蓝莓";break;
	case 2:fruit = "红枣";break;
	case 3:fruit = "草莓";break;
	case 4:fruit = "无花果";break;

	}
	return fruit;
}

/*转换图片*/
Mat readfrombuffer(uchar* frame_data,int height, int width,int channels){
    if(channels == 3){
        Mat img(height, width, CV_8UC3);
        uchar* ptr =img.ptr<uchar>(0);
        int count = 0;
        for (int row = 0; row < height; row++){
             ptr = img.ptr<uchar>(row);
             for(int col = 0; col < width; col++){
	               for(int c = 0; c < channels; c++){
	                  ptr[col*channels+c] = frame_data[count];
	                  count++;
	                }
	         }
        }
        return img;
    }
}
/**
 * @brief 转换MAT  -》 string
 * 
 * @param img 
 * @return char* 
 */
char* mattostring(Mat img){
    // Mat img = readfrombuffer(frame_data,rows,cols,channels);
    if (!img.empty()) {

        vector<uchar> data_encode;
        vector<int> compression_params;
        compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);  // png 选择jpeg  CV_IMWRITE_JPEG_QUALITY
        compression_params.push_back(1); //在这个填入你要的图片质量 0-9

        imencode(".png", img, data_encode);

        std::string str_encode(data_encode.begin(), data_encode.end());
        char* char_r = new char[str_encode.size() + 10];     
        memcpy(char_r, str_encode.data(), sizeof(char) * (str_encode.size()));
        return char_r;
    }
}

/*数据类型转换*/
CircleStruct vec3fToStruct(Vec3f circle){
	CircleStruct Circle;
	Circle.centerX = circle[0];
	Circle.centerY = circle[1];
	Circle.R              = circle[2];

	return Circle;
}

/*运算符重载*/
string operator+(string& content, int number) {
	string temp = "";
	char t = 0;
	while (true) {
		t = number % 10 + '0';
		temp = t + temp;
		number /= 10;
		if (number == 0) {
			return content + temp;
		}
	}
}
string& operator+=(string& content, int number) {
	return content = content + number;
}

// ostream & operator <<(ostream &out, stringstream& str){
// 	out<<str.data<<endl;
// }


/*数据标准化*/


/**
 * 求平均值
 */
float average(vector<float> table)
{
    float sum = 0;
    for (int i = 0; i < table.size(); i++)
        sum += table[i];
    return sum/table.size(); 
}
/**
 * 求方差
 */
float variance(vector<float> table)
{
    float avg = average(table);
	float sum = 0;
    for (int i = 0; i < table.size(); i++)
        sum += pow(table[i] - avg, 2);
    return sum/table.size(); 
}
/**
 * 求标准差
 */
float stds(vector<float> table)
{
    float vac = variance(table);
    return sqrt(vac); 
}
/**
 * @brief 
 * 数据标准化
 * @param table 
 * @param ref 
 * @return vector<double> 
 */
vector<float> z_score(vector<float> table, float ref){
	//取平均值
	float mean = average(table);
	float std = stds(table);

	if(!std){
		for(int i = 0; i<table.size(); i++){
			table[i] = 1;
		}
		return table;
	}

	vector<float> stats_z;
	for(int i =0; i<table.size(); i++){
		stats_z.push_back(float((float(i) - mean)/std));
	}

	for (int i = 0; i < stats_z.size(); i++)
	{
		if(stats_z[i] < ref){
			stats_z[i] = 1;
		}else{
			stats_z[i] = 0;
		}

		return stats_z;
	}
	


}

/**
 * @brief 
 * 判断容器中true的个数，大于0返回true
 * @param sel 
 * @return true 
 * @return false 
 */
bool notAny(vector<float> sel){
	int sum = 0;
	for (int i = 0; i < sel.size(); i++)
	{
		if(sel[i] != 0){
			sum++;
		}
	}

	if (sum!=0)
	{
		return true;
	}else{
		return false;
	}
	
	
}