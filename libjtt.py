
def create_tables(cur):
    stmts = (
        'CREATE TABLE IF NOT EXISTS period_data (date TEXT, dh REAL, nh REAL)', 
        'CREATE TABLE IF NOT EXISTS period_params (period TEXT, salary REAL, first REAL, second REAL, relax REAL, bonus REAL, dprise REAL, tax REAL)',
        'CREATE TABLE IF NOT EXISTS config (selected_period TEXT)',
        )

    for stmt in stmts:
        cur.execute(stmt)
