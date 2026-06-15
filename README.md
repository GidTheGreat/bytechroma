# bytechroma
Bare metal terminal render to reduce print clutter(purely ansi escape codes)

# Use case
Designed for when you want visibility in websocket feeds but dont want terminal rendering
bottleneck

## Usage
```
pip install bytechroma
   pip install git+https://github.com/GidTheGreat/bytechroma.git

   from bytechroma import ByteChroma
   bc = ByteChroma()

   bc.update("key","value")
```

### if high frequency updates you need to batch updates
```
import threading
    from bytechroma import ByteChroma
    bc = ByteChroma(interval:float)
    e.g. bc = ByteChroma(2) 
    t = threading.Thread(target=auto_flush_loop)
    t.start()
    bc.upadate("key","value")
'''
    
