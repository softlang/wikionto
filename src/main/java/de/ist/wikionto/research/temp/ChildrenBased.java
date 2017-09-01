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
	private double threshold_instances = 0.34;
	private double threshold_semantically = 0.4;
	private double threshold_classifiers = 0.3;
	private long cats = 2;
	private static final String URI = "http://myWikiTax.de/";
	HashMap<String, Boolean> classifiers = new HashMap<>();
	String query = "/sparql/queries/getAllClassifiers00.sparql";
	Boolean a = true;

	public ChildrenBased(TransformationManager manager) {
		super(manager,"ChildrenBased");
	}

	@Override
	public void annotate() {

		this.log.logDate("Log Start\nThreshold children: " + threshold_instances + "\nThreshold subcategories: " + threshold_classifiers + "\n");
		this.manager.createNewDatasetName(this.name, this.manager.getStoreName());
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
					boolean result = reachable >= (distant * threshold_semantically);
					
					log.logLn("Semantically distant: " + distant + "  " + reachable );
					result = false;
					result = result || checkSubcategories(name) ;
					result = checkArticles(name) || result;
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
		List<String> articles = QueryUtil.getInstances(manager.getOldStore(), name);
		long articleSize = articles.size();
		
		long artCount = articles.stream()
				.filter(manager::getFromRelevantArticles).count();
		if (articles.size() > 0){
			result =  artCount >= (threshold_instances * articleSize);
		}
		this.log.logLn("Articles: " + articles.size() + "  " + artCount + "  " + result);
		return result;
	}

	private boolean checkSubcategories(String name) {
		boolean result = false;
		List<String> subcategories = QueryUtil.getSubclassifiers(manager.getOldStore(), name);
		long subCount = subcategories.stream().filter(manager::getFromRelevantCategories).count();
		if (subcategories.size() > 0){
			result = subCount  >= (threshold_classifiers * subcategories.size());

		}
		this.log.logLn("Subcategories: "  + subcategories.size() + "  " + subCount + "  " + result);
		return result;
	}
	

	public HashMap<String, Boolean> getClassifiers() {
		return classifiers;
	}

	public void setClassifiers(HashMap<String, Boolean> classifiers) {
		this.classifiers = classifiers;
	}

}
