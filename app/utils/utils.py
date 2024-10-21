import asyncio
import threading

def async_to_sync(fn, *args, **kwargs):
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        thread_name = f"Thread Runner with loop for task {fn.__name__}"
        thr = threading.Thread(target=loop.run_forever, name=thread_name, daemon=True)
        if not thr.is_alive():
            thr.start()
        coro = fn(*args, **kwargs)
        future = asyncio.run_coroutine_threadsafe(coro, loop)
        return future.result()
    return wrapper