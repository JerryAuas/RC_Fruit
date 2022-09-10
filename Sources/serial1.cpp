/**************************************************************
Authors:    jerry Ler
**************************************************************/
#include <fcntl.h>
#include <unistd.h>
#include <termios.h>
#include <errno.h>
#include <iostream>
#include <fstream>
#include <string>
#include <string.h>
#include <stdexcept>
#include <exception>
#include <stdio.h>
#include <stdint.h>
#include <mutex>
#include <chrono>
#include<thread>
#include <cmath>
#include "queue"

using namespace std;


 struct ControlData
{
    char* retValue;
};


class Serial
{
public:

    Serial();
    Serial(const Serial& right) = delete;
    Serial(Serial&& ) = delete;
    ~Serial();


    int openPort();

    /*
        * @Brief:  close serial port
        */
    int closePort();

    /*
        * @Brief
        */
    bool isOpened() const;



    //控制部分
    template<typename _Rep, typename _Period>
    int tryControl(const ControlData& controlData, const std::chrono::duration<_Rep, _Period>& time_duration)
    {
        std::unique_lock<std::timed_mutex> lockGuard(_mutex, time_duration);
        if(lockGuard.owns_lock())
        {
            control(controlData);
            std::this_thread::sleep_for(std::chrono::milliseconds(1));
            return _errorCode;
        }
        else
        {
            return -1;
        }

    }

public:
    /* -1 if serial port not opened */
    int _serialFd;

    int _errorCode;


    // 控制返回值
    struct ControlSerial
    {
        char* retValue;
    }_controlSerial;


    std::timed_mutex _mutex;


    // 返回状态值

    int ret;

public:

    int control(const ControlData& controlData);

    ControlSerial pack(const ControlData& controlData);

    int send();

};


Serial::Serial():
        _serialFd(-1)
{
    // static_assert(sizeof(ControlSerial) == 1, "Size of backdata is not 4");
}

Serial::~Serial()
{
    tcflush(_serialFd, TCIOFLUSH); //清空终端未完成的输入/输出请求和数据
}

int Serial::openPort()
{
    _serialFd = open("/dev/CH340", O_RDWR | O_NOCTTY | O_NONBLOCK);
    //所提供的环境中已为所需用到的串口设置了别名
    //O_NOCTTY为O_NOCTTY 如果pathname指的是终端设备，则不将此设备分配作为此进程的控制终端。
    //O_NONBLOCK 如果pathname指的是一个FIFO、一个块特殊文件或一个字符特殊文件，则此选择项为此文件的本次打开操作和后续的I/O操作设置非阻塞方式。
    if (_serialFd == -1)
    {
        return _errorCode = 1;;
    }


    termios tOption;                                // 串口配置结构体
    tcgetattr(_serialFd, &tOption);                 //获取当前设置
    cfmakeraw(&tOption);
    cfsetispeed(&tOption, B115200);                 // 接收波特率
    cfsetospeed(&tOption, B115200);                 // 发送波特率
    tcsetattr(_serialFd, TCSANOW, &tOption);
    tOption.c_cflag &= ~PARENB;
    tOption.c_cflag &= ~CSTOPB;
    tOption.c_cflag &= ~CSIZE;
    tOption.c_cflag |= CS8;
    tOption.c_cflag &= ~INPCK;
    tOption.c_cflag |= (B460800 | CLOCAL | CREAD);  // 设置波特率，本地连接，接收使能
    tOption.c_cflag &= ~(INLCR | ICRNL);
    tOption.c_cflag &= ~(IXON);
    tOption.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG);
    tOption.c_oflag &= ~OPOST;
    tOption.c_oflag &= ~(ONLCR | OCRNL);
    tOption.c_iflag &= ~(ICRNL | INLCR);
    tOption.c_iflag &= ~(IXON | IXOFF | IXANY);
    tOption.c_cc[VTIME] = 1;                        //只有设置为阻塞时这两个参数才有效
    tOption.c_cc[VMIN] = 1;
    tcflush(_serialFd, TCIOFLUSH);                  //TCIOFLUSH刷新输入、输出队列。

    return _errorCode = 0;
}

int Serial::closePort()
{
    tcflush(_serialFd, TCIOFLUSH);
    if (-1 == close(_serialFd))
    {
        _errorCode = 1;
    }
    else
    {
        _errorCode = 0;
    }
    return _errorCode;
}

bool Serial::isOpened() const
{
    return (_serialFd != -1);
}

int Serial::control(const ControlData& controlData)
{
    //pack包装字符串并传入
//        controlData = controlData + mode;
    _controlSerial = pack(controlData);
    return send();
}


Serial::ControlSerial Serial::pack(const ControlData& ctrl)
{
    return ControlSerial
            {
                ctrl.retValue
            };
}


int Serial::send()
{
    tcflush(_serialFd, TCOFLUSH);

    int sendCount;
    try
    {
        sendCount  = write(_serialFd, &_controlSerial, sizeof(ControlSerial));
    }
    catch(exception e)
    {
        return _errorCode = 1;
    }

    if (sendCount == -1)
    {
        _errorCode = -2;
    }
    else if (sendCount < static_cast<int>(sizeof(ControlSerial)))
    {
        _errorCode = -2;
    }
    else
    {
        _errorCode = 0;
    }

    return _errorCode;
}

extern "C" int try1(char* val){

    int ret =0;

    ControlData data_;
    std::chrono::duration<double, std::ratio<1, 30>> hz30(3.5);

    data_.retValue = val;

    Serial test;
    
    test.openPort();
    if(test.isOpened()){
        test.tryControl(data_, hz30);
        ret = 1;
    }

    test.closePort();
    

    return ret;
}

