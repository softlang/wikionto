package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class ChildrenBased extends Annotation {
	private double thresholdInstances = 0.34;
	private double thresholdSemantically = 0.4;
	private double thresholdClassifiers = 0.3;
	private static final String URI = "http://myWikiTax.de/";
	HashMap<String, Boolean> classifiers = new HashMap<>();
	String query = "/sparql/queries/getAllUnmarkedClassifiers.sparql";
	Boolean a = true;

	public ChildrenBased(WikiOntoPipeline manager) {
		super(manager,"ChildrenBased");
	}

	@Override
	public void execute() {
		this.log.logDate("Log Start\nThreshold children: " + thresholdInstances + "\nThreshold subcategories: " + thresholdClassifiers + "\n");
		while (a){
			a = false;
			List<String> temp = new ArrayList<>(); 
			Dataset store = this.manager.getStore();
			ResultSet rs = this.query(store, query);
			store.begin(ReadWrite.WRITE);
			Model model = store.getDefaultModel();
			Property marked = model.createProperty(URI + "marked");
			rs.forEachRemaining(qs -> {
				if (qs.contains("?classifier")){
					a = true;
					String classifier = qs.get("?classifier").asResource().getURI();
					String name = qs.get("?name").asLiteral().getString();
					int distant = qs.get("?howManyDistantTypes").asLiteral().getInt();
					int reachable = qs.get("?howManyReachableTypes").asLiteral().getInt();
					log.logLn("Category " + name);
					boolean result = reachable >= (distant * thresholdSemantically);
					
					log.logLn("  Semantically distant: " + result + "  " + distant + "  " + reachable );

					result = checkSubcategories(name) || checkArticles(name);
					log.logLn("Result: " + result + "\n");
					this.manager.putInRelevantCategories(name, result);
					this.classifiers.put(name, result);
					model.createProperty(classifier).addProperty(marked, Boolean.toString(result));
				}
			});
			store.commit();
			store.end();
			
		}
		this.log.logDate("Log End");
	}

	
	private boolean checkArticles(String name) {
		boolean result = false;
		List<String> articles = QueryUtil.getInstancesFromClassifier(manager.getSourceStore(), name);
		long articleSize = articles.size();
		
		long artCount = articles.stream()
				.filter(manager::getFromRelevantArticles).count();
		if (articles.size() > 0){
			result =  artCount >= (thresholdInstances * articleSize);
		}
		this.log.logLn("  Articles: " + result + "  " + articles.size() + "  " + artCount + "  " );
		return result;
	}

	private boolean checkSubcategories(String name) {
		boolean result = false;
		List<String> subcategories = QueryUtil.getSubclassifiers(manager.getSourceStore(), name);
		long subCount = subcategories.stream().filter(manager::getFromRelevantCategories).count();
		if (subcategories.size() > 0){
			result = subCount  >= (thresholdClassifiers * subcategories.size());

		}
		this.log.logLn("  Subcategories: " + result + "  "  + subcategories.size() + "  " + subCount);
		return result;
	}
	

	public HashMap<String, Boolean> getClassifiers() {
		return classifiers;
	}

	public void setClassifiers(HashMap<String, Boolean> classifiers) {
		this.classifiers = classifiers;
	}

}
