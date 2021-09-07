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
    this_thread::sleep_for(chrono::seconds(2));
    state = 1;
    cv.notify_one();

      
}

void thread2()
{
    
        // the cheking is done after we acquire the lock so if notify get called before wait
        // we still gonna able to run because the done is already = 1 so we will not going to call
        // the wait
        cout <<"thread2 will wait"<<endl;
        std::unique_lock<std::mutex> lck(mtx);
        while (state == 0)
        {
            cout << "thread2 will wait" << endl;
            cv.wait(lck);

        }

 

}

int main()
{

    thread t1(thread1);
    thread t2(thread2);
    t1.join();
    t2.join();
    cout << "both threads finish"<<endl;
    return 0;
}
