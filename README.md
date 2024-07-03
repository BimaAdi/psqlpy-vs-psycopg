# PSQLPy vs Psycopg

## Requirement
- python 3.12
- poetry 1.8.2
- postgres 12

## Intallation
1. `poetry install`
1. edit setting.py based on postgres configuration
1. `poetry run python main.py`

## Benchmark
### Insert Bulk Time
|     | psqlpy | psycopg |
|-----|--------|---------|
| 1   | 0.271  | 0.096   |
| 2   | 0.269  | 0.184   |
| 3   | 0.319  | 0.216   |
| 4   | 0.38   | 0.097   |
| 5   | 0.378  | 0.117   |
| 6   | 0.288  | 0.139   |
| 7   | 0.287  | 0.159   |
| 8   | 0.267  | 0.101   |
| 9   | 0.285  | 0.107   |
| 10  | 0.448  | 0.181   |
| avg | 0.319  | 0.14    |


### Get Bulk Time
|     | psqlpy | psycopg |
|-----|--------|---------|
| 1   | 0.002  | 0.002   |
| 2   | 0.005  | 0.003   |
| 3   | 0.004  | 0.004   |
| 4   | 0.002  | 0.002   |
| 5   | 0.005  | 0.002   |
| 6   | 0.002  | 0.002   |
| 7   | 0.002  | 0.003   |
| 8   | 0.003  | 0.002   |
| 9   | 0.003  | 0.002   |
| 10  | 0.003  | 0.002   |
| avg | 0.003  | 0.002   |
