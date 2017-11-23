package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class CleanUp extends Transformation {
	Dataset store;
	String deleteInstancesQuery = "/cleanUpIrrelevantInstances.sparql";
	String deleteClassifiersQuery = "/cleanUpClassifier.sparql";
	String moveUp = "";
	
	public CleanUp(WikiOntoPipeline manager) {
		super(manager, "CleanUp");
		this.store = this.manager.getStore();
	}

	@Override
	public void execute() {
		log.logDate("Start " + this.getName());
		
		System.out.println("Delete instances: " + cleanUpInstances());
		System.out.println("Delete classifiers: " + cleanUpClassifiers());
		cleanUpUnreachableClassifiers();
		log.logDate("Finish " + this.getName());
	}

	private int cleanUpInstances(){
		List<String> deleteInstances = QueryUtil.getReachableInstances(this.store).stream()
			.filter(key -> !this.manager.getOptionalFromRelevantArticles(key).orElse(false))
			.collect(Collectors.toList());
		deleteInstances.forEach(name -> {
			log.logLn("Remove article " + name);
//			TransformationUtil.removeInstance(this.store,name);
		});
		System.out.println(TransformationUtil.transformFile(this.store, deleteInstancesQuery, new HashMap<>()));
		return deleteInstances.size();
	}
	
	private int cleanUpClassifiers(){
		List<String> deleteClassifiers = QueryUtil.getReachableClassifiers(this.store).stream()
			.filter(key -> !this.manager.getOptionalFromRelevantCategories(key).orElse(false))
			.collect(Collectors.toList());
		TransformationUtil.moveUp(this.store, deleteClassifiers);
		TransformationUtil.transformFile(this.store, "/removeIrrelevantClassifiers.sparql", new HashMap<>());
		deleteClassifiers.forEach(name -> {
			log.logLn("Remove category " + name);
		});
		return deleteClassifiers.size();
	}
	
	private void cleanUpUnreachableClassifiers(){
		TransformationUtil.transformFile(this.store, "/removeInstanceOfs.sparql", new HashMap<>());
		TransformationUtil.transformFile(this.store, "/removeSubclassifiersFromIrrelevantClassifiers.sparql", new HashMap<>());
	}
}
