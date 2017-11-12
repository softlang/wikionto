package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class EponymousTransformation extends Transformation {

	
	private String queryPath = "/sparql/queries/getEponymousInstances.sparql";

	private String queryClassifiers = "/sparql/queries/getAllClassifiers.sparql";
	private String queryInstances = "/sparql/queries/getAllReachableArticles.sparql";
	private Map<String,Resource> instances = new HashMap<>();
	private Map<String,Resource> classifiers = new HashMap<>();
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
		this.log.logDate("Write transformation " + this.name + " to store " + this.manager.getStoreName());
		this.instances = QueryUtil.getReachableInstanceResources(store);
		this.classifiers = QueryUtil.getReachableClassifierResources(store);
		ResultSet rs = query(store, queryPath);
		rs.forEachRemaining(qs -> {
			boolean check = this.check(qs);
			String name = qs.get("?name").asLiteral().getString();
			if (check) {
				this.log.logLn("Delete Category " + name);
				deleteClassifiers.add(name);
				
			} else {
				this.log.logLn("Delete Article " + name);
				deleteInstances.add(name);
				
			}
		});
		TransformationUtil.removeInstances(store, deleteInstances);
		TransformationUtil.moveUp(store, deleteClassifiers);
		TransformationUtil.removeClassifiers(store, deleteClassifiers);
		this.log.logDate("Finish Transformation " + this.name);
	}

	public boolean check(QuerySolution qs) {
		if (qs.contains("?name")) {
			String name = qs.get("?name").asLiteral().getString();
			return this.manager.getFromRelevantArticles(name);
		}
		return false;
	}

}
