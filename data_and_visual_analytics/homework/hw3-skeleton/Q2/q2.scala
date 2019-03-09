// Databricks notebook source
// MAGIC %md
// MAGIC #### Q2 - Skeleton Scala Notebook
// MAGIC This template Scala Notebook is provided to provide a basic setup for reading in / writing out the graph file and help you get started with Scala.  Clicking 'Run All' above will execute all commands in the notebook and output a file 'examplegraph.csv'.  See assignment instructions on how to to retrieve this file. You may modify the notebook below the 'Cmd2' block as necessary.
// MAGIC 
// MAGIC #### Precedence of Instruction
// MAGIC The examples provided herein are intended to be more didactic in nature to get you up to speed w/ Scala.  However, should the HW assignment instructions diverge from the content in this notebook, by incident of revision or otherwise, the HW assignment instructions shall always take precedence.  Do not rely solely on the instructions within this notebook as the final authority of the requisite deliverables prior to submitting this assignment.  Usage of this notebook implicitly guarantees that you understand the risks of using this template code. 

// COMMAND ----------

/*
DO NOT MODIFY THIS BLOCK
This assignment can be completely accomplished with the following includes and case class.
Do not modify the %language prefixes, only use Scala code within this notebook.  The auto-grader will check for instances of <%some-other-lang>, e.g., %python
*/
import org.apache.spark.sql.functions.desc
import org.apache.spark.sql.functions._
case class edges(Source: String, Target: String, Weight: Int)
import spark.implicits._

// COMMAND ----------

/* 
Create an RDD of graph objects from our toygraph.csv file, convert it to a Dataframe
Replace the 'examplegraph.csv' below with the name of Q2 graph file.
*/

val df = spark.read.textFile("/FileStore/tables/examplegraph.csv") 
  .map(_.split(","))
  .map(columns => edges(columns(0), columns(1), columns(2).toInt)).toDF()

// COMMAND ----------

// Insert blocks as needed to further process your graph, the division and number of code blocks is at your discretion.
var new_df = df.distinct().filter($"Weight" >=5 )


new_df.show()



// COMMAND ----------

var out_deg = new_df.groupBy($"Source").sum().orderBy($"Source").withColumnRenamed("sum(Weight)","weighted-out-degree")
var in_deg =  new_df.groupBy($"Target").sum().orderBy($"Target").withColumnRenamed("sum(Weight)","weighted-in-degree")


in_deg.show()

// COMMAND ----------

var tot_deg =  out_deg.as("out_deg").join(in_deg.as("in_deg"), out_deg("Source") === in_deg("Target")).select("out_deg.Source","out_deg.weighted-out-degree","in_deg.weighted-in-degree").withColumnRenamed("Source","node")
var total_degree = tot_deg.withColumn("weighted-total-degree", tot_deg("weighted-in-degree") + tot_deg("weighted-out-degree"))
total_degree.show()

// COMMAND ----------

// find node with highest weighted-in-degree, if two or more nodes have the same weighted-in-degree, report the one with the lowest node id
var weight_in = total_degree.filter($"weighted-in-degree" === total_degree.agg(max("weighted-in-degree")).head().get(0)).orderBy("node").first()
var v0 = weight_in.get(0).toString.toInt
var d0 = weight_in.get(1).toString.toInt
var c0 = 'i'.toString

// find node with highest weighted-out-degree, if two or more nodes have the same weighted-out-degree, report the one with the lowest node id
var weight_out = total_degree.filter($"weighted-out-degree" === total_degree.agg(max("weighted-out-degree")).head().get(0)).orderBy("node").first()
var v1 = weight_out.get(0).toString.toInt
var d1 = weight_out.get(2).toString.toInt
var c1 = 'o'.toString

// find node with highest weighted-total degree, if two or more nodes have the same weighted-total-degree, report the one with the lowest node id
var weight_total= total_degree.filter($"weighted-total-degree" === total_degree.agg(max("weighted-total-degree")).head().get(0)).orderBy("node").first()
var v2 = weight_total.get(0).toString.toInt
var d2 = weight_total.get(3).toString.toInt
var c2 = 't'.toString



// COMMAND ----------

var result = Seq(
  (v0, d0, c0),
  (v1, d1, c1),
  (v2, d2, c2)
).toDF("v", "d", "c")

result.show()


/*
Create a dataframe to store your results
Schema: 3 columns, named: 'v', 'd', 'c' where:
'v' : vertex id
'd' : degree calculation (an integer value.  one row with highest weighted-in-degree, a row w/ highest weighted-out-degree, a row w/ highest weighted-total-degree )
'c' : category of degree, containing one of three string values:
                                                'i' : weighted-in-degree
                                                'o' : weighted-out-degree                                                
                                                't' : weighted-total-degree
- Your output should contain exactly three rows.  
- Your output should contain exactly the column order specified.
- The order of rows does not matter.
                                                
A correct output would be:

v,d,c
4,15,i
2,20,o
2,30,t

whereas:
- Node 2 has highest weighted-out-degree with a value of 20
- Node 4 has highest weighted-in-degree with a value of 15
- Node 2 has highest weighted-total-degree with a value of 30

*/

// COMMAND ----------

display(result)
