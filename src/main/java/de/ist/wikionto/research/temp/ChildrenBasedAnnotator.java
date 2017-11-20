package de.ist.wikionto.research.temp;

import java.util.List;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class ChildrenBasedAnnotator extends Annotator {
	private double thresholdInstances = 0.34;
	private double thresholdSemantically = 0.4;
	private double thresholdClassifiers = 0.3;
	private static final String URI = "http://myWikiTax.de/";
	String query = "/sparql/queries/classifier/getAllUnmarkedClassifiers.sparql";
	Boolean a = true;
	Boolean changed = false;
	private  int iteration = 0;
	
	public ChildrenBasedAnnotator(WikiOntoPipeline manager, int iteration) {
		super(manager,"ChildrenBased" + "Iteration" + iteration);
		this.iteration = iteration;
		
	}

	@Override
	public void execute() {
		log.logDate("Log Start + Iteration " + iteration + "\nThreshold children: " + thresholdInstances + "\nThreshold subcategories: " + thresholdClassifiers + "\n");
		changed = false;
		while (a){
			a = false;
			Dataset store = this.manager.getStore();
			ResultSet rs = QueryUtil.executeQuery(store, query);
			store.begin(ReadWrite.WRITE);
			Model model = this.manager.getStore().getDefaultModel();
			Property marked = model.createProperty(URI + "marked");
			QuerySolution qs;
			while (rs.hasNext()){
				qs = rs.next();
				if (qs.contains("?classifier")){
					a = true;
					Resource classifier = qs.get("?classifier").asResource();
					String name = qs.get("?name").asLiteral().getString();
					log.logLn("Category " + name);
					boolean result = false;
					result = checkSubcategories(name);
					result = checkArticles(name) || result;
					log.logLn("  Result: " + result);	
					hasChanged(name,result);
					log.log("\n");
					model.add(classifier,marked, Boolean.toString(result));
					if (result) {
						this.manager.addCategoryAnnotation(name, Annotation.CHILDRENBASED);
					} else {
						this.manager.addCategoryAnnotation(name, Annotation.CHILDRENBASED_FALSE);
					}
				}
			}
			
			store.commit();
			store.end();
			
		}
		log.logDate("Log End");
		log.close();
	}

	
	private void hasChanged(String name, boolean result) {
		boolean old = this.manager.getFromRelevantCategories(name);
		if (old != result) {
			changed = true;		
//			log.logLn("  Changed value");
			this.manager.putInRelevantCategories(name, result);
		}
	}

	private boolean checkArticles(String name) {
		boolean result = false;
		List<String> articles = QueryUtil.getInstances(manager.getSourceStore(), name);
//		System.out.println(name + ": " + articles.toString());
		long articleSize = articles.size();
		long artCount = articles.stream()
				.filter(manager::getFromRelevantArticles).count();
		if (articles.size() > 0){
			result =  artCount >= (thresholdInstances * articleSize);
		}
		log.logLn("  Articles: " + result + "  " + articles.size() + "  " + artCount + "  " );
		return result;
	}

	private boolean checkSubcategories(String name) {
		boolean result = false;
		List<String> subcategories = QueryUtil.getSubclassifiers(manager.getSourceStore(), name);
		long subCount = subcategories.stream().filter(manager::getFromRelevantCategories).count();
		if (subcategories.size() > 0){
			result = subCount  >= (thresholdClassifiers * subcategories.size());
		}
		log.logLn("  Subcategories: " + result + "  "  + subcategories.size() + "  " + subCount);
		return result;
	}

	public boolean hasChanged(){
		return changed;
	}

	public int getIteration() {
		return iteration;
	}

	
}
