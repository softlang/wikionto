package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.Map;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.graph.Graph;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ParameterizedSparqlString;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.update.UpdateAction;

public class TransformationUtil {

	public static void removeClassifier(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove isA relations
		String query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?s :isA ?o .}\n" + "WHERE {"
				+ "{ SELECT DISTINCT ?s ?o WHERE " + "{ " + "?s :name ?name "
				+ "FILTER REGEX (str(?s),\"Classifier\"). " + "?s :isA ?o. " + " }} " + "UNION "
				+ "{ SELECT DISTINCT ?s ?o WHERE " + "{ " + "?o :name ?name "
				+ "FILTER REGEX (str(?o),\"Classifier\"). " + "?s :isA ?o. " + " }}} ";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);

		// remove instanceOf Relations
		query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?i :instanceOf ?c .}\n" + "WHERE{\n"
				+ "?i :instanceOf ?c .\n" + "FILTER(regex(STR(?c),\"Classifier\")) .\n" + "?c :name ?name . }";
		pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);
		dataset.commit();

		dataset.end();
	}

	public static void removeInstance(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove instanceOf relations
		String query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?a :instanceOf ?b.}\n" + "WHERE{\n"
				+ "?a :instanceOf ?b .\n" + "FILTER(regex(STR(?a),\"Instance\")) .\n" + "?a :name ?name . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);

		dataset.commit();

		dataset.end();
	}

	public static void deleteInstanceOf(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove instanceOf relations
		String query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?b ?r ?a .}\n" + "WHERE{\n"
				+ "?b ?r ?a .\n" + "FILTER(regex(STR(?a),\"Instance\")) .\n" + "?a :name ?name . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);
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
