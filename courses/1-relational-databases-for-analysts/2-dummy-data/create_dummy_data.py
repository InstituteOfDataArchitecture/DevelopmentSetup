import os
import psycopg2
from psycopg2.extras import execute_values
from faker import Faker
import random
from datetime import datetime, timedelta
import time

NUMBER_OF_CUSTOMERS = 10000
NUMBER_OF_PRODUCTS = 1000
NUMBER_OF_SALES = 10000000
SEED = 40
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime(2024, 1, 1)

total_start_time = time.time()

random.seed(SEED)
Faker.seed(SEED)

locale_to_country = {
    'en_US': 'USA', 'de_DE': 'Germany', 'fr_FR': 'France',
    'es_ES': 'Spain', 'it_IT': 'Italy', 'en_GB': 'United Kingdom',
    'da_DK': 'Denmark', 'en_PH': 'Philippines', 'en_TH': 'Thailand'
}
customer_faker_pool = {locale: Faker(locale) for locale in locale_to_country}
product_faker = Faker()

def generate_timestamp():
    """
    Generate a random timestamp between START_DATE and END_DATE.
    """
    total_seconds = int((END_DATE - START_DATE).total_seconds())
    return START_DATE + timedelta(seconds=random.randint(0, total_seconds))

def create_customer(customer_number):
    """
    Create a customer record.

    Returns a tuple with the following structure:
    (customer_number, first_name, last_name, street_address, city, country, email, date_of_birth, created_at)
    """
    selected_locale = random.choice(list(locale_to_country))
    local_faker = customer_faker_pool[selected_locale]
    return (
        customer_number,
        local_faker.first_name(),
        local_faker.last_name(),
        local_faker.street_address(),
        local_faker.city(),
        locale_to_country[selected_locale],
        local_faker.email(),
        local_faker.date_of_birth().isoformat() if random.random() > 0.6 else None,
        generate_timestamp()
    )

start_time = time.time()
customers = [create_customer(n) for n in range(1, NUMBER_OF_CUSTOMERS + 1)]
print("Customers creation time: {:.2f} seconds".format(time.time() - start_time))

def create_product(product_number):
    """
    Create a product record.

    Returns a tuple with the following structure:
    (product_number, name, category, description, in_stock, rating)
    """
    categories = ['Electronics', 'Clothing', 'Home & Garden', 'Travel', 'Games']
    return (
        product_number,
        product_faker.word().capitalize(),
        random.choice(categories),
        product_faker.sentence(),
        random.choice([True, False]),
        round(random.uniform(1, 5), 1)
    )

start_time = time.time()
products = [create_product(n) for n in range(1, NUMBER_OF_PRODUCTS + 1)]
print("Products creation time: {:.2f} seconds".format(time.time() - start_time))

def create_sales(sales_number):
    """
    Create a sales record.

    Returns a tuple with the following structure:
    (sales_number, customer_number, product_number, quantity, price, total_price, created_at)
    The total_price is calculated as quantity * price.
    """
    price = round(random.uniform(1, 100), 2)
    quantity = random.randint(1, 10)
    total_price = round(quantity * price, 2)
    return (
        sales_number,
        random.randint(1, NUMBER_OF_CUSTOMERS),
        random.randint(1, NUMBER_OF_PRODUCTS),
        quantity,
        price,
        total_price,
        generate_timestamp()
    )

start_time = time.time()
sales = [create_sales(i) for i in range(1, NUMBER_OF_SALES + 1)]
print("Sales creation time: {:.2f} seconds".format(time.time() - start_time))

POSTGRES_URL = os.environ['POSTGRES_URL']
conn = psycopg2.connect(POSTGRES_URL)
cur = conn.cursor()

cur.execute("""
    create temp table temp_customers (
        customer_number int,
        first_name varchar(255),
        last_name varchar(255),
        street_address varchar(255),
        city varchar(255),
        country varchar(255),
        email varchar(255),
        date_of_birth date,
        created_at timestamp
    );

    create temp table temp_products (
        product_number int,
        name varchar(255),
        category varchar(255),
        description text,
        in_stock boolean,
        rating decimal(2, 1)
    );

    create temp table temp_sales (
        sales_number int,
        customer_number int,
        product_number int,
        quantity int,
        price decimal(10, 2),
        total_price decimal(10, 2),
        created_at timestamp
    );
""")

start_time = time.time()
execute_values(cur, "INSERT INTO temp_customers VALUES %s", customers)
print("Customers bulk insert time: {:.2f} seconds".format(time.time() - start_time))

start_time = time.time()
execute_values(cur, "INSERT INTO temp_products VALUES %s", products)
print("Products bulk insert time: {:.2f} seconds".format(time.time() - start_time))

start_time = time.time()
execute_values(cur, "INSERT INTO temp_sales VALUES %s", sales)
print("Sales bulk insert time: {:.2f} seconds".format(time.time() - start_time))


start_time = time.time()
cur.execute("CREATE INDEX idx_product_number ON temp_products (product_number);")
print("Index creation on product_number time: {:.2f} seconds".format(time.time() - start_time))

start_time = time.time()
cur.execute("CREATE INDEX idx_customer_number ON temp_customers (customer_number);")
print("Index creation on customer_number time: {:.2f} seconds".format(time.time() - start_time))


start_time = time.time()
cur.execute("""
    drop table if exists sales;

    create table sales as
    select
        temp_sales.sales_number,
        temp_customers.customer_number,
        temp_customers.first_name as customer_first_name,
        temp_customers.last_name as customer_last_name,
        temp_customers.email as customer_email,
        temp_customers.date_of_birth as customer_date_of_birth,
        temp_customers.created_at as customer_created_at,
        temp_products.product_number,
        temp_products.name as product_name,
        temp_products.category as product_category,
        temp_products.description as product_description,
        temp_products.in_stock as product_in_stock,
        temp_products.rating as product_rating,
        temp_sales.quantity,
        temp_sales.price,
        temp_sales.total_price,
        temp_sales.created_at
    from temp_sales
    left join
        temp_customers
        on temp_sales.customer_number = temp_customers.customer_number
    left join
        temp_products
        on temp_sales.product_number = temp_products.product_number;
""")
print("Permanent sales table creation time: {:.2f} seconds".format(time.time() - start_time))

conn.commit()
cur.close()
conn.close()

print("Total time: {:.2f} seconds".format(time.time() - total_start_time))
