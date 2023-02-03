import sqlite3

# Connect to database (creates database if not exists)
conn = sqlite3.connect('GENOMEVCF.db')

# Create a cursor
cursor = conn.cursor()
# Execute an SQL statement
cursor.execute("""CREATE TABLE IF NOT EXISTS vcf_data (
    #DEFINE 'FILTER',b
    CHROM INT,
    POS INT,
    ID VARCHAR(255),
    REF VARCHAR(255),
    ALT VARCHAR(255),
    QUAL INT,
    INFO VARCHAR(255),
    b VARCHAR(255),
    /*{
    #DEFINE '=',a;
    #DEFINE FLOAT b;
    DP VARCHAR(255),
    }
    DP VARCHAR(255),
    {
     a VARCHAR(255),
     {
      b INT,
     }
    }*/
    FORMAT VARCHAR(255),
                    )""")
# Commit the transaction
conn.commit()

# Close the connection
conn.close()