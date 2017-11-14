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

	private Map<String,Resource> instances = new HashMap<>();
	private Map<String,Resource> classifiers = new HashMap<>();
	private List<String> baseClassifiers = new ArrayList<>();
	private List<String> baseInstances = new ArrayList<>();
	private List<String> deleteClassifiers = new ArrayList<>();
	private List<String> deleteInstances = new ArrayList<>();
	
	public CleanUp(WikiOntoPipeline manager) {
		super(manager, "CleanUp");
	}

	@Override
	public void execute() {
		log.logDate("Start " + this.getName());
		classifiers = QueryUtil.getReachableClassifierResources(this.manager.getStore());
		instances = QueryUtil.getReachableInstanceResources(this.manager.getStore());
		baseClassifiers = QueryUtil.getReachableClassifiers(this.manager.getStore());
		baseInstances = QueryUtil.getReachableArticles(this.manager.getStore());
		deleteClassifiers = baseClassifiers.stream()
			.filter(key -> !this.manager.getFromRelevantCategories(key))
			.collect(Collectors.toList());
		deleteInstances = baseInstances.stream()
			.filter(key -> !this.manager.getFromRelevantArticles(key))
			.collect(Collectors.toList());
		deleteClassifiers.forEach(name -> log.logLn("Remove category " + name));
		deleteInstances.forEach(name -> log.logLn("Remove article " + name));
		System.out.println(deleteInstances.size());
		System.out.println(deleteClassifiers.size());
//		TransformationUtil.transformFile(this.manager.getStore(), "abandonUnrelevantInstance.sparql" , new HashMap<String, String>());
		TransformationUtil.removeInstances(this.manager.getStore(), deleteInstances);
		TransformationUtil.moveUp(this.manager.getStore(),deleteClassifiers);
		TransformationUtil.removeClassifiers(this.manager.getStore(), deleteClassifiers);
//		TransformationUtil.transformFile(this.manager.getStore(), "abandonUnmarkedClassifier0.sparql" , new HashMap<String, String>());
		log.logDate("Finish " + this.getName());
	}
	
	@Deprecated
	public void moveUp(String name){
		Dataset dataset = this.manager.getStore();
		List<String> children = QueryUtil.getInstancesFromClassifier(this.manager.getStore(), name);
		dataset.begin(ReadWrite.WRITE);
		Model model = dataset.getDefaultModel();
		Property p = model.getProperty("http://myWikiTax.de/instanceOf");
		children.stream()
			.filter(manager::getFromRelevantArticles)
			.forEach(x -> {
				List<String> parents = QueryUtil.getSuperclassifiers(this.manager.getSourceStore(), name);
				parents.forEach(y -> {
					if (this.manager.getFromRelevantCategories(y))
						model.add(this.instances.get(x), p , this.classifiers.get(y));
				});
			});
		dataset.commit();
		dataset.end();
	}


}
