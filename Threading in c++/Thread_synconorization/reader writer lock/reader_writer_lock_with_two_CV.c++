#include <iostream>
#include <thread>
#include <mutex>       
#include <chrono>
#include <condition_variable> 
#include <atomic>
#include <vector>

using namespace std;
using namespace std::chrono;


mutex mtx;
condition_variable reader_cv;
condition_variable writer_cv;

volatile int num_readers = 0;
volatile int num_writers = 0;
volatile bool write_mode = false;
int arr[5] = {1,2,3,4,5};

void acquire_readlock()
{
    std::unique_lock<std::mutex> lck(mtx);
    while (write_mode)
    {
        reader_cv.wait(lck);
    }
    num_readers++;
}
void release_readlock()
{
    std::unique_lock<std::mutex> lck(mtx);
    num_readers--;
    //if no reader remain notify writer ,note:here we use only one condition var
    if (!num_readers){
        writer_cv.notify_all();
    }
}

void acquire_writelock()
{
    std::unique_lock<std::mutex> lck(mtx);
    //if another writer have the write lock or there is readers
    while (write_mode or num_readers > 0)
    {
        writer_cv.wait(lck);
    }
    num_writers++;
    write_mode = true;
}
void release_writelock()
{
    std::unique_lock<std::mutex> lck(mtx);
    num_writers--;
    write_mode = false;
    reader_cv.notify_all();
    //if there other writer so we have to notify them
    //that required if the all readers finish and there is more than one writer waiting 
    if (num_writers)
        writer_cv.notify_all();
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
