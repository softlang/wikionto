package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.List;

public class PipelineFactory {
	
	//TODO Write Else branches with errors. 
	
	private static List<String> executed = new ArrayList<>();
	private static List<String> todo = new ArrayList<>();
	
	public static void seed(WikiOntoPipeline pipeline){
		SeedAnnotator anno = new SeedAnnotator(pipeline);
		anno.execute();
		PipelineFactory.executed.add("seed");
	}
	
	public static void hypernym(WikiOntoPipeline pipeline){
		HypernymAnnotator anno = new HypernymAnnotator(pipeline);
		anno.execute();
		PipelineFactory.executed.add("hypernym");
	}
	
	public static void eponymous(WikiOntoPipeline pipeline){
		if (executed.contains("hypernym")){
			EponymousTransformation trans = new EponymousTransformation(pipeline);
			trans.execute();
			PipelineFactory.executed.add("eponymous");
		}
	}
	
	public static void semantic(WikiOntoPipeline pipeline, int iteration){
		if (executed.contains("hypernym")) {
			SemanticallyDistanstAnnotator anno = new SemanticallyDistanstAnnotator(pipeline, iteration);
			anno.execute();
			PipelineFactory.executed.add("semantic");

		}
	}
	
	public static void children(WikiOntoPipeline pipeline, int iteration){
		if (executed.contains("hypernym")) {
			ChildrenBasedAnnotator anno = new ChildrenBasedAnnotator(pipeline, iteration);
			anno.execute();
			PipelineFactory.executed.add("children");
		}
	}
	
	public static void insertArticles(WikiOntoPipeline pipeline, int iteration){
		if (executed.contains("hypernym")) {
			InsertRelevantArticlesTransformation anno = new InsertRelevantArticlesTransformation(pipeline);
			anno.execute();
			PipelineFactory.executed.add("articles");
	
		}
	}
	
	public static void insertCategories(WikiOntoPipeline pipeline, int iteration){
		if (executed.contains("children")) {
			InsertRelevantCategoriesTransformation anno = new InsertRelevantCategoriesTransformation(pipeline);
			anno.execute();
			PipelineFactory.executed.add("categories");
		}
	}
	
	public static void cleanUp(WikiOntoPipeline pipeline){
		if (executed.contains("children")) {
			CleanUp anno = new CleanUp(pipeline);
			anno.execute();
			PipelineFactory.executed.add("clean");
		}
	}
	
}
