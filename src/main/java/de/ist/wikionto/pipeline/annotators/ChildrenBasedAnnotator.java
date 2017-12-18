package de.ist.wikionto.research.temp;

import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Queue;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class ChildrenBasedAnnotator extends Annotator {
	private double thresholdInstances = 0.34;
	private double thresholdSemantically = 0.4;
	private double thresholdClassifiers = 0.3;
	private static final String URI = "http://myWikiTax.de/";
	private String query = "/sparql/queries/classifier/getAllUnmarkedClassifiers.sparql";
	private Boolean a = true;
	
	
	private  int iteration = 0;
	private int i = 0;
	
	private Map<String, Optional<Boolean>> currentMap = new HashMap<>();
	private Map<String, String> articlesCheckResults = new HashMap<>();
	private Map<String, String> categoriesCheckResults = new HashMap<>();
	
	//	private Optional<Boolean> current;
	
	public ChildrenBasedAnnotator(WikiOntoPipeline manager, int iteration) {
		super(manager,"ChildrenBased" + "Iteration" + iteration);
		this.iteration = iteration;
		
	}

	@Override
	public void execute() {
		log.logDate("Log Start + Iteration " + iteration + "\nThreshold children: " + thresholdInstances + "\nThreshold subcategories: " + thresholdClassifiers + "\n");
		changed = false;
		List<String> classifiers = QueryUtil.getReachableClassifiers(this.manager.getStore());
		Queue<String> todos = forEachCheckArticles(classifiers);
		forEachCheckCategories(todos);
		logResults(classifiers);
		commitResults();
		log.logDate("Log End");
		log.close();
	}

	

	private void commitResults() {
		currentMap.keySet().stream()
			.forEach(name -> {
				this.commitChangedValue(name, this.currentMap.get(name).get());
			});
		
	}
	
	private boolean commitChangedValue(String name, Boolean result){
		if (this.manager.getBooleanFromRelevantCategories(name) == result) {
			return false;
		} else {
			changed = true;
			this.manager.putInRelevantCategories(name, result);
			return  true;
		}

	}

	private void logResults(List<String> classifiers) {
		classifiers.stream()
			.filter(this.currentMap::containsKey)
			.forEach(name -> {
				log.logLn("Category " + name );
				log.logLn(this.articlesCheckResults.get(name));
				if (this.categoriesCheckResults.containsKey(name))
					log.logLn(this.categoriesCheckResults.get(name));
				log.logLn("  Result: " + this.currentMap.get(name).orElse(false) + "\n");
			});
		
		
	}
	
	private void forEachCheckCategories(Queue<String> classifiers) {
		Queue<String> todos = classifiers;
		while(!todos.isEmpty()) {
			String name = todos.poll();
			Optional<Boolean> result = checkSubcategories(name);
			if (result.isPresent())
				this.currentMap.put(name, result);
			else
				todos.offer(name);
		}
	}

	private Queue<String> forEachCheckArticles(List<String> classifiers) {
		Queue<String> todos = new LinkedList<>();
		classifiers.stream()
			.forEach(name -> {
				Boolean result = checkArticles(name);
				if (result) 
					currentMap.put(name, Optional.of(true));
				else {
					todos.offer(name);
					currentMap.put(name, Optional.empty());
				}
			});
		return todos;
	}

	private Boolean checkArticles(String name) {
		boolean result = false;
		List<String> articles = QueryUtil.getInstances(manager.getSourceStore(), name);
		long articleSize = articles.size();
		long artCount = articles.stream()
				.filter(x -> manager.getOptionalFromRelevantArticles(x).orElse(false)).count();
		if (articles.size() > 0){
			result =  artCount >= (thresholdInstances * articleSize);
		}
		
		this.articlesCheckResults.put(name,"  Articles: " + result + "  " + articles.size() + "  " + artCount);
		return result;
	}

	private Optional<Boolean> checkSubcategories(String name) {
		Boolean result = false;
		List<String> subcategories = QueryUtil.getSubclassifiers(manager.getStore(), name);
		if (subcategories.stream().anyMatch(x -> !currentMap.get(x).isPresent())) {
			return Optional.empty();
		}
		long subCount = subcategories.stream().filter(x -> this.currentMap.get(x).get()).count();
		if (subcategories.size() > 0){
			 result = subCount  >= (thresholdClassifiers * subcategories.size());
		}
		this.categoriesCheckResults.put(name,"  Subcategories: " + result + "  "  + subcategories.size() + "  " + subCount);
		return Optional.of(result);
	}

	public int getIteration() {
		return iteration;
	}
	
}
