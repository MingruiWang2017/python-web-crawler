import installation
"""串行执行"""

@installation.timeit
def developer_day(customers):
    for customer in customers:
        installation.install_wordpress(customer)


developer_day(['Bill', 'Elon', 'Steve', 'Mark'])

# 串行执行12s