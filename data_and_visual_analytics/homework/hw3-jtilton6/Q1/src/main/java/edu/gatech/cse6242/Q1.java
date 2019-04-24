
/*References: https://www.dezyre.com/hadoop-tutorial/java-for-hadoop-arrays
 https://hadoop.apache.org/docs/current/hadoop-mapreduce-client/hadoop-mapreduce-client-core/MapReduceTutorial.html#Example:_WordCount_v1.0*/

package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import java.util.StringTokenizer;


public class Q1 {
  public static class TokenizerMapper
      extends Mapper<Object, Text, Text, IntWritable>{

   public void map(Object key, Text value, Context context
                   ) throws IOException, InterruptedException {
     String[] tgt=value.toString().split("\t");
     context.write(new Text(tgt[1]), new IntWritable(Integer.parseInt(tgt[2])));
   }
 }
 public static class IntSumReducer
        extends Reducer<Text,IntWritable,Text,IntWritable> {
     private IntWritable result = new IntWritable();

     public void reduce(Text key, Iterable<IntWritable> values,
                        Context context
                        ) throws IOException, InterruptedException {
       int sum = 0;
       for (IntWritable val : values) {
         sum += val.get();
       }
       result.set(sum);
       context.write(key, result);
     }
   }


  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Q1");

    System.out.println("some message");
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
