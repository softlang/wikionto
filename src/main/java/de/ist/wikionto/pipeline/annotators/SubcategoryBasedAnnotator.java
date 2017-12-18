package de.ist.wikionto.pipeline.annotators;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
import java.util.stream.Collectors;

import org.apache.xml.utils.SuballocatedByteVector;

import de.ist.wikionto.pipeline.Threshold;
import de.ist.wikionto.pipeline.WikiOntoPipeline;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class SubcategoryBasedAnnotator extends AbstractAnnotator {
	private double thresholdClassifiers = Threshold.CHILDREN_CATEGORIES.getThreshold(); //0.3;
	private Boolean current = false;
		
	private  int iteration = 0;
	
	private Map<String, Boolean> currentMap = new HashMap<>();
	private Map<String, String> articlesCheckResults = new HashMap<>();
	private Map<String, String> categoriesCheckResults = new HashMap<>();
	
	public SubcategoryBasedAnnotator(WikiOntoPipeline manager, int iteration) {
		super(manager,"SubCategoryBased" + "Iteration" + iteration);
		this.iteration = iteration;
		
	}

	@Override
	public void execute() {
		log.logDate("Log Start + Iteration " + iteration + "\nThreshold subcategories: " + thresholdClassifiers + "\n");
		changed = false;
		List<String> classifiers = QueryUtil.getReachableClassifiers(this.manager.getStore()).stream()
				.filter(name -> !this.manager.getBooleanFromRelevantCategories(name))
				.collect(Collectors.toList());
		int i = 1;
		
		do {
			this.current = false;
			classifiers = forEachCategory(classifiers, i);
			i++;
		} while (this.current);
		
		log.logDate("Log End");
		log.close();
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

	/**
	 * Check subcategories
	 * @param classifiers
	 * @param iteration
	 * @return new list of categories for possible next iteration
	 */
	private List<String> forEachCategory(List<String> classifiers, int iteration){
		List<String> nextClassifiers = new ArrayList<String>();
		this.log.logLn("Iteration " + iteration + ":" );
		classifiers.forEach(name -> {
			boolean result = this.checkSubcategories(name);
//			this.log.logLn("  Category " + name + "at iteration " + iteration + "\n    Check Subcategories: " + result + "  ");
			if (this.commitChangedValue(name, result))
				this.current = true;
			if (!result)
				nextClassifiers.add(name);
		});
		return nextClassifiers;
	}
	
	private Boolean checkSubcategories(String name) {
		Boolean result = false;
		List<String> subcategories = QueryUtil.getSubclassifiers(manager.getStore(), name);
		int subCount = 0;
		for (String x : subcategories){
			if (this.manager.getBooleanFromRelevantCategories(x))
				subCount++;
		}
		// this stream doesn't work
//		long subCount = subcategories.stream().filter(x -> {
//			boolean a = this.manager.getBooleanFromRelevantCategories(name);
//			System.out.println(name + " " + x + " " + a);
//			return a;
//		
//		}).count();
		System.out.println(name + "  " + subCount);
		if (subcategories.size() > 0){
			 result = subCount  >= (thresholdClassifiers * subcategories.size());
		}
		this.log.logLn("Category " + name +  ":\n  Subcategories: " + result + "  " + subcategories.size() + "  " + subCount);
		return result;
	}

	public int getIteration() {
		return iteration;
	}
	
}
