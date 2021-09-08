#include <iostream>
#include <thread>
#include <mutex>       
#include <chrono>
#include <condition_variable> 
#include <atomic>

using namespace std;
using namespace std::chrono;


volatile long long shared = 0;

class YieldLock
{
    atomic<int> state =0;
public:
    long long count;
    void lock()
    {   
        while (atomic_exchange_explicit(&state, 1, memory_order_acquire))
        {
            count ++ ;
            //cout << this_thread::get_id() <<state << endl;
            //The problem with yield is that it has no clear semantics: the kernel has *no* idea what you are waiting for, so it has to guess when to wake you up.4
            //In a word, "yield()" is always a hack.
            this_thread::yield();
     
        }

    }
    void unlock()
    {
        state.store(0);

    }
};
YieldLock mm;

void count()
{
    for (int i = 1; i <= 10000000; i++)
    {
        mm.lock();
        shared = shared + i;
        mm.unlock();
    }
}

//here the diffrence between this and spinlock will not be huge because we spend very little time in critical secition 
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
    cout << mm.count << endl;
    return 0;
}
