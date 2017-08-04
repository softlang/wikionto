package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.graph.Graph;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ParameterizedSparqlString;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.update.UpdateAction;

public class TransformationUtil {

	public static void deleteClassifier(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove instanceOf relations
		String query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?i ?r ?c .}\n" + "WHERE{\n"
				+ "?i ?r ?c .\n" + "FILTER(regex(STR(?c),\"Classifier\")) .\n" + "?c :name ?name . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);

		// remove remove isA Relations
		query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?c ?r ?i .}\n" + "WHERE{\n" + "?c ?r ?i .\n"
				+ "FILTER(regex(STR(?c),\"Classifier\")) .\n" + "?c :name ?name . }";
		pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);
		dataset.commit();

		dataset.end();
	}

	public static void deleteInstance(Dataset dataset, String name) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		// remove instanceOf relations
		String query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?b ?r ?a .}\n" + "WHERE{\n"
				+ "?b ?r ?a .\n" + "FILTER(regex(STR(?a),\"Instance\")) .\n" + "?a :name ?name . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);

		// remove remove isA Relations
		query = "PREFIX : <http://myWikiTax.de/> \n" + "DELETE {\n" + "?a ?r ?b .}\n" + "WHERE{\n" + "?a ?r ?b .\n"
				+ "FILTER(regex(STR(?a),\"Instance\")) .\n" + "?a :name ?name . }";
		pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("name", name);
		UpdateAction.execute(pss.asUpdate(), graph);
		dataset.commit();

		dataset.end();
	}

}
