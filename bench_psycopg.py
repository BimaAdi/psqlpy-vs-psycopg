from time import time
from faker import Faker
import psycopg

from setting import (
    POSTGRESQL_DATABASE,
    POSTGRESQL_HOST,
    POSTGRESQL_PASSWORD,
    POSTGRESQL_PORT,
    POSTGRESQL_USER,
)
from shared import BenchTypedDict


async def create_table(acur: psycopg.AsyncCursor):
    await acur.execute(
        """
        CREATE TABLE IF NOT EXISTS todo (
            id serial PRIMARY KEY,
            todo text,
            is_done bool)
        """
    )


async def insert_bulk(acur: psycopg.AsyncCursor):
    fake = Faker()
    for _ in range(100):
        await acur.execute(
            """
        INSERT INTO todo (todo, is_done) VALUES (%s, %s)
        """,
            (fake.pystr(), fake.pybool()),
        )


async def get_bulk(acur: psycopg.AsyncCursor):
    _ = await acur.execute("SELECT id, todo, is_done FROM todo LIMIT 30")
    async for record in acur:
        _ = record


async def drop_table(acur: psycopg.AsyncCursor):
    await acur.execute("DROP TABLE IF EXISTS todo")


async def bench() -> BenchTypedDict:
    bench_time: BenchTypedDict = {"insert_bulk_time": 0.0, "get_bulk_time": 0.0}
    async with await psycopg.AsyncConnection.connect(
        f"postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:{POSTGRESQL_PORT}/{POSTGRESQL_DATABASE}"
    ) as aconn:
        async with aconn.cursor() as acur:
            await create_table(acur=acur)

            start = time()
            await insert_bulk(acur=acur)
            await aconn.commit()
            end = time() - start
            bench_time["insert_bulk_time"] = end

            start = time()
            await get_bulk(acur=acur)
            end = time() - start
            bench_time["get_bulk_time"] = end

            await drop_table(acur=acur)
            await aconn.commit()

    return bench_time
