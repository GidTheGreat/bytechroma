# bytechroma
Bare-metal terminal renderer built entirely on 
ANSI escape codes.
Designed for ultra-fast terminal updates where 
print() spam and heavy renderers become 
the bottleneck. Ideal for websocket feeds,
market data, logs, telemetry, 
and realtime dashboards.

# Features 
- Pure ANSI rendering
- Minimal CPU overhead
- Zero UI framework dependency
- Optimized for high-frequency updates
- Key/value style rendering
- Optional batching for extreme throughput

# Installation 
```
   pip install bytechroma
   pip install git+https://github.com/GidTheGreat/bytechroma.git
```
# Basic Usage
```
   from bytechroma import ByteChroma
    bc = ByteChroma()
    bc.update("price", "104532")
    bc.update("volume", "82.1")
```

# High Frequency Streams
```
    import threading
    from bytechroma import ByteChroma
    bc = ByteChroma(interval=2)
    t = threading.Thread(target=bc.auto_flush_loop)
    t.daemon = True
    t.start()
    bc.update("btc", "104532")
    bc.update("eth", "5921")
```

## Why batching helps

  ### without batching
  ```
     update -> render -> flush
     update -> render -> flush
     update -> render -> flush
   ```
   ### with batching
   ```
      1000 updates -> single render -> single flush
   ```
    + less terminal I/0
    + less redraw pressure
    + smoother feeds

## Use cases
* Crypto orderbooks
* Websocket feeds
* Realtime monitoring
* CLI dashboards
* Telemetry streams
* Low-overhead logging

## Philosophy
Most terminal libraries optimize aesthetics.
bytechroma optimizes throughput
    
    
