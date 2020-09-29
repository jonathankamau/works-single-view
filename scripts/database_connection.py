import configparser
import pandas as pd
from sqlalchemy import create_engine, text
from scripts.extract import ExtractWorks

extract = ExtractWorks()

class DatabaseConnection:
    """Create a database connection with postgres."""

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('configs/data.cfg')
        self.db = config['POSTGRES']['DATABASE']
        self.db_username = config['POSTGRES']['USERNAME']
        self.db_password = config['POSTGRES']['PASSWORD'] 
        

    def save_data(self):

        final_df = extract.extract_data()

        pandas_df = final_df.toPandas()

        

        engine = create_engine(
            f'postgresql://{self.db_username}:{self.db_password}@localhost:5432/{self.db}')

        if not engine.dialect.has_table(engine, 'music_works'): 
            engine.execute(
                """
                CREATE TABLE IF NOT EXISTS 
                music_works (
                    iswc varchar NOT NULL UNIQUE, 
                    title varchar, 
                    contributors varchar, 
                    sources varchar)
                """)
            
            pandas_df.to_sql("music_works", engine, index=False, if_exists="append")
        
        engine.execute(
            """CREATE TEMPORARY TABLE 
            temp_music_works (
                iswc varchar NOT NULL UNIQUE, 
                title varchar, 
                contributors varchar, 
                sources varchar)
                """)
        
        pandas_df.to_sql("temp_music_works", engine, index=False, if_exists="append")

        engine.execute("""
                INSERT INTO music_works (
                    iswc, title, contributors, sources) 
                SELECT iswc, title, contributors, sources FROM temp_music_works
                ON CONFLICT DO NOTHING
                """
            )






