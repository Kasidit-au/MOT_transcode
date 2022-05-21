def print_log(msg, type='INFO'):
    from datetime import datetime as dt
    print(f'[{dt.now()}] [{type}] {msg}')