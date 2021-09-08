#include <iostream>
#include <thread>
#include <mutex>       
#include <chrono>
#include <condition_variable> 
#include <atomic>
#include <vector>

using namespace std;
using namespace std::chrono;


/*
            problems:
1- 
scince we using single cv ,we wakes up all waiters and if we have many waiter that will wake up all of them and it wastful because they will fail to acquire the lock except one 
of course if it even grap the lock before a reader come and grap it.
solution:is to use diffrent lock for waiters and readers 

2-starvation ,we can have to many readers that writers will starve ,or we have many writers that successfully grap the lock one after the other and the readers starve 
solution:to solve this we may introduce ticket algorithm like the one i used in python example ,so each thread have a ticket and turn ,and each time one thread try to read we compare
the ticket that generated to that thread with the balance factor that we have e.x we will allow only 3 readers if there writer wait then the writer come 
but here another problem that may be the writer will take long time and cause contention 

3-Locks aren't dealt out in the order they are requested
solution:to solve this we may introduce writer cv for each writer and then put them in a queue and deal with them one by one in the order they came

i will solve one problem after the other in the next few days ,hope you enjoy reading this .
*/

volatile long long shared = 0;
mutex mtx;
condition_variable cv;
volatile int num_readers = 0;
volatile bool write_mode = false;
int arr[5] = {1,2,3,4,5};

void acquire_readlock()
{
    std::unique_lock<std::mutex> lck(mtx);
    while (write_mode)
    {
        cv.wait(lck);
    }
    num_readers++;
}
void release_readlock()
{
    std::unique_lock<std::mutex> lck(mtx);
    num_readers--;
    //if no reader remain notify writer ,note:here we use only one condition var
    if (!num_readers){
        cv.notify_all();
    }
}

void acquire_writelock()
{
    std::unique_lock<std::mutex> lck(mtx);
    //if another writer have the write lock or there is readers
    while (write_mode or num_readers > 0)
    {
        cv.wait(lck);
    }
    write_mode = true;
}
void release_writelock()
{
    std::unique_lock<std::mutex> lck(mtx);
    write_mode = false;
    cv.notify_all();
}
void reader()
{
    for (int i = 1; i <= 10; i++)
    {
        acquire_readlock();
        int index = rand() % 4;
        //cout << this_thread::get_id();
        int val = arr[index];
        cout << "reader " << this_thread::get_id() << " reads "<<val<<endl;
        release_readlock();
    }
}
void writer()
{
    for (int i = 0; i <= 4; i++)
    {
        acquire_writelock();
        int val = rand() % 1000;
        arr[i] = val;
        cout << "writer " << this_thread::get_id() <<" writes " <<val << endl;
        release_writelock();
    }

}

int main()
{
    auto start = high_resolution_clock::now();
    vector<thread> readers;
    vector<thread> writers;
    for (int i = 0; i < 3; i++)
    {
     
        readers.push_back(thread(reader));
        writers.push_back(thread(writer));

    }
    for (std::thread& th : readers)
    {
        th.join();

    }
    for (std::thread& th : writers)
    {
        th.join();

    }

    return 0;
}
