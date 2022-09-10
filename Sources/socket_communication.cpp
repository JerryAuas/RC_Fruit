// #include "dofbot_kinemarics.h"

/*
g++ -o test.so -shared -fPIC test.cpp
*/
#include <iostream>


#include "stdio.h"
#include "stdlib.h"
#include <unistd.h>
#include "sys/types.h"
#include <sys/stat.h>
#include "string.h"
#include <arpa/inet.h>
#include <sys/un.h>

using namespace std;


void socket_communication(char *str){

    struct sockaddr_un serv, client;

    char ADDR[] =  "/home/jetson/dofbot_ws/src/dofbot_moveit/src/server.sock";

    int sock = socket(AF_UNIX, SOCK_STREAM, 0);
}