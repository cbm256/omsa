package edu.gatech.cse6242;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import java.io.IOException;
import org.apache.hadoop.mapred.JobConf;



public class Q4 {
  public static class TokenizerMapper
      extends Mapper<Object, Text, Text, IntWritable>{

   private final static IntWritable one = new IntWritable(1);
   private final static IntWritable neg_one = new IntWritable(-1);
   public void map(Object key, Text value, Context context
                   ) throws IOException, InterruptedException {
     String[] tgt=value.toString().split("\t");
     context.write(new Text(tgt[0]), one);
     context.write(new Text(tgt[1]), neg_one);
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

    public static class TokenizerMapper_
        extends Mapper<Object, Text, Text, IntWritable>{

     private final static IntWritable one = new IntWritable(1);
     public void map(Object key, Text value, Context context
                     ) throws IOException, InterruptedException {
       String[] tgt=value.toString().split("\t");
       context.write(new Text(tgt[1]), one);

     }
    }

  public static void main(String[] args) throws Exception {
    Configuration conf1 = new Configuration();
    Job job = Job.getInstance(conf1);

    /* TODO: Needs to be implemented */
    job.setJarByClass(Q4.class);
    job.setMapperClass(TokenizerMapper.class);
    job.setCombinerClass(IntSumReducer.class);
    job.setReducerClass(IntSumReducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    Path outputPath=new Path("FirstMapper");
    FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job,outputPath);
        outputPath.getFileSystem(conf1).delete(outputPath);
    job.waitForCompletion(true);

      Configuration conf2=new Configuration();
      Job j2=Job.getInstance(conf2);
      j2.setJarByClass(Q4.class);
      j2.setMapperClass(TokenizerMapper_.class);
      j2.setCombinerClass(IntSumReducer.class);
      j2.setReducerClass(IntSumReducer.class);
      j2.setOutputKeyClass(Text.class);
      j2.setOutputValueClass(IntWritable.class);
      Path outputPath1=new Path(args[1]);
      FileInputFormat.addInputPath(j2, outputPath);
      FileOutputFormat.setOutputPath(j2, outputPath1);
      outputPath1.getFileSystem(conf2).delete(outputPath1, true);
      j2.waitForCompletion(true);
      Configuration conf3=new Configuration();
      Job j3=Job.getInstance(conf3);
      Path deletePath=new Path("FirstMapper");
      deletePath.getFileSystem(conf3).delete(deletePath, true);
      System.exit(j3.waitForCompletion(true)?0:1);



  }
}
