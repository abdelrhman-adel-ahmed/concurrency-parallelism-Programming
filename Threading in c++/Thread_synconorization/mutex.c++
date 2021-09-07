#include <iostream>
#include <thread>
#include <mutex>       

using namespace std;

volatile long long shared = 0;
mutex mtx;
void count()
{
    for (int i = 1; i <= 1000000; i++)
    {
        mtx.lock();
        shared =shared + i;
        mtx.unlock();
    }
}


int main()
{

    thread t1(count);
    thread t2(count);
    t1.join();
    t2.join();
    cout << shared;
    return 0;
}
