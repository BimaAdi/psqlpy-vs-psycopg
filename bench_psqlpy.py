from time import time

from faker import Faker
from psqlpy import ConnectionPool, ConnectionPoolBuilder

from setting import (
    POSTGRESQL_DATABASE,
    POSTGRESQL_HOST,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_PORT,
    POSTGRESQL_USER,
)
from shared import BenchTypedDict


async def create_table(db_pool: ConnectionPool):
    await db_pool.execute("""
        CREATE TABLE IF NOT EXISTS todo (
            id serial PRIMARY KEY,
            todo text,
            is_done bool)
        """)


async def insert_bulk(db_pool: ConnectionPool):
    fake = Faker()
    conn = await db_pool.connection()
    transaction = conn.transaction()
    transaction.begin()
    for _ in range(100):
        await db_pool.execute(
            """
        INSERT INTO todo (todo, is_done) VALUES ($1, $2)
        """,
            [fake.pystr(), fake.pybool()],
        )
    transaction.commit()


async def get_bulk(db_pool: ConnectionPool):
    results = await db_pool.execute("SELECT id, todo, is_done FROM todo LIMIT 30")
    for item in results.result():
        _ = item


async def drop_table(db_pool: ConnectionPool):
    await db_pool.execute("DROP TABLE IF EXISTS todo")


async def bench() -> BenchTypedDict:
    bench_time: BenchTypedDict = {"insert_bulk_time": 0.0, "get_bulk_time": 0.0}
    try:
        db_pool = (
            ConnectionPoolBuilder()
            .user(POSTGRESQL_USER)
            .password(POSTGRESQL_PASSWORD)
            .host(POSTGRESQL_HOST)
            .port(POSTGRESQL_PORT)
            .dbname(POSTGRESQL_DATABASE)
            .build()
        )
        await create_table(db_pool=db_pool)

        start = time()
        await insert_bulk(db_pool=db_pool)
        end = time() - start
        bench_time["insert_bulk_time"] = end

        start = time()
        await get_bulk(db_pool=db_pool)
        end = time() - start
        bench_time["get_bulk_time"] = end

        await drop_table(db_pool=db_pool)
    finally:
        db_pool.close()

    return bench_time
