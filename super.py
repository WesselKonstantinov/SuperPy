# Imports
import argparse
import csv
import os
import superpy as sp
from datetime import date, datetime

# Do not change these lines.
__winc_id__ = 'a2bc36ea784242e4989deb157d527ba0'
__human_name__ = 'superpy'


# Your code below this line.
def generate_current_date_file():
    """Create text file that stores and keeps track of current date."""
    filename = 'current_date.txt'
    if not os.path.exists(filename):
        with open(filename, 'w') as text_file:
            text_file.write(date.today().strftime('%Y-%m-%d'))


def generate_products_file():
    """Create csv file that stores information about each product."""
    filename = 'products.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csv_file:
            fieldnames = [
                'id',
                'product_name',
                'buy_date',
                'buy_price',
                'expiration_date',
                'sell_date',
                'sell_price'
            ]
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()


def generate_financial_records_file():
    """Create csv file that records financial information for each day."""
    filename = 'financial_records.csv'
    if not os.path.exists(filename):
        with open(filename, 'w', newline='') as csv_file:
            fieldnames = ['date', 'costs', 'revenue', 'profit']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()


def generate_parser():
    """Generate parser along with subparsers and arguments."""
    parser = argparse.ArgumentParser(
        description='SuperPy inventory tracking tool'
    )
    subparsers = parser.add_subparsers()

    advance_date_parser = subparsers.add_parser(
        'advance-date',
        help='advance date by given day of numbers'
    )
    advance_date_parser.add_argument(
        'days',
        help='number of days to advance date by',
        type=int
    )
    advance_date_parser.set_defaults(func=sp.advance_date)

    show_date_parser = subparsers.add_parser(
        'show-date',
        help='display current date'
    )
    show_date_parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='increase output verbosity for current date'
    )
    show_date_parser.set_defaults(func=sp.show_current_date)

    buy_parser = subparsers.add_parser(
        'buy',
        help='buy and place product in stock'
    )
    buy_group = buy_parser.add_argument_group('required named arguments')
    buy_group.add_argument(
        '-pn',
        '--product-name',
        help='name of product to be bought',
        metavar='',
        required=True,
        type=str
    )
    buy_group.add_argument(
        '-p',
        '--price',
        dest='buy_price',
        help='buy price of product',
        metavar='',
        required=True,
        type=float
    )
    buy_parser.add_argument(
        '-ed',
        '--expiration-date',
        help='expiration date of product in YYYY-MM-DD format',
        metavar='',
        # Check specifically for YYYY-MM-DD format
        type=lambda date: datetime.strptime(date, '%Y-%m-%d').date()
    )
    buy_parser.set_defaults(func=sp.buy_product)

    sell_parser = subparsers.add_parser('sell', help='sell product')
    sell_group = sell_parser.add_argument_group('required named arguments')
    sell_group.add_argument(
        '-pn',
        '--product-name',
        help='name of product to be sold',
        metavar='',
        required=True,
        type=str
    )
    sell_group.add_argument(
        '-p',
        '--price',
        dest='sell_price',
        help='sell price of product',
        type=float,
        metavar='',
        required=True
    )
    sell_parser.set_defaults(func=sp.sell_product)

    inventory_parser = subparsers.add_parser(
        'inventory',
        help='display each product that is currently in stock'
    )
    inventory_parser.add_argument(
        '-c',
        '--count',
        help='display the count of each product currently in stock',
        action='store_true'
    )
    inventory_parser.set_defaults(func=sp.display_current_inventory)

    report_parser = subparsers.add_parser(
        'report',
        help='display information about sales, revenue, costs or profit'
    )
    report_parser.add_argument(
        'information',
        choices=['sales', 'revenue', 'costs', 'profit'],
        help='information about sales, revenue, costs or profit',
        type=str
    )
    report_group = report_parser.add_argument_group('required day arguments')
    report_mutually_exclusive_group = \
        report_group.add_mutually_exclusive_group(required=True)
    report_mutually_exclusive_group.add_argument(
        '-td',
        '--today',
        action='store_true',
        help='sales, revenue, costs or profit for today'
    )
    report_mutually_exclusive_group.add_argument(
        '-yd',
        '--yesterday',
        action='store_true',
        help='sales, revenue, costs or profit for yesterday'
    )
    report_mutually_exclusive_group.add_argument(
        '-d',
        '--date',
        help='sales, revenue, costs or profit for given date in YYYY-MM-DD \
        format',
        metavar='',
        type=lambda date:
        datetime.strptime(date, '%Y-%m-%d').date().strftime('%Y-%m-%d')
    )
    report_parser.set_defaults(func=sp.display_sales_data)

    record_parser = subparsers.add_parser(
        'record',
        help='record costs, revenue and profit for a specified day'
    )
    record_group = record_parser.add_argument_group('required day arguments')
    record_mutually_exclusive_group = \
        record_group.add_mutually_exclusive_group(required=True)
    record_mutually_exclusive_group.add_argument(
        '-td',
        '--today',
        action='store_true',
        help='costs, revenue and profit for today'
    )
    record_mutually_exclusive_group.add_argument(
        '-yd',
        '--yesterday',
        action='store_true',
        help='costs, revenue and profit for yesterday'
    )
    record_mutually_exclusive_group.add_argument(
        '-d',
        '--date',
        help='costs, revenue and profit for given date in YYYY-MM-DD format',
        metavar='',
        type=lambda date:
        datetime.strptime(date, '%Y-%m-%d').date().strftime('%Y-%m-%d')
    )
    record_parser.set_defaults(func=sp.record_sales_data)

    visualize_parser = subparsers.add_parser(
        'visualize',
        help='show financial data for each recorded date in a chart'
    )
    visualize_group = visualize_parser.add_argument_group(
        'required named arguments'
    )
    visualize_group.add_argument(
        '-t',
        '--type',
        choices=['bar', 'line'],
        help='plot data as either a line or a bar chart',
        metavar='',
        required=True,
        type=str
    )
    visualize_parser.set_defaults(func=sp.visualize_financial_records)

    return parser.parse_args()


def main():
    generate_current_date_file()
    generate_products_file()
    generate_financial_records_file()

    args = generate_parser()
    args.func(args)


if __name__ == '__main__':
    main()
