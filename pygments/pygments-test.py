from pygments.formatters import get_all_formatters
from pygments import highlight
from pygments.lexers import ScalaLexer
from pygments.lexers import PythonConsoleLexer
from pygments.formatters import HtmlFormatter


CODE = "// Another way, using auto infer schema\n\n// NOTE: In this case make sure that auto inferred data types are matching the case class\n\nimport java.sql.Date\nimport spark.implicits._\n\ncase class Flight1(id: String, fldate: Date, month: Long, dofW: Long, carrier: String, src: String, dst: String, crsdephour: Long, crsdeptime: Long, depdelay: Double, crsarrtime: Long, arrdelay: Double, crselapsedtime: Double, dist: Double) extends Serializable\n\n\n// val flightDS_autoinfer = spark.read.format(\"json\").load(z.get(\"flight-data-2018\").toString).as[Flight1]\n// same as below\n\nval flightDS_autoinfer = flightDF_autoinfer.as[Flight1]\n"
RESULT = "+--------------------+----------+-----+----+-------+---+---+----------+----------+--------+----------+--------+--------------+-----+\n|                  id|    fldate|month|dofW|carrier|src|dst|crsdephour|crsdeptime|depdelay|crsarrtime|arrdelay|crselapsedtime| dist|\n+--------------------+----------+-----+----+-------+---+---+----------+----------+--------+----------+--------+--------------+-----+\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|         9|       850|     0.0|      1116|     0.0|         146.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        11|      1122|     8.0|      1349|     0.0|         147.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        14|      1356|     9.0|      1623|     0.0|         147.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        16|      1620|     0.0|      1851|     3.0|         151.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        19|      1940|     6.0|      2210|     0.0|         150.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        12|      1248|     0.0|      1513|     0.0|         145.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        22|      2215|     0.0|        39|     0.0|         144.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|BOS|        15|      1500|    21.0|      1734|    33.0|         154.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     WN|ATL|BOS|        15|      1500|   198.0|      1725|   208.0|         145.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     WN|ATL|BOS|        21|      2055|    14.0|      2330|     0.0|         155.0|946.0|\n|ATL_BOS_2018-01-0...|2018-01-01|    1|   1|     WN|ATL|BOS|        10|      1015|   215.0|      1250|   191.0|         155.0|946.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     AA|ATL|CLT|        11|      1114|     0.0|      1238|     0.0|          84.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     AA|ATL|CLT|         8|       845|     0.0|      1011|     0.0|          86.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     AA|ATL|CLT|        15|      1548|     0.0|      1710|     0.0|          82.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     AA|ATL|CLT|         7|       705|     0.0|       821|     0.0|          76.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     AA|ATL|CLT|        12|      1226|     0.0|      1347|     0.0|          81.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     AA|ATL|CLT|        22|      2205|     0.0|      2319|     1.0|          74.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|CLT|        22|      2210|    11.0|      2324|     0.0|          74.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|CLT|        15|      1543|     1.0|      1659|     0.0|          76.0|226.0|\n|ATL_CLT_2018-01-0...|2018-01-01|    1|   1|     DL|ATL|CLT|        10|      1008|     0.0|      1124|     0.0|          76.0|226.0|\n+--------------------+----------+-----+----+-------+---+---+----------+----------+--------+----------+--------+--------------+-----+\nonly showing top 20 rows\n\n"
MARKDOWN = "<h1>Datasets, DataFrames, and Spark SQL</h1>\n"
MARKDOWN1 = "<h3>Common Dataset typed transformations &ldquo;Dataset[T]&rdquo;</h3>\n<ul>\n<li>filter</li>\n<li>map</li>\n<li>groupByKey</li>\n</ul>\n"


def main():
    formatter = HtmlFormatter(full=False, style='monokai')

    html = []
    with open('out.html', 'w') as f:
        html.append('<link rel="stylesheet" type="text/css" href="style.css">')
        html.append(MARKDOWN)
        html.append(highlight(CODE, ScalaLexer(), formatter))
        html.append(highlight(RESULT, PythonConsoleLexer(), formatter))
        html.append(MARKDOWN1)
        f.write("\n\n".join(html))

    with open('style.css', 'w') as f:
        f.write(formatter.get_style_defs('body'))


if __name__ == '__main__':
    main()
