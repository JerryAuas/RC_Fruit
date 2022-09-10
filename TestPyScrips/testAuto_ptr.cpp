#define _CRTDBG_MAP_ALLOC
#include<iostream>
#include<mcheck.h>
#include<string.h>
using namespace std;

#include<memory>

int main()
{   
    // mtrace();

    int *p = new int(10);

    unique_ptr<int> pa(p);
    // auto_ptr<int> pa(p);

    // muntrace();
    
    return 0;
}