
# Description

Coding was done on Macbook with Docker Desktop for Mac. If something is wrong, please contact an author. 

## Prerequisites:  

 - docker
 - docker-compose
 - web-browser
 - psql (optional)

### Options
- You can scale Citus workers by using command-line argument --scale worker=N (ex.: --scale worker=4)

## What to do:  
1. Run `docker-compose build`
2. Run `docker-compose up`
3. Wait until the container "set_up" outputs `"SET UP DONE"` 
4. Find in the output lines:
   `"Uvicorn running on http://0.0.0.0:8001"` and
   `"Uvicorn running on http://0.0.0.0:8002"` – API is ready to explore
5. Now you can open web-browser and navigate either to:
    
    players API - `http://127.0.0.1:8001/docs#/`
    or

    publisher/studio API - `http://127.0.0.1:8002/docs#/`

## Note
FastAPI + SQLAlchemy + asyncpg + Citus database.

FastAPI is an asynchronous framework built atop of asyncio library, and expected to have high-performance out of the box.

The REST API is divided into distinct pieces - `players` and `publisher, studio`.
They are running in separate containers and can be scaled up by employing load-balancing service (nginx, HAProxy, etc.)

Citus database was chosen as a drop-in replacement for Postgres.
Tables `players`, `players_games` are distributed across the cluster and will scale up nicely with the number of the players.
Other tables are expected to be way smaller, so they duplicated to each Citus worker (referenced tables).

#### How to login:
The set-up sequence will generate fake players, users, games and studios in the database.
Also, they will be dumped into files `players.csv`, `users.csv` in your current directory.

### TO-DO

* Research for using two databases at the same time (single node and sharded for different parts of the system) 
* Better support for switching between Postgres and Citus for development
* Refactor API routers
* Integrate load-balancer
* Refactor authentication system
* Refactor authorization system
* Learn how to use Citus
* Optimize SQL queries when needed