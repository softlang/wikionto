package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.graph.Graph;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ParameterizedSparqlString;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.update.UpdateAction;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class TransformationUtil {

	public static void removeClassifier(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove isA relations
		String query = "PREFIX : <http://myWikiTax.de/> \n" 
				+ "DELETE {\n" 
				+ "?s :isA ?o .}\n" 
				+ "WHERE {"
				+ "{ SELECT DISTINCT ?s ?o WHERE " 
				+ "{ " + "?s :name ?name "
				+ "FILTER REGEX (str(?s),\"Classifier\"). " 
				+ "?s :isA ?o. " 
				+ " }} " 
				+ "UNION "
				+ "{ SELECT DISTINCT ?s ?o WHERE " 
				+ "{ " 
				+ "?o :name ?name "
				+ "FILTER REGEX (str(?o),\"Classifier\"). " 
				+ "?s :isA ?o. " + " }}} ";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);

		// remove instanceOf Relations
		query = 
			"PREFIX : <http://myWikiTax.de/> \n" 
				+ "DELETE {\n" 
				+ "?i :instanceOf ?c .}\n" 
				+ "WHERE{\n"
				+ "?i :instanceOf ?c .\n" 
				+ "FILTER(regex(STR(?c),\"Classifier\")) .\n" 
				+ "?c :name ?name . }";
		pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
//		UpdateAction.execute(pss.asUpdate(), graph);
		dataset.commit();

		dataset.end();
	}
	
	//TODO Wirte Methode to remove unmarked articles and categories
	
	public static void removeClassifiers(Dataset dataset, List<String> names) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove isA relations
		names.forEach(name -> {
			String query = "PREFIX : <http://myWikiTax.de/> \n" 
					+ "DELETE {\n" 
					+ "?s :isA ?o .}\n" 
					+ "WHERE {"
					+ "{ SELECT DISTINCT ?s ?o WHERE " 
					+ "{ " + "?s :name ?name "
					+ "FILTER REGEX (str(?s),\"Classifier\"). " 
					+ "?s :isA ?o. " 
					+ " }} " 
					+ "UNION "
					+ "{ SELECT DISTINCT ?s ?o WHERE " 
					+ "{ " 
					+ "?o :name ?name "
					+ "FILTER REGEX (str(?o),\"Classifier\"). " 
					+ "?s :isA ?o. " + " }}} ";
			ParameterizedSparqlString pss = new ParameterizedSparqlString();
			pss.setCommandText(query);
			pss.setLiteral("name", name);
			UpdateAction.execute(pss.asUpdate(), graph);

			// remove instanceOf Relations
			query = 
				"PREFIX : <http://myWikiTax.de/> \n" 
					+ "DELETE {\n" 
					+ "?i :instanceOf ?c .}\n" 
					+ "WHERE{\n"
					+ "?i :instanceOf ?c .\n" 
					+ "FILTER(regex(STR(?c),\"Classifier\")) .\n" 
					+ "?c :name ?name . }";
			pss = new ParameterizedSparqlString();
			pss.setCommandText(query);
			pss.setLiteral("name", name);
			UpdateAction.execute(pss.asUpdate(), graph);
		});
		dataset.commit();
		dataset.end();
	}


	public static void removeInstance(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove instanceOf relations
		String query = 
				"PREFIX : <http://myWikiTax.de/> \n" 
						+ "DELETE {\n" + "?a :instanceOf ?b.}\n" 
						+ "WHERE{\n"
						+ "?a :instanceOf ?b .\n" 
						+ "FILTER(regex(STR(?a),\"Instance\")) .\n" 
						+ "?a :name ?name . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);
		dataset.commit();
		dataset.end();
	}
	
	public static void removeInstances(Dataset dataset, List<String> names) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove instanceOf relations
		names.forEach(name -> {
			String query = 
					"PREFIX : <http://myWikiTax.de/> \n" 
							+ "DELETE {\n" + "?a :instanceOf ?b.}\n" 
							+ "WHERE{\n"
							+ "?a :instanceOf ?b .\n" 
							+ "FILTER(regex(STR(?a),\"Instance\")) .\n" 
							+ "?a :name ?name . }";
			ParameterizedSparqlString pss = new ParameterizedSparqlString();
			pss.setCommandText(query);
			pss.setLiteral("name", name);
			UpdateAction.execute(pss.asUpdate(), graph);
		});
		dataset.commit();
		dataset.end();
	}
	
	public static void moveUpInstance(Dataset dataset, String name){
		List<String> instances = QueryUtil.getInstancesFromClassifier(dataset, name);
		Map<String,Resource> instanceResources = QueryUtil.getReachableInstanceResources(dataset);
		Map<String,Resource> classifierResources = QueryUtil.getReachableClassifierResources(dataset);
		dataset.begin(ReadWrite.WRITE);
		Model model = dataset.getDefaultModel();
		Property p = model.getProperty("http://myWikiTax.de/instanceOf");
		instances.stream()
			.forEach(x -> {
				List<String> parents = QueryUtil.getSuperclassifiers(dataset, name);
				parents.forEach(y -> {
					model.add(instanceResources.get(x), p , classifierResources.get(y));
				});
			});
		dataset.commit();
		dataset.end();
	}
	
	public static void moveUpInstances(Dataset dataset, List<String> names){
		Map<String,Resource> instanceResources = QueryUtil.getReachableInstanceResources(dataset);
		Map<String,Resource> classifierResources = QueryUtil.getReachableClassifierResources(dataset);
		names.forEach(name -> {
			List<String> instances = QueryUtil.getInstancesFromClassifier(dataset, name);
			List<String> parents = QueryUtil.getSuperclassifiers(dataset, name);
			dataset.begin(ReadWrite.WRITE);
			Model model = dataset.getDefaultModel();
			Property p = model.getProperty("http://myWikiTax.de/instanceOf");
			instances.stream()
				.forEach(x -> {
					parents.forEach(y -> {
						model.add(instanceResources.get(x), p , classifierResources.get(y));
					});
				});
			dataset.commit();
			dataset.end();
		});
		
	}
	
	public static void moveUpClassifier(Dataset dataset, String name){
		List<String> subCats = QueryUtil.getSubclassifiers(dataset, name);
		Map<String,Resource> classifierResources = QueryUtil.getReachableClassifierResources(dataset);
		dataset.begin(ReadWrite.WRITE);
		Model model = dataset.getDefaultModel();
		Property p = model.getProperty("http://myWikiTax.de/isA");
		subCats.stream()
			.forEach(x -> {
				List<String> parents = QueryUtil.getSuperclassifiers(dataset, name);
				parents.forEach(y -> {
					model.add(classifierResources.get(x), p , classifierResources.get(y));
				});
			});
		dataset.commit();
		dataset.end();
	}
	
	public static void moveUpClassifiers(Dataset dataset, List<String> names){
		Map<String,Resource> classifierResources = QueryUtil.getReachableClassifierResources(dataset);
		names.forEach(name -> {
			List<String> subCats = QueryUtil.getSubclassifiers(dataset, name);
			List<String> parents = QueryUtil.getSuperclassifiers(dataset, name);
			dataset.begin(ReadWrite.WRITE);
			Model model = dataset.getDefaultModel();
			Property p = model.getProperty("http://myWikiTax.de/isA");
			subCats.stream()
				.forEach(x -> {
					parents.forEach(y -> {
						model.add(classifierResources.get(x), p , classifierResources.get(y));
					});
				});
			dataset.commit();
			dataset.end();
		});
	}
	
	public static void moveUp(Dataset dataset, String name){
		List<String> subCats = QueryUtil.getSubclassifiers(dataset, name);
		List<String> instances = QueryUtil.getInstancesFromClassifier(dataset, name);
		List<String> parents = QueryUtil.getSuperclassifiers(dataset, name);
		Map<String,Resource> instanceResources = QueryUtil.getReachableInstanceResources(dataset);
		Map<String,Resource> classifierResources = QueryUtil.getReachableClassifierResources(dataset);
		dataset.begin(ReadWrite.WRITE);
		Model model = dataset.getDefaultModel();
		Property isAP = model.getProperty("http://myWikiTax.de/isA");
		Property instanceOfP = model.getProperty("http://myWikiTax.de/instanceOf");
		parents.forEach(parent -> {
			subCats.forEach(subCat -> {
				model.add(classifierResources.get(subCat), isAP , classifierResources.get(parent));
			});
			instances.forEach(instance -> {
				model.add(instanceResources.get(instance), instanceOfP , classifierResources.get(parent));
			});
		});
		dataset.commit();
		dataset.end();
	}
	
	public static void moveUp(Dataset dataset, List<String> names){
		
		Map<String,Resource> instanceResources = QueryUtil.getReachableInstanceResources(dataset);
		Map<String,Resource> classifierResources = QueryUtil.getReachableClassifierResources(dataset);
		names.forEach(name -> {
			List<String> subCats = QueryUtil.getSubclassifiers(dataset, name);
			List<String> instances = QueryUtil.getInstancesFromClassifier(dataset, name);
			List<String> parents = QueryUtil.getSuperclassifiers(dataset, name);
			dataset.begin(ReadWrite.WRITE);
			Model model = dataset.getDefaultModel();
			Property isAP = model.getProperty("http://myWikiTax.de/isA");
			Property instanceOfP = model.getProperty("http://myWikiTax.de/instanceOf");
			parents.forEach(parent -> {
				subCats.forEach(subCat -> {
					model.add(classifierResources.get(subCat), isAP , classifierResources.get(parent));
				});
				instances.forEach(instance -> {
					model.add(instanceResources.get(instance), instanceOfP , classifierResources.get(parent));
				});
			});
			dataset.commit();
			dataset.end();
		});
	}
	
	public static void addInstance(Dataset dataset, Resource instance, Resource classifier){
		dataset.begin(ReadWrite.WRITE);
		Model model = dataset.getDefaultModel();
		Property p = model.getProperty("http://myWikiTax.de/instanceOf");
		model.add(instance, p , classifier);
		dataset.commit();
		dataset.end();
	}
	
	public static long transformFile(Dataset dataset, String tfilename, Map<String, String> parameter) {
		File tfile = new File(System.getProperty("user.dir") + "/sparql/transformations/" + tfilename);
		String transformation = "";
		try {
			transformation = FileUtils.readFileToString(tfile);
		} catch (IOException ex) {
			System.err.println("Exception reading:" + tfilename);
			ex.printStackTrace();
			return 0;
		}
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		long size = graph.size();
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(transformation);
		for (String key : parameter.keySet()) {
			String query = pss.asUpdate().toString();
			if (!parameter.get(key).contains("http://"))
				pss.setLiteral(key, parameter.get(key).trim());
			else
				pss.setIri(key, parameter.get(key).trim());
			if (query.equals(pss.asUpdate().toString())) {
				System.err.println(pss.toString());
				dataset.abort();
				return 0;
			}
		}
		UpdateAction.execute(pss.asUpdate(), graph);
		size = graph.size() - size;
		dataset.commit();
		return size;
	}

}
