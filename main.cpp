#include<iostream>
#include<opencv2/opencv.hpp>
using namespace std;
using namespace cv;

int main()
{
    Mat img;
    VideoCapture cap;
    cap.open(3);    

    while (cap.read(img))
    {
        /* code */
        // cap.read(img);

        imshow("q23", img);


        waitKey(1);
    }

    waitKey(0);

    return 0;
    
}