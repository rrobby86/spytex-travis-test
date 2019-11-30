from datetime import date

from utils import task_returns, task_raises


# basic calls
test_pow = task_returns("pow.json", 9)
test_date_kw = task_returns("date_kw.json", date(2019, 11, 29))
test_date_pos = task_returns("date_pos.json", date(2019, 11, 29))
test_pow_nested = task_returns("pow_nested.json", 81)
test_range_short = task_returns("range_short.json", range(4))

# bindings
test_pow_bind = task_returns("pow_bind.json", 9)
test_pow_unbound = task_raises("pow_unbound.json", KeyError)
test_pow_bind_run = task_returns("pow_bind_run.json", 81)

# magics
test_pow_run = task_returns("pow_run.json", 81)
test_pow_unpickle = task_returns("pow_unpickle.json", 81)
