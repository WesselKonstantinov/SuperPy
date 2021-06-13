# Report on technical elements of SuperPy

## Products file structure
Instead of creating two separate csv files for bought and sold products, I decided to go with the "single source of truth" approach and use only one file called 'products.csv' to store information about each bought and sold product.

Once the user has bought a product, SuperPy records information such as its name and buy price and stores it in this file along with a unique id. This id is especially useful, because it allows SuperPy to check if the product has already been sold or not. The following function handles this check:
```python
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
```
If the user decides to sell a product, SuperPy goes through 'products.csv' to find a row that matches the product to be sold by handling a few checks (including the one mentioned above). If there is a matching product, it gets updated with new information like the selling price and date. The final step is to correctly update the whole file in order to reflect the that a product has been sold. This is handled by the following function:
```python
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
```
## Handling expiration dates
Supermarkets are known for buying and selling products that do not have an expiration date. Because of this, I decided to make sure that SuperPy only optionally stores an expiration date for each product. This also becomes relevant when looking for matching products to sell. This function is run in order to ensure a product does not have an expiration date in case the user wants to sell a non-expiring product.
```python
def product_is_non_expiring(product):
    """Check if product is non-expiring (e.g. kitchen utensils)."""
    return not product['expiration_date']
```
However, if the product to be sold has an expiration date, we want to make sure it is still fresh on the current day by running this function:
```python
def product_is_fresh(product):
    """Check if product is not expired."""
    current_date = open('current_date.txt').read()
    return product['expiration_date'] >= current_date
```
## File generation
In order to avoid any FileNotFoundErrors, I created a few functions that are responsible for creating the relevant files if they are not present. For example:
```python
def generate_current_date_file():
    """Create text file that stores and keeps track of current date."""
    filename = 'current_date.txt'
    if not os.path.exists(filename):
        with open(filename, 'w') as text_file:
            text_file.write(date.today().strftime('%Y-%m-%d'))
```
By placing these functions at the beginning of the program, we can make sure that no problems occur by the time the user decides to run a command:
```python
def main():
    generate_current_date_file()
    generate_products_file()
    generate_financial_records_file()

    args = generate_parser()
    args.func(args)


if __name__ == '__main__':
    main()
```