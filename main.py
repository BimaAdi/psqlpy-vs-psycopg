import asyncio
from typing import List
from bench_psqlpy import bench as bench_pysql
from bench_psycopg import bench as bench_psycopg
import polars as pl

from shared import BenchTypedDict


async def main():
    bench_result_psqlpy: List[BenchTypedDict] = []
    bench_result_psycopg: List[BenchTypedDict] = []
    for i in range(10):
        print(f"try {i + 1}")
        y = await bench_psycopg()
        bench_result_psycopg.append(y)
        x = await bench_pysql()
        bench_result_psqlpy.append(x)

    with pl.Config() as cfg:
        cfg.set_tbl_formatting("ASCII_MARKDOWN")
        cfg.set_tbl_rows(20)
        print("insert bulk time")
        list_psqlpy_insert_bulk_time = [
            round(i["insert_bulk_time"], 3) for i in bench_result_psqlpy
        ]
        list_psycopg_insert_bulk_time = [
            round(i["insert_bulk_time"], 3) for i in bench_result_psycopg
        ]
        df_insert_bulk_time = pl.DataFrame(
            {
                "": [str(i) for i in range(1, 11)] + ["avg"],
                "psqlpy": list_psqlpy_insert_bulk_time
                + [
                    round(
                        sum(list_psqlpy_insert_bulk_time)
                        / len(list_psqlpy_insert_bulk_time),
                        3,
                    )
                ],
                "psycopg": list_psycopg_insert_bulk_time
                + [
                    round(
                        sum(list_psycopg_insert_bulk_time)
                        / len(list_psycopg_insert_bulk_time),
                        3,
                    )
                ],
            }
        )
        print(df_insert_bulk_time)

        print("get bulk time")
        list_psqlpy_get_bulk_time = [
            round(i["get_bulk_time"], 3) for i in bench_result_psqlpy
        ]
        list_psycopg_get_bulk_time = [
            round(i["get_bulk_time"], 3) for i in bench_result_psycopg
        ]
        df_get_bulk_time = pl.DataFrame(
            {
                "": [str(i) for i in range(1, 11)] + ["avg"],
                "psqlpy": list_psqlpy_get_bulk_time
                + [
                    round(
                        sum(list_psqlpy_get_bulk_time) / len(list_psqlpy_get_bulk_time),
                        3,
                    )
                ],
                "psycopg": list_psycopg_get_bulk_time
                + [
                    round(
                        sum(list_psycopg_get_bulk_time)
                        / len(list_psycopg_get_bulk_time),
                        3,
                    )
                ],
            }
        )
        print(df_get_bulk_time)


asyncio.run(main=main())
