"""
This module contains the core functionalities of the SuperPy
commandline tool. These include the following abilities:
- displaying and advancing the current date
- buying and selling products
- displaying the current inventory
- getting information about the sales, revenue and profit for each day
- visualizing financial data
"""

# Imports
import csv
import numpy as np
from collections import Counter
from datetime import datetime, timedelta
from uuid import uuid4
from matplotlib import pyplot as plt
from rich import print as rprint
from rich.table import Table


# Date-related functions
def advance_date(args):
    """Increment the current date by given number of days."""
    current_date = open('current_date.txt').read()
    new_current_date = (datetime.strptime(current_date, '%Y-%m-%d')
                        + timedelta(days=args.days)).strftime('%Y-%m-%d')

    with open('current_date.txt', 'w') as text_file:
        text_file.write(new_current_date)

    rprint('[bold green]OK[/bold green]')
    rprint(f'Current date has been set to: {new_current_date}')


def show_current_date(args):
    """Display the current date that has been set to today."""
    current_date = open('current_date.txt').read()
    if args.verbose:
        rprint(f'Current date is: {current_date}')
    else:
        rprint(f'{current_date}')


# Product-related functions
def buy_product(args):
    """Buy and store product in inventory."""
    buy_date = open('current_date.txt').read()
    product = {
        'id': uuid4(),
        'product_name': args.product_name,
        'buy_price': args.buy_price,
        'buy_date': buy_date,
        'expiration_date': args.expiration_date,
    }

    with open('products.csv', 'a', newline='') as csv_file:
        fieldnames = [
            'id',
            'product_name',
            'buy_date',
            'buy_price',
            'expiration_date',
            'sell_date',
            'sell_price',
        ]
        product_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        product_writer.writerow(product)

    rprint('[bold green]OK[/bold green]')
    print(f'Added {args.product_name} to inventory.')


def product_is_non_expiring(product):
    """Check if product is non-expiring (e.g. kitchen utensils)."""
    return not product['expiration_date']


def product_is_fresh(product):
    """Check if product is not expired."""
    current_date = open('current_date.txt').read()
    return product['expiration_date'] >= current_date


def product_is_in_stock(product):
    """Check if product has not yet been sold."""
    current_date = open('current_date.txt').read()
    with open('products.csv', newline='') as csv_file:
        product_reader = csv.DictReader(csv_file)
        product_id = product['id']
        sold_products_ids = [product['id'] for product in product_reader
                             if product['sell_date']]
    # Make product available for sale from the day it has been bought.
    return product_id not in sold_products_ids and \
        current_date >= product['buy_date']


def update_inventory(all_products):
    """Update inventory after product has been sold."""
    with open('products.csv', 'w', newline='') as csv_file:
        fieldnames = [
            'id',
            'product_name',
            'buy_date',
            'buy_price',
            'expiration_date',
            'sell_date',
            'sell_price',
        ]
        product_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        product_writer.writeheader()
        for product in all_products:
            product_writer.writerow(product)


def sell_product(args):
    """ Sell product from inventory."""
    with open('products.csv', newline='') as csv_file:
        product_reader = csv.DictReader(csv_file)
        all_products = [product for product in product_reader]

        # Non-perishable goods to be sold are filtered based on being
        # non-expiring and perishable goods are filtered based on the
        # fact that they are still fresh on the current day.
        matching_products = [product for product in all_products
                             if product['product_name'] == args.product_name
                             and (product_is_non_expiring(product) or
                                  product_is_fresh(product)) and
                             product_is_in_stock(product)]

    if matching_products:
        sell_date = open('current_date.txt').read()
        matching_product = matching_products.pop()
        matching_product['sell_price'] = args.sell_price
        matching_product['sell_date'] = sell_date

        for product in all_products:
            if product['id'] == matching_product['id']:
                product = matching_product

        update_inventory(all_products)

        rprint('[bold green]OK[/bold green]')
        print(f'Successfully sold {matching_product["product_name"]}.')
    else:
        rprint('[bold red]ERROR[/bold red]')
        print('Product is expired or is not in stock.')


# Function related to current inventory
def display_current_inventory(args):
    """Show products that are in stock (optionally by count)."""
    with open('products.csv', newline='') as csv_file:
        product_reader = csv.DictReader(csv_file)
        products_in_stock = [product for product in product_reader
                             if product_is_in_stock(product)]

    if args.count:
        inventory_table = Table(title='Currently in stock')
        inventory_table.add_column('Product Name', style='steel_blue1')
        inventory_table.add_column('Count', style='yellow')

        if products_in_stock:
            product_counter = Counter()
            for product_in_stock in sorted(products_in_stock,
                                           key=lambda product:
                                           product['product_name']):
                product_counter[product_in_stock['product_name']] += 1

            for product, count in product_counter.items():
                inventory_table.add_row(product.title(), str(count))

            rprint(inventory_table)
        else:
            rprint('[bold red]ERROR[/bold red]')
            print('No products found in stock.')
    else:
        inventory_table = Table(title='Currently in stock')
        inventory_table.add_column('Product Name', style='steel_blue1')
        inventory_table.add_column('Buy Price', style='yellow')
        inventory_table.add_column('Expiration Date', style='dark_sea_green4')

        if products_in_stock:
            for product_in_stock in sorted(products_in_stock,
                                           key=lambda product:
                                           product['product_name']):

                if product_is_non_expiring(product_in_stock):
                    product_in_stock['expiration_date'] = 'Non-expiring'
                if not product_is_fresh(product_in_stock):
                    product_in_stock['expiration_date'] = '[red]Expired[/red]'

                inventory_table.add_row(
                    product_in_stock['product_name'].title(),
                    product_in_stock['buy_price'],
                    product_in_stock['expiration_date'],
                )

            rprint(inventory_table)
        else:
            rprint('[bold red]ERROR[/bold red]')
            print('No products found in stock.')


# Functions related to sales, revenue, costs and profit
def get_costs(date):
    """Calculate and return costs of sold products for a given date."""
    with open('products.csv', newline='') as csv_file:
        costs = 0
        product_reader = csv.DictReader(csv_file)
        sold_products = [product for product in product_reader
                         if product['sell_date']]
        for sold_product in sold_products:
            if sold_product['sell_date'] == date:
                costs += float(sold_product['buy_price'])

        costs = round(costs, 2)

    return costs


def get_revenue(date):
    """Calculate and return revenue for a given date."""
    with open('products.csv', newline='') as csv_file:
        revenue = 0
        product_reader = csv.DictReader(csv_file)
        sold_products = [product for product in product_reader
                         if product['sell_date']]
        for sold_product in sold_products:
            if sold_product['sell_date'] == date:
                revenue += float(sold_product['sell_price'])

        revenue = round(revenue, 2)

    return revenue


def get_profit(date):
    """Calculate and return profit for a given date."""
    revenue = get_revenue(date)
    costs = get_costs(date)
    profit = round(revenue - costs, 2)

    return profit


def get_sold_products(date):
    """Return sold products for a given date."""
    with open('products.csv', newline='') as csv_file:
        product_reader = csv.DictReader(csv_file)
        sold_products = [product for product in product_reader
                         if product['sell_date'] == date]

    return sold_products


def display_sales_data(args):
    """Display sales, revenue, costs or profit based on given day."""
    today = open('current_date.txt').read()
    yesterday = (datetime.strptime(today, '%Y-%m-%d')
                 - timedelta(days=1)).strftime('%Y-%m-%d')

    if args.information == 'revenue':
        if args.today:
            revenue = get_revenue(today)
            if revenue > 0:
                rprint(f"Today's revenue: [green]+{revenue}[/green]")
            else:
                rprint(f"Today's revenue: [orange1]{revenue}[/orange1]")
        elif args.yesterday:
            revenue = get_revenue(yesterday)
            if revenue > 0:
                rprint(f"Yesterday's revenue: [green]+{revenue}[/green]")
            else:
                rprint(f"Yesterday's revenue: [orange1]{revenue}[/orange1]")
        elif args.date:
            revenue = get_revenue(args.date)
            if revenue > 0:
                rprint(f'Revenue for {args.date}: [green]+{revenue}[/green]')
            else:
                rprint(
                    f'Revenue for {args.date}: [orange1]{revenue}[/orange1]')
    elif args.information == 'costs':
        if args.today:
            costs = get_costs(today)
            if costs > 0:
                rprint(f"Today's costs of sold products: [red]+{costs}[/red]")
            else:
                rprint(
                    f"Today's costs of sold products: [orange1]{costs} \
                    [/orange1]")
        elif args.yesterday:
            costs = get_costs(yesterday)
            if costs > 0:
                rprint(
                    f"Yesterday's costs of sold products: [red]+{costs}[/red]")
            else:
                rprint(
                    f"Yesterday's costs of sold products: [orange1]{costs} \
                    [/orange1]")
        elif args.date:
            costs = get_costs(args.date)
            if costs > 0:
                rprint(
                    f"Costs of sold products for {args.date}: [red]+{costs} \
                    [/red]")
            else:
                rprint(
                    f"Costs of sold products for {args.date}: [orange1]{costs} \
                    [/orange1]")
    elif args.information == 'profit':
        if args.today:
            profit = get_profit(today)
            if profit > 0:
                rprint(f"Today's profit: [green]+{profit}[/green]")
            elif profit < 0:
                rprint(f"Today's profit: [red]{profit}[/red]")
            else:
                rprint(f"Today's profit: [orange1]{profit}[/orange1]")
        elif args.yesterday:
            profit = get_profit(yesterday)
            if profit > 0:
                rprint(f"Yesterday's profit: [green]+{profit}[/green]")
            elif profit < 0:
                rprint(f"Yesterday's profit: [red]{profit}[/red]")
            else:
                rprint(f"Yesterday's profit: [orange1]{profit}[/orange1]")
        elif args.date:
            profit = get_profit(args.date)
            if profit > 0:
                rprint(f"Profit for {args.date}: [green]+{profit}[/green]")
            elif profit < 0:
                rprint(f"Profit for {args.date}: [red]{profit}[/red]")
            else:
                rprint(f"Profit for {args.date}: [orange1]{profit}[/orange1]")
    elif args.information == 'sales':
        if args.today:
            sales_table = Table(title="Today's sales")
            sold_products = get_sold_products(today)
        elif args.yesterday:
            sales_table = Table(title="Yesterday's sales")
            sold_products = get_sold_products(yesterday)
        elif args.date:
            sales_table = Table(title=f'Sales for {args.date}')
            sold_products = get_sold_products(args.date)

        sales_table.add_column('Product Name', style='steel_blue1')
        sales_table.add_column('Buy Price', style='yellow')
        sales_table.add_column('Sell Price', style='bright_green')

        if sold_products:
            for sold_product in sorted(sold_products,
                                       key=lambda product:
                                       product['product_name']):
                sales_table.add_row(
                    sold_product['product_name'].title(),
                    sold_product['buy_price'],
                    sold_product['sell_price'],
                )

            rprint(sales_table)
        else:
            rprint('[bold red]ERROR[/bold red]')
            print('No sales data available.')


# Functions related to recording and visualizing financial data
def record_sales_data(args):
    """Record costs, revenue and profit for given date."""
    today = open('current_date.txt').read()
    yesterday = (datetime.strptime(today, '%Y-%m-%d')
                 - timedelta(days=1)).strftime('%Y-%m-%d')

    if args.today:
        costs = get_costs(today)
        revenue = get_revenue(today)
        profit = get_profit(today)
        new_record = {
            'date': today,
            'costs': costs,
            'revenue': revenue,
            'profit': profit,
        }
    elif args.yesterday:
        costs = get_costs(yesterday)
        revenue = get_revenue(yesterday)
        profit = get_profit(yesterday)
        new_record = {
            'date': yesterday,
            'costs': costs,
            'revenue': revenue,
            'profit': profit,
        }
    elif args.date:
        costs = get_costs(args.date)
        revenue = get_revenue(args.date)
        profit = get_profit(args.date)
        new_record = {
            'date': args.date,
            'costs': costs,
            'revenue': revenue,
            'profit': profit,
        }

    with open('financial_records.csv', newline='') as csv_file:
        record_reader = csv.DictReader(csv_file)
        all_records = [record for record in record_reader]
        recorded_dates = [record['date'] for record in all_records]

    # Dates that have not yet been recorded will be newly added to the
    # file, while existing dates will be updated.
    if new_record['date'] in recorded_dates:
        for record in all_records:
            if record['date'] == new_record['date']:
                record = record.update(new_record)
    else:
        all_records.append(new_record)

    with open('financial_records.csv', 'w', newline='') as csv_file:
        fieldnames = ['date', 'costs', 'revenue', 'profit']
        record_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        record_writer.writeheader()
        for record in all_records:
            record_writer.writerow(record)

    if args.today:
        rprint('[bold green]OK[/bold green]')
        print("Successfully recorded today's costs, revenue and profit.")
    elif args.yesterday:
        rprint('[bold green]OK[/bold green]')
        print("Successfully recorded yesterday's costs, revenue and profit.")
    elif args.date:
        rprint('[bold green]OK[/bold green]')
        rprint(
            f"Successfully recorded costs, revenue and profit for {args.date}."
        )


def visualize_financial_records(args):
    """Show recorded data in a line or bar chart."""
    with open('financial_records.csv', newline='') as csv_file:
        record_reader = csv.DictReader(csv_file)
        all_records = [record for record in record_reader]

        # Sort all records by date to make them appear in the correct
        # order in the generated chart
        all_records.sort(key=lambda record: datetime.strptime(
            record['date'], '%Y-%m-%d'
        ))

        # Get MM-DD format for each date
        dates = [record['date'][5:] for record in all_records]
        costs = [float(record['costs']) for record in all_records]
        revenue = [float(record['revenue'])for record in all_records]
        profit = [float(record['profit']) for record in all_records]

    x = np.arange(len(dates))
    width = 0.2

    plt.style.use('seaborn')
    fig, ax = plt.subplots()

    if args.type == 'bar':
        ax.bar(x - width, costs, width, label='Costs', color='cyan')
        ax.bar(x, revenue, width, label='Revenue', color='orange')
        ax.bar(x + width, profit, width, label='Profit', color='green')
    else:
        ax.plot(dates, costs, label='Costs', color='cyan')
        ax.plot(dates, revenue, label='Revenue', color='orange')
        ax.plot(dates, profit, label='Profit', color='green')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_ylabel('Costs, revenue and profit')
    ax.set_title('Financial overview for each day')
    ax.set_xlabel('Days (MM-DD)')
    ax.set_xticks(x)
    ax.set_xticklabels(dates)
    ax.legend()

    fig.tight_layout()
    fig.autofmt_xdate()

    rprint('[bold green]OK[/bold green]')
    print('Successfully created chart.')

    plt.show()
