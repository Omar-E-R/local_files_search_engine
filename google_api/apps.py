from django.apps import AppConfig


class GoogleApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'google_api'

    def ready(self):
        import pandas as pd
        import psycopg2 as pg
        import psycopg2.extras
        import re
        import numpy as np
        from spacy.lang.fr.stop_words import STOP_WORDS as fr_stopwords_list
        import glob
        from os import path

        # Finding all txt files
        txt_files = glob.glob("/home/omar/workspace/M2/hypermedia/google/google_api/text_files/*.txt")

        PG_TABLE = 'google_api_index'

        connection = pg.connect(
            host="localhost",
            database="project_hypermedia",
            user="postgres",
            password="17082015")

        def init_db():
            creat_tables = ("""
            CREATE TABLE IF NOT EXISTS google_api_index (
                id INTEGER PRIMARY KEY,
                words varchar(25) NOT NULL,
                occurrences integer NOT NULL,
                documents varchar(50) NOT NULL
            );
            CREATE TABLE IF NOT EXISTS saved (
                documents varchar(50) NOT NULL
            );
            """)

            cursor = connection.cursor()
            cursor.execute(creat_tables)
            cursor.close()

        def save_to_db(df: pd.DataFrame, file: str):
            save_document_query = ("""
            INSERT INTO saved(documents)
                VALUES (%s);
            """)

            if len(df) > 0:
                df_columns = ["words", "occurrences", "documents"]
                columns = 'words,occurrences,documents'

                # create VALUES('%s', '%s',...) one '%s' per column
                values = "VALUES({})".format(",".join(["%s" for _ in df_columns]))

                # create INSERT INTO table (columns) VALUES('%s',...)
                insert_stmt = "INSERT INTO {} ({}) {}".format(PG_TABLE, columns, values)

                cursor = connection.cursor()
                cursor.execute(save_document_query, (file,))
                pg.extras.execute_batch(cursor, insert_stmt, df.values)
                connection.commit()
                cursor.close()

        def check_doc(file: str):
            query = ("""
            select * from saved where documents = %s
            """)
            cursor = connection.cursor()
            cursor.execute(query, (file,))
            result = cursor.rowcount
            cursor.close()
            return result

        def tokenize_files(files: list):
            for file in files:
                head, file = path.split(file)
                if check_doc(file) == 0:
                    df = pd.DataFrame(columns=["words"])

                    # Read Txt file by putting each line on new row
                    df["words"] = pd.read_csv(''.join([head, '/', file]), sep='\n', header=None)

                    # Split lines of text into list of words at every non alpha character
                    df["words"] = df["words"].apply(lambda x: re.split("[^A-Za-zÀ-ȕ]+", x))

                    # Transform each row of list of words into rows of words
                    df = df.explode('words').reset_index(drop=True)

                    # lower case rows
                    df["words"] = df["words"].str.lower()

                    # Drop Nan rows
                    df.dropna(inplace=True)

                    # Create a stop word list comparison
                    pattern = r'\b(?:{})\b'.format('|'.join(fr_stopwords_list))

                    # Filter out words from stop_list
                    df["words"] = df["words"].str.replace(pattern, '', regex=True)

                    # Remove words smaller than 2 letters
                    df["words"] = df["words"].apply(lambda x: re.sub('^[a-zÀ-ȕ]{1,2}$', '', x))

                    df["words"] = df["words"].replace(r'^\s*$', np.nan, regex=True)

                    df.dropna(inplace=True)

                    # Add occurrences column to df
                    df = df["words"].value_counts().reset_index()

                    df.columns = ["words", "occurrences"]

                    df.reset_index(drop=True, inplace=True)

                    # Add document name to df
                    df['documents'] = file

                    save_to_db(df, file)
                else:
                    print(file, 'is already indexed')

        init_db()
        tokenize_files(txt_files)
