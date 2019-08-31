# -*- coding: utf-8 -*-
"""pyspark_bank_marketing_project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/151ne9uP3KM8BG_3TwHnBfYgPujX1ZjTs

## Install JDK
## Install Spark
## Set Environment variables
## Create a Spark Session
"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q http://apachemirror.wuchna.com/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
!tar -xvf spark-2.4.3-bin-hadoop2.7.tgz
!pip install -q findspark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.4.3-bin-hadoop2.7"
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

"""## Copy a data file to your local Colab environment"""

!wget https://raw.githubusercontent.com/futurexskill/bigdata/master/bank_prospects.csv

"""## Check if the file is copied"""

!ls

"""# DataFrame

## Read the CSV file into a DataFrame
"""

bankProspectsDF = spark.read.csv("bank_prospects.csv",header=True)

bankProspectsDF.show()

"""## Remove the record with unknow value in country column"""

bankProspectsDF1 = bankProspectsDF.filter(bankProspectsDF['country'] != "unknown")

bankProspectsDF1.show()

"""##  Cast the String datatype to Integer/Float"""

bankProspectsDF1.printSchema()

from pyspark.sql.types import IntegerType,FloatType

bankProspectsDF2 = bankProspectsDF1.withColumn("age", bankProspectsDF1["age"].cast(IntegerType())).withColumn("salary", bankProspectsDF1["salary"].cast(FloatType()))

bankProspectsDF2.printSchema()

"""## Replace Age and Salary with average values of their respective column

import mean from sql.fuctions
"""

from pyspark.sql.functions import mean

"""### Calculate "mean" value of the age"""

mean_age_val = bankProspectsDF2.select(mean(bankProspectsDF2['age'])).collect()

type(mean_age_val)

mean_age_val

mean_age = mean_age_val[0][0]

mean_age

"""### Calculate mean salary value"""

mean_salary_val = bankProspectsDF2.select(mean(bankProspectsDF2['salary'])).collect()

mean_salary = mean_salary_val[0][0]

mean_salary

"""### Replace missing age with average value"""

bankProspectsDF2.show()

bankbankProspectsDF3 = bankProspectsDF2.na.fill(mean_age,["age"])

bankbankProspectsDF3.show()

"""### Replace missing age with salary value"""

bankbankProspectsDF4 = bankbankProspectsDF3.na.fill(mean_salary,["salary"])

bankbankProspectsDF4.show()

bankbankProspectsDF4.printSchema()

"""## Write the transformed file to a new csv file"""

bankbankProspectsDF4.write.format("csv").save("bank_prospects_transformed")

!ls

!ls bank_prospects_transformed/

!cat bank_prospects_transformed/part-00000-e3e9e3b6-be0c-45c2-a8f3-9f4be4663429-c000.csv

