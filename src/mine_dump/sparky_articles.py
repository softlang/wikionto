import pyspark

"""
explorative stuff
df = sc.read.format("com.databricks.spark.xml").option("rowTag", "instance") \
        .option("valueTag", "some_value").load("data.xml")

df.withColumn('values', explode('key')).select(
       col('_name').alias('name'),
       col('_number').alias('number'),
       col('values._value').alias('value')
    ).show()
"""