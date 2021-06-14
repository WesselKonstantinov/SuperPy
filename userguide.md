# SuperPy inventory tracking tool
## What is SuperPy?
SuperPy is a commandline tool, which supermarkets can use to keep track of their inventory. It supports the following functionalities:
- Displaying and advancing the current date
- Buying and selling products
- Storing information about these products (e.g. buy price and expiration date)
- Providing an overview of the current inventory
- Displaying sales, costs, revenue or profit for today, yesterday or any given date
- Recording costs, revenue and profit for today, yesterday or any given date
- Visualizing financial data
## Third-party modules
SuperPy relies on built-in modules in the Python standard library along with a few third-party modules for its core functionality. The required third-party modules are:
- Matplotlib (3.4.2)
- Numpy (1.20.3)
- Rich (10.2.2)
## Commands
### show-date
#### Function
Reads 'current_date.txt' and prints the current date that has been stored in it.
#### Example of usage
Use the following command to display the current date:
```zsh
python3 super.py show-date
```
This will output:
```zsh
2021-06-14
```
Optionally, you can use the command with the `--verbose` or `-v` flag for a longer output:
```
Current date is: 2021-06-14
```
### advance-date
#### Function
Sets the date by advancing it by a given number of days and updates 'current_date.txt'.
#### Example of usage
Let's say we need to set the current date to 2021-06-16. To do this, you use the following command:
```
python3 super.py advance-date 2
```
This will output:
```
OK
Current date has been set to: 2021-06-16
```
### buy
#### Function
Buys a product and stores its information supplied by the user in 'products.csv'. The product is then available for sale.
#### Example of usage
In order to buy a product, you need to provide its name, the price it is bought for and optionally an expiration date. Suppose we need to buy and store cheese, peanut butter and a sandwich bag. For this, we need `--product-name/-pn`, `--price/-p` and `--expiration-date/-ed`:
```
python3 super.py buy --product-name cheese --price 3.5 --expiration-date 2021-06-20
```
This will output:
```
OK
Added cheese to inventory.
```
For products with a name that consists of more than one word, you want to use quotes to make the command work:
```
python3 super.py buy --product-name 'peanut butter' --price 2.55 --expiration-date 2021-08-15
```
Again, this will output:
```
OK
Added peanut butter to inventory.
```
Finally, buying non-expiring products works as shown below:
```
python3 super.py buy --product-name 'sandwich bag' --price 1.5
```
Output:
```
OK
Added sandwich bag to inventory.
```
### inventory
#### Function
Displays each product that is currently in stock in a table. It can either show the information for each product (e.g. expiration date and buy price) or just the quantity.
#### Example of usage
Getting an overview of the current stock is quite straightforward. You just need to run the following command:
```
python3 super.py inventory
```
This will print a table with each product:
```
             Currently in stock               
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Product Name  ┃ Buy Price ┃ Expiration Date ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Cheese        │ 3.5       │ 2021-06-20      │
│ Peanut Butter │ 2.55      │ 2021-08-15      │
│ Sandwich Bag  │ 1.5       │ Non-expiring    │
└───────────────┴───────────┴─────────────────┘
```
This table will also indicate whether a product has already expired:
```
              Currently in stock               
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Product Name  ┃ Buy Price ┃ Expiration Date ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Bread         │ 1.0       │ Expired         │
│ Cheese        │ 3.5       │ 2021-06-20      │
│ Peanut Butter │ 2.55      │ 2021-08-15      │
│ Sandwich Bag  │ 1.5       │ Non-expiring    │
└───────────────┴───────────┴─────────────────┘
```

You can also add the `--count/-c` flag in order to print a table, which displays the number of each product: 
```
   Currently in stock    
┏━━━━━━━━━━━━━━━┳━━━━━━━┓
┃ Product Name  ┃ Count ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━┩
│ Bread         │ 1     │
│ Cheese        │ 1     │
│ Peanut Butter │ 1     │
│ Sandwich Bag  │ 1     │
└───────────────┴───────┘
```
### sell
#### Function
Sells a product and updates 'products.csv' to correctly record its selling price and date.
#### Example of usage
To sell a product, you need to supply its name (`--product-name/-pn`) and the price you would like to sell it for (`--price/-p`). Let's sell the cheese we have in our inventory:
```
python3 super.py sell --product-name cheese --price 5
```
This will then output:
```
OK
Successfully sold cheese.
```
Running the inventory command shows that we no longer have cheese in our inventory:
```
              Currently in stock               
┏━━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Product Name  ┃ Buy Price ┃ Expiration Date ┃
┡━━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ Bread         │ 1.0       │ Expired         │
│ Peanut Butter │ 2.55      │ 2021-08-15      │
│ Sandwich Bag  │ 1.5       │ Non-expiring    │
└───────────────┴───────────┴─────────────────┘
```
What happens if we decide to sell an expired product? Let's find out:
```
python3 super.py sell --product-name bread --price 3.5
```
This will output:
```
ERROR
Product is expired or is not in stock.
```
This error will appear in case the product to be sold has already expired. It will also show up if you try to sell a product that is not in your inventory.
### report
#### Function
Provides the user with information about sales, costs, revenue or profit for today, yesterday or any given date.
#### Example of usage
#### sales
If you need to get information about today's sales so far, you just need to run:
```
python3 super.py report sales --today
```
This will display a table containing information about each sold product on the relevant day:
```
              Today's sales              
┏━━━━━━━━━━━━━━┳━━━━━━━━━━━┳━━━━━━━━━━━━┓
┃ Product Name ┃ Buy Price ┃ Sell Price ┃
┡━━━━━━━━━━━━━━╇━━━━━━━━━━━╇━━━━━━━━━━━━┩
│ Cheese       │ 3.5       │ 5.0        │
└──────────────┴───────────┴────────────┘
```
If there is no sales data available for a specified date, the program will output an error:
```
ERROR
No sales data available.
```
#### costs
In order to find out today's costs, you just need to run:
```
python3 super.py report costs --today
```
This results in the following output:
```
Today's costs of sold products: +3.5
```
In case data about costs for a specified date is not present, the output will just default to 0:
```
python3 super.py report costs --date 2021-06-10
```
```
Costs of sold products for 2021-06-10: 0
```
The same applies to revenue and profit.
#### revenue
If you want to find out what yesterday's revenue was, just replace `--today/-td` with `--yesterday/-yd`:
```
python3 super.py report revenue --yesterday
```
This will then output:
```
Yesterday's revenue: +18.0
```
#### profit
Suppose we have set today's date to 2021-06-16 and we want to know how much profit we made on 2021-06-13. This works as shown below:
```
python3 super.py report profit --date 2021-06-13
```
This results in:
```
Profit for 2021-06-13: +8.0
```
### record 
#### Function
Saves financial data like costs, revenue and profit for today, yesterday or any given date in 'financial_records.csv'.
#### Example of usage
Just like the report command, `record` also works with either `--today/-td`, `--yesterday/-yd` or `--date/-d`. So, if you want to record today's costs, revenue and profit, just run:
```
python3 super.py record --today
```
This will then show the output as follows:
```
OK
Successfully recorded today's costs, revenue and profit.
```
Recording the same date more than once is also possible. In this case, the program will just update 'financial_records.csv' and provide it with the most recent costs, revenue and profit associated with the relevant date.
### visualize
#### Function
Reads the recorded data in 'financial_records.csv' and plots this in either a line or bar chart.
#### Example of usage
If you would like to display the recorded financial data in a chart, you only need to run one of the two following commands:
```
python3 super.py visualize -type line
```
```
python3 super.py visualize -type bar
```
This outputs:
```
OK
Successfully created chart.
```
The line chart is displayed like this:
![line-chart](https://user-images.githubusercontent.com/69632494/121910051-cdcebd80-cd2e-11eb-9056-c2245ed36ec3.png)
And the bar chart like this:
![bar-chart](https://user-images.githubusercontent.com/69632494/121910508-31f18180-cd2f-11eb-8399-1a20968a53ae.png)