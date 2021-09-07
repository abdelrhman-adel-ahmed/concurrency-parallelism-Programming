#include <iostream>
#include <thread>
#include <mutex>       
#include <chrono>
#include <condition_variable> 
using namespace std;

int state = 0;
mutex mtx;
condition_variable cv;
void thread1()
{
    std::unique_lock<std::mutex> lck(mtx);
    //actually here in c++ we can even not sleep because thread are running at the same time "hopfullt" so notifer have higher change 
    //to run first and acquire the lock preventing thread2 from wait and then notify and thread2 miss the notification and stuck waiting for ever
    this_thread::sleep_for(chrono::seconds(2));
    state = 1;
    cv.notify_one();

      
}

void thread2()
{
    while (state == 0)
    {
        cout <<"thread2 will wait"<<endl;
        std::unique_lock<std::mutex> lck(mtx);
        cv.wait(lck);
    }
 

}

int main()
{

    thread t1(thread1);
    thread t2(thread2);
    t1.join();
    t2.join();
    cout << "both thread finsh"<<endl;
    return 0;
}
