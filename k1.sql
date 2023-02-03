CREATE TABLE GENOMEVCF{
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
};