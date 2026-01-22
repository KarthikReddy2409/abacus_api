# Abacus Microservice

Running sum calculator with FastAPI + Redis.

## Run

```bash
docker-compose up --build
```

This starts 2 nodes (port 8001, 8002) and redis.

## API

```bash
# add number
curl -X POST http://localhost:8001/abacus/number -H "Content-Type: application/json" -d '{"number": 42}'

# get sum
curl http://localhost:8001/abacus/sum

# reset
curl -X DELETE http://localhost:8001/abacus/sum
```

## Test

```bash
pip install httpx
python test_consistency.py -n 500
```

## How it works

Each node connects to same redis instance. When you POST a number, it uses redis `INCRBYFLOAT` which is atomic at server level. So even if 100 requests hit different nodes at same time, redis handles them one by one internally - no data lost.

GET just reads from redis, DELETE sets it back to 0.

Thats it. No fancy locking or distributed consensus stuff needed because redis does the heavy lifting.
