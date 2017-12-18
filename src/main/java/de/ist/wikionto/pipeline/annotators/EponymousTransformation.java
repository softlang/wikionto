package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.List;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class EponymousTransformation extends Transformation {

	
	private String queryPath = "/sparql/smells/EponymousClassifier.sparql";

private List<String> deleteInstances = new ArrayList<>();
	private List<String> deleteClassifiers = new ArrayList<>();
	private Dataset store;
	
	public EponymousTransformation(WikiOntoPipeline manager) {
		super(manager,"Eponymous");
		this.store = manager.getStore();
	}

	// needs Hypernym
	
	@Override
	public void execute() {
		log.logDate("Write transformation " + this.name + " to store " + this.manager.getStoreName());
		ResultSet rs = QueryUtil.executeQuery(store, queryPath);
		rs.forEachRemaining(qs -> {
			boolean check = this.check(qs);
			String name = qs.get("?cname").asLiteral().getString();
			if (check) {
				log.logLn("Delete Category " + name);
				deleteClassifiers.add(name);
				
			} else {
				log.logLn("Delete Article " + name);
				deleteInstances.add(name);
				
			}
		});
		TransformationUtil.removeInstances(store, deleteInstances);
		TransformationUtil.moveUp(store, deleteClassifiers);
		TransformationUtil.removeClassifiers(store, deleteClassifiers);
		log.logDate("Finish Transformation " + this.name);
	}

	public boolean check(QuerySolution qs) {
		if (qs.contains("?cname")) {
			String name = qs.get("?cname").asLiteral().getString();
			return this.manager.getBooleanFromRelevantArticles(name);
		}
		return false;
	}

}
