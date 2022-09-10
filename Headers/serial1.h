  /**************************************************************
Authors:    Jerry Ler
**************************************************************/
#pragma once

#include<iostream>
#include <fstream>
#include <stdio.h>
#include <stdint.h>
#include <mutex>
#include <chrono>
#include<thread>
#include <cmath>
#include "queue"



/* Serial frame's EOF may conflict with somewhere else's EOF */
#undef EOF


    struct ControlData
{
    float retValue;
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

private:
    /* -1 if serial port not opened */
    int _serialFd;

    int _errorCode;


    // 控制返回值
    struct ControlSerial
    {
        float retValue;
    }_controlSerial;


    std::timed_mutex _mutex;


    // 返回状态值

    int ret;

public:
    void try1(float angle);

    int send();

};


