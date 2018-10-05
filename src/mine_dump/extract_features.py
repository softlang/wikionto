import mwparserfromhell
from nltk import sent_tokenize, word_tokenize, pos_tag
import re
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StructField, StringType
from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from data import DATAP
from os.path import join
import time
from mine_dump.articles_tocsv import hms_string


def extract_urlpattern(title):
    tag = ''
    rest = title
    if '(' in title:
        tag = title.split('(')[1].split(')')[0]
        rest = title.split('(')[0]
    words = rest.lower()
    words = re.sub(r'[^\w]', ' ', words)
    words = [w.strip() for w in words.split('_')]
    if tag:
        words += [tag]
    return ', '.join(words)


def extract_nouns(text):
    wikicode = mwparserfromhell.parse(text)
    sections = wikicode.get_sections()
    if sections:
        summary = sections[0].strip_code()
        sents = sent_tokenize(summary, language='english')
        if sents:
            words = word_tokenize(sents[0].replace('\\n', ' '))
            return ', '.join([w.strip() for w,tag in pos_tag(words) if 'NN' in tag])
    return ''


def extract_hypernyms(text):
    return []


def extract_infobox_names(text):
    wikicode = mwparserfromhell.parse(text)
    templates = wikicode.filter_templates(recursive=False)
    templates = list(filter(lambda t: 'infobox' in str(t).lower(), templates))
    result = []
    if templates:
        result = [t.name.lower().strip() for t in templates]
    return ', '.join(result)


def extract_seedrecognition(title):
    return 0


if __name__ == "__main__":
    start_time = time.time()
    schema = StructType([
        StructField("title", StringType()),
        StructField("text", StringType())
    ])

    con = SparkConf()\
        .setAppName("Main").setMaster("local["+str(4)+"]")\
        .set("spark.local.dir", join("","pyspark"))\
        .set("spark.driver.memory", "12g")\
        .set("spark.executor.memory", "12g") \
        .set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")\
        .set("spark.kryoserializer.buffer.max", "1280m")\
        .set("spark.driver.maxResultSize","12g")
    sc = SparkContext(conf=con)
    sql_sc = SQLContext(sc)

    url_ex = udf(extract_urlpattern, StringType())
    inf_ex = udf(extract_infobox_names, StringType())
    noun_ex = udf(extract_nouns, StringType())

    df = sql_sc.read \
        .format("com.databricks.spark.csv")\
        .schema(schema)\
        .option("header", "false")\
        .option("quotechar",'"')\
        .option("delimiter",',')\
        .load(DATAP+'/dump/articles.csv.bz2')
    df = df.withColumn("urlwords", url_ex(df.title))
    df = df.withColumn("infoboxnames", inf_ex(df['text']))
    df = df.withColumn("nouns", noun_ex(df['text']))
    df['title', 'urlwords', 'infoboxnames', 'nouns'].write.csv(DATAP + '/dump/articles_annotated.csv')
    #print(df.columns)

    elapsed_time = time.time() - start_time
    print("Elapsed time: {}".format(hms_string(elapsed_time)))

