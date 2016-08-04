package de.ist.wikionto.triplestore.query;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ParameterizedSparqlString;
import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.Syntax;

public class QueryUtil {

	public static ResultSet executeQuery(Dataset dataset, String p) {
		File smellFile = new File(System.getProperty("user.dir") + p);

		String queryString = null;
		try {
			queryString = FileUtils.readFileToString(smellFile);
		} catch (IOException e) {
			e.printStackTrace();
		}
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(queryString, Syntax.syntaxARQ);
		dataset.end();
		return new QueryProcessor(query, dataset).query();

	}

	public static List<String> getClassifiers(Dataset dataset, String i) {
		String query = "PREFIX : <http://myWikiTax.de/>\nSELECT ?cname WHERE{ \n?c :name ?cname . \n"
				+ "?c :classifies ?i . \n?i :name ?iname . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("iname", i);
		dataset.begin(ReadWrite.READ);
		ResultSet results = null;
		List<String> instances = new ArrayList<>();
		try (QueryExecution qe = QueryExecutionFactory.create(pss.asQuery(), dataset)) {
			results = qe.execSelect();
			while (results.hasNext()) {
				QuerySolution r = results.next();
				instances.add(r.get("cname").toString());
			}
		} catch (Exception e) {
			System.err.println("getClassifiers failed");
			e.printStackTrace();
		}

		dataset.end();
		return instances;
	}

	public static List<String> getInstances(Dataset dataset, String typename) {
		String query = "PREFIX : <http://myWikiTax.de/>\nSELECT ?iname WHERE{ \n?c :name ?cname . \n"
				+ "?c :classifies ?i . \n?i :name ?iname . }";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("cname", typename);
		dataset.begin(ReadWrite.READ);
		ResultSet results = null;
		List<String> instances = new ArrayList<>();
		try (QueryExecution qe = QueryExecutionFactory.create(pss.asQuery(), dataset)) {
			results = qe.execSelect();
			while (results.hasNext()) {
				QuerySolution r = results.next();
				instances.add(r.get("iname").toString());
			}
		} catch (Exception e) {
			System.err.println("getInstances failed");
			e.printStackTrace();
		}

		dataset.end();
		return instances;
	}

	public static List<String> getSuperclassifiers(Dataset dataset, String typename) {
		String query = "PREFIX : <http://myWikiTax.de/> \nSELECT DISTINCT ?scname WHERE {\n?sc :name ?scname ."
				+ "\n?sc :hasSubclassifier ?c ." + "\n?c :name ?cname . } ";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("cname", typename);
		dataset.begin(ReadWrite.READ);
		ResultSet results = null;
		List<String> subtypes = new ArrayList<>();
		try (QueryExecution qe = QueryExecutionFactory.create(pss.toString(), dataset)) {
			results = qe.execSelect();
			System.out.println(results.hasNext());
			while (results.hasNext()) {
				QuerySolution r = results.next();
				subtypes.add(r.get("scname").toString());
			}
		} catch (Exception e) {
			System.err.println();
			e.printStackTrace();
		}
		dataset.end();
		return subtypes;
	}

	public static List<String> getSubclassifiers(Dataset dataset, String typename) {
		String query = "PREFIX : <http://myWikiTax.de/> \nSELECT DISTINCT ?sname WHERE {\n?s :name ?typename ."
				+ "\n?s :hasSubclassifier ?o ." + "\n?o :name ?sname . } ";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("typename", typename);
		dataset.begin(ReadWrite.READ);
		ResultSet results = null;
		List<String> subtypes = new ArrayList<>();
		try (QueryExecution qe = QueryExecutionFactory.create(pss.toString(), dataset)) {
			results = qe.execSelect();
			while (results.hasNext()) {
				QuerySolution r = results.next();
				subtypes.add(r.get("sname").toString());
			}
		} catch (Exception e) {
			System.err.println();
			e.printStackTrace();
		}
		dataset.end();
		return subtypes;
	}

	/**
	 * Return the path from top to down
	 *
	 * @param dataset
	 * @param from
	 * @param to
	 * @return
	 */
	public static List<String> getPathFromClassToClass(Dataset dataset, String from, String to) {
		List<String> result = new ArrayList<String>();
		List<String> subs = getSubclassifiers(dataset, from);
		if (subs.contains(to)) {
			result.add(to);
			return result;
		}
		List<List<String>> front = new ArrayList<>();
		for (String s : subs) {

		}

		return null;
	}

	public static List<String> getPathFromClassToInstance(Dataset dataset, String from, String to) {
		List<String> rs = null;
		return rs;
	}
}
