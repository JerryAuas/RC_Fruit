// change uchar* to mat
#include<iostream>
#include<opencv2/opencv.hpp>


using namespace std;
using namespace cv;

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
char* mattostring(uchar* frame_data, int rows, int cols, int channels){
    Mat mat = readfrombuffer(frame_data,rows,cols,channels);
    if (!mat.empty()) {

        vector<uchar> data_encode;
        vector<int> compression_params;
        compression_params.push_back(CV_IMWRITE_PNG_COMPRESSION);  // png 选择jpeg  CV_IMWRITE_JPEG_QUALITY
        compression_params.push_back(1); //在这个填入你要的图片质量 0-9

        imencode(".png", mat, data_encode);

        std::string str_encode(data_encode.begin(), data_encode.end());
        char* char_r = new char[str_encode.size() + 10];     
        memcpy(char_r, str_encode.data(), sizeof(char) * (str_encode.size()));
        return char_r;
    }
}
extern "C"{
    char* mattostring1(uchar* matrix, int rows, int cols, int channels)
    {
       
        return mattostring(matrix, rows, cols,  channels);
    }
}
