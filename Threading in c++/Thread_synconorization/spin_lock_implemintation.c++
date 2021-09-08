#include <iostream>
#include <thread>
#include <mutex>       
#include <chrono>
#include <condition_variable> 
#include <atomic>

using namespace std;


volatile long long shared = 0;
mutex m;
class SpinLock
{
    atomic<int> state =0;

public:
    void lock()
    {   
        //memory_order_acquire:
        //Acquire operation: no reads in the current thread can be reordered before this load.
        //atomic_exchange_explicit:
        //set the atomic value to the value that we send and return the oldd value
        while (atomic_exchange_explicit(&state, 1, memory_order_acquire))
        {
            //cout << this_thread::get_id() <<state << endl;
            continue;
        }

    }
    void unlock()
    {
        //memory_order_release:
        //Release operation: no writes in the current thread can be reordered after this store.
        //atomic_store_explicit(&state, 0, memory_order_release);
        //or
        state.store(0);
        
    }
};
SpinLock mm;

void count()
{
    for (int i = 1; i <= 1000000000; i++)
    {
        mm.lock();
        shared = shared + i;
        mm.unlock();
    }
}
using namespace std::chrono;

int main()
{
    auto start = high_resolution_clock::now();
    thread t1(count);
    thread t2(count);
    t1.join();
    t2.join();
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(stop - start);
    cout << "result: "<<shared<<endl;
    cout <<"time in milliseconds : " <<duration.count() << endl;
    return 0;
}
