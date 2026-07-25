def get_user_by_name(name, cursor):
    # Issue: SQL injection (CWE-89)
    query = f"SELECT * FROM users WHERE name = '{name}'"
    cursor.execute(query)
    return cursor.fetchone()


def parse_config(path):
    # Issue: bare except swallows real errors
    try:
        with open(path) as f:
            return f.read()
    except:
        return None


def calculate_discount(price, discount_percent):
    # Issue: no input validation
    return price - (price * discount_percent / 100)


def divide(a, b):
    # Issue: no zero-check, will crash
    return a / b


unused_variable = "this will get flagged as unused"
