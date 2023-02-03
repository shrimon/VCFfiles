#! /usr/bin/env python3
"""import_micro_db.py script for importing microbial growth data into sqlite3 db
"""
import argparse
import csv
import sqlite3

parser = argparse.ArgumentParser(
    description="""Populate empty microbial growth database."""
)
parser.add_argument(
    'micro_db', type=str, nargs='?',
    help="empty sqlite database (it should have the schema from micro_db_schema.sql)",
    default='./data/microdb.sqlite'
)
parser.add_argument(
    'input_csv_path', type=str, nargs='?',
    help="input CSV file",
    default='./data/microbial_growth_data.csv'
)

args = parser.parse_args()

author_ids = dict()
known_organisms = set()
known_experiments = set()

def import_row(db_cursor, row):
    # Splitting author column and stripping whitespace from author names
    author_names = [ author.strip() for author in row['Authors'].split(',') ]
    insert_organism(db_cursor, row['Organism'], row['Is Fungus'])
    insert_authors(db_cursor, author_names)
    insert_experiment(
        db_cursor,
        row['Experiment'],
        author_names,
        row['Organism'],
        row['Medium'],
        row['Temperature']
    )
    insert_datapoint(db_cursor, row['Experiment'], row['Time'], row['CFU'])

def insert_organism(db_cursor, organism, is_fungus):
    if organism not in known_organisms:
        db_cursor.execute(
            f'INSERT INTO organisms VALUES("{organism}", {is_fungus});'
        )
        known_organisms.add(organism)

def insert_authors(db_cursor, author_names):
    for author_name in author_names:
        if author_name not in author_ids:
            db_cursor.execute(
                f'INSERT INTO authors (name) VALUES("{author_name}");'
            )
            author_ids[author_name] = db_cursor.lastrowid

def insert_experiment(db_cursor, exp_id, author_names, organism, medium, temp):
    if exp_id not in known_experiments:
        db_cursor.execute(
            f'INSERT INTO experiments VALUES("{exp_id}", "{organism}", "{medium}", {temp});'
        )
        known_experiments.add(exp_id)
        for author_name in author_names:
            author_id = author_ids[author_name]
            db_cursor.execute(
                f'INSERT INTO experiments_authors VALUES("{exp_id}", {author_id});'
            )

def insert_datapoint(db_cursor, exp_id, time, cfu):
    db_cursor.execute(
        f'INSERT INTO datapoints (experiment_id, time, cfu) VALUES("{exp_id}", {time}, {cfu});'
    )

conn = sqlite3.connect(args.micro_db)

with open(args.input_csv_path, mode='r', encoding='utf-8') as csv_file, \
     sqlite3.connect(args.micro_db) as db_connection:
    csv_reader = csv.DictReader(csv_file)
    cursor = db_connection.cursor()
    for row in csv_reader:
        try:
            import_row(cursor, row)
        except Exception as e:
            print(e)
            exit('Error: Data import failed')
