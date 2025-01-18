import logging

from fastapi import FastAPI, HTTPException
import redis

"""
An API to fetch data required stats from Redis cache
"""
app = FastAPI()
redis_client = redis.StrictRedis(host="redis", port=6379, decode_responses=True)

@app.get("/users/{user_id}/stats")
def get_user_stats(user_id: str):
    """
    Fetch basic user-level stats.
    :param user_id:
    :type user_id:
    :return:
    :rtype:
    """
    user_key = f"user:{user_id}"
    stats = redis_client.hgetall(user_key)
    if not stats:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "user_id": user_id,
        "order_count": int(stats.get("order_count", 0)),
        "total_spend": float(stats.get("total_spend", 0.0))
    }


@app.get("/stats/global")
def get_global_stats():
    """
     Fetch global stats.
    :return:
    :rtype:
    """
    global_key = "global:stats"
    stats = redis_client.hgetall(global_key)
    return {
        "total_orders": int(stats.get("total_orders", 0)),
        "total_revenue": float(stats.get("total_revenue", 0.0))
    }

@app.get("/users/{user_id}/monthly_stats")
def get_user_monthly_stats(user_id: str, year: int, month: int):
    user_key = f"user:{user_id}:{year}:{month:02d}"

    # Check if the key exists
    key_exists = redis_client.exists(user_key)


    if not key_exists:
        # Key does not exist
        return {"user_id": user_id, "order_count": 0, "total_spend": 0.0}

    stats = redis_client.hgetall(user_key)
    return {
        "user_id": user_id,
        "order_count": int(stats.get("order_count", 0)),
        "total_spend": float(stats.get("total_spend", 0.0)),
    }
