package de.ist.wikionto.triplestore.query;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

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
import com.hp.hpl.jena.rdf.model.Resource;

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
	
	public static List<String> getReachableClassifiers(Dataset dataset) {
		List<String> result = new ArrayList<>();
		String sparql = "PREFIX : <http://myWikiTax.de/> SELECT DISTINCT  ?name "
				+ "WHERE {	"
				+ "?c :name ?name.	?c :isA* ?root.	"
				+ "?root :name \"Computer_languages\".	"
				+ "FILTER regex(str(?c), \"Classifier\").}";
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(sparql);
		ResultSet rs = QueryExecutionFactory.create(query, dataset).execSelect();
		rs.forEachRemaining(qs -> {
			result.add(qs.get("name").asLiteral().getString());
		});
		dataset.end();
		return result;
	}
	
	public static List<String> getReachableArticles(Dataset dataset) {
		List<String> result = new ArrayList<>();
		String sparql = "PREFIX : <http://myWikiTax.de/> SELECT DISTINCT  ?name "
				+ "WHERE {	"
				+ "?i :instanceOf ?c."
				+ "?c :isA* ?root."
				+ "?root :name \"Computer_languages\"."
				+ "?i :name ?name."
				+ "FILTER regex(str(?i), \"Instance\")"
				+ "}";
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(sparql);
		ResultSet rs = QueryExecutionFactory.create(query, dataset).execSelect();
		rs.forEachRemaining(qs -> {
			result.add(qs.get("name").asLiteral().getString());
		});
		dataset.end();
		return result;
	}

	public static List<String> getClassifiersFromInstance(Dataset dataset, String i) {
		String query = "PREFIX : <http://myWikiTax.de/>\nSELECT ?cname WHERE{ \n?c :name ?cname . \n"
				+ "?i :instanceOf ?c . \n?i :name ?iname . }";
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

	public static List<String> getInstancesFromClassifier(Dataset dataset, String typename) {
		String query = "PREFIX : <http://myWikiTax.de/>\nSELECT ?iname WHERE{ \n?c :name ?cname . \n"
				+ "?i :instanceOf ?c . \n?i :name ?iname . }";
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
	
	public static Map<String,Resource> getReachableInstanceResources(Dataset dataset){
		Map<String,Resource> result = new HashMap<>();
		String sparql = "PREFIX : <http://myWikiTax.de/> SELECT DISTINCT ?i ?name "
				+ "WHERE {	"
				+ "?i :instanceOf ?c."
				+ "?c :isA* ?root."
				+ "?root :name \"Computer_languages\"."
				+ "?i :name ?name."
				+ "FILTER regex(str(?i), \"Instance\")"
				+ "}";
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(sparql);
		ResultSet rs = QueryExecutionFactory.create(query, dataset).execSelect();
		rs.forEachRemaining(qs -> {
			String name = qs.get("?name").asLiteral().getString();
			Resource res = qs.getResource("?i");
			result.put(name, res);
		});
		dataset.end();
		return result;
	}
	
	public static Map<String,Resource> getReachableClassifierResources(Dataset dataset){
		Map<String,Resource> result = new HashMap<>();
		String sparql = "PREFIX : <http://myWikiTax.de/> SELECT DISTINCT ?c ?name "
				+ "WHERE {	"
				+ "?c :name ?name.	"
				+ "?c :isA* ?root.	"
				+ "?root :name \"Computer_languages\".	"
				+ "FILTER regex(str(?c), \"Classifier\"). "
				+ "}";
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(sparql);
		ResultSet rs = QueryExecutionFactory.create(query, dataset).execSelect();
		rs.forEachRemaining(qs -> {
			String name = qs.get("?name").asLiteral().getString();
			Resource res = qs.getResource("?c");
			result.put(name, res);
		});
		dataset.end();
		return result;
	}

	public static List<String> getSuperclassifiers(Dataset dataset, String typename) {
		String query = "PREFIX : <http://myWikiTax.de/> \nSELECT DISTINCT ?scname WHERE {\n?sc :name ?scname ."
				+ "\n?c :isA ?sc ." + "\n?c :name ?cname ." + " ?c :depth ?depth." + "} ORDER BY ASC (?depth)";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("cname", typename);
		dataset.begin(ReadWrite.READ);
		ResultSet results = null;
		List<String> subtypes = new ArrayList<>();
		try (QueryExecution qe = QueryExecutionFactory.create(pss.toString(), dataset)) {
			results = qe.execSelect();
//			System.out.println(results.hasNext());
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
				+ "\n?o :isA ?s ." + "\n?o :name ?sname . } ";
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

	public static List<String> getClassifiersAtDepth(Dataset dataset, int depth) {
		String query = "PREFIX : <http://myWikiTax.de/> \nSELECT DISTINCT ?sname WHERE {\n?s :name ?typename ."
				+ "\n?o :isA ?s ." + "\n?o :name ?sname . } ";
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(query);
		pss.setLiteral("depth", depth);
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
	 * Return the path from the classifier to a target classifier. The algorithm
	 * is based on the idea of BFS. For each classifier added to the front we
	 * state the constraint that there should be a way to the target classifier
	 * in the first place.
	 *
	 * @param dataset
	 * @param from
	 * @param to
	 * @return
	 */
	public static List<String> getPathFromClassToClass(Dataset dataset, String from, String to) {
		List<String> nextcs = determineNextClassifiersOnPathCC(dataset, from, to);

		List<List<String>> front = new ArrayList<>();
		for (String s : nextcs) {
			ArrayList<String> cs = new ArrayList<>();
			cs.add(s);
			front.add(cs);
		}
		while (!front.isEmpty()) {
			// check the front whether the target is already reached
			List<List<String>> finished = front.stream().filter(l -> l.get(l.size() - 1).equals(to))
					.collect(Collectors.toList());
			if (!finished.isEmpty()) {
				return finished.get(0);
			}
			// build a new front based on the next classifiers on the way.
			List<List<String>> temp = new ArrayList<>();
			for (List<String> f : front) {
				String last = f.get(f.size() - 1);
				List<String> overs = determineNextClassifiersOnPathCC(dataset, last, to);
				if (overs.isEmpty()) {
					continue;
				}
				for (String o : overs) {
					List<String> newf = new ArrayList<>();
					newf.addAll(f);
					newf.add(o);
					temp.add(newf);
				}
			}
			front = temp;
		}

		return new ArrayList<>();

	}

	private static List<String> determineNextClassifiersOnPathCC(Dataset dataset, String from, String to) {
		List<String> os = new ArrayList<>();
		String q = "PREFIX : <http://myWikiTax.de/>" + "\nSELECT DISTINCT ?o WHERE {" + "\n ?cfrom :name \"" + from
				+ "\" ." + "\n ?cto :name \"" + to + "\" ." + "\n ?cfrom :hasSubclassifier ?cover ."
				+ "\n ?cover :hasSubclassifier* ?cto ." + "\n ?cover :name ?o . }";
		dataset.begin(ReadWrite.READ);
		try (QueryExecution qe = QueryExecutionFactory.create(q, dataset)) {
			ResultSet results = qe.execSelect();
			while (results.hasNext()) {
				QuerySolution r = results.next();
				os.add(r.get("o").toString());
			}
		} catch (Exception e) {
			System.err.println("Query execution failed");
			e.printStackTrace();
		}
		dataset.end();
		return os;
	}

	public static List<String> getPathFromClassToInstance(Dataset dataset, String start, String aim) {
		List<String> nextcs = determineNextClassifiersOnPathCI(dataset, start, aim);
		// the instance may be classified by start
		if (getInstancesFromClassifier(dataset, start).contains(aim)) {
			ArrayList<String> rs = new ArrayList<>();
			rs.add(aim);
			return rs;
		}
		// build the initial front
		List<List<String>> front = new ArrayList<>();
		for (String s : nextcs) {
			ArrayList<String> cs = new ArrayList<>();
			cs.add(s);
			front.add(cs);
		}
		while (!front.isEmpty()) {
			// check the front whether the target is already reached
			List<List<String>> finished = front.stream()
					.filter(l -> getInstancesFromClassifier(dataset, l.get(l.size() - 1)).contains(aim)).collect(Collectors.toList());
			if (!finished.isEmpty()) {
				ArrayList<String> rs = new ArrayList<>();
				rs.addAll(finished.get(0));
				rs.add(aim);
				return rs;
			}
			// build a new front based on the next classifiers on the way.
			List<List<String>> temp = new ArrayList<>();
			for (List<String> f : front) {
				String last = f.get(f.size() - 1);
				List<String> overs = determineNextClassifiersOnPathCI(dataset, last, aim);
				if (overs.isEmpty()) {
					continue;
				}
				for (String o : overs) {
					List<String> newf = new ArrayList<>();
					newf.addAll(f);
					newf.add(o);
					temp.add(newf);
				}
			}
			front = temp;
		}

		return new ArrayList<>();
	}

	private static List<String> determineNextClassifiersOnPathCI(Dataset dataset, String from, String to) {
		List<String> os = new ArrayList<>();
		String q = "PREFIX : <http://myWikiTax.de/>" + "\nSELECT DISTINCT ?o WHERE {" + "\n ?cfrom :name \"" + from
				+ "\" ." + "\n ?ito :name \"" + to + "\" ." + "\n ?cfrom :hasSubclassifier ?cover ."
				+ "\n ?cover :hasSubclassifier*/:classifies ?ito ." + "\n ?cover :name ?o . }";
		dataset.begin(ReadWrite.READ);
		try (QueryExecution qe = QueryExecutionFactory.create(q, dataset)) {
			ResultSet results = qe.execSelect();
			while (results.hasNext()) {
				QuerySolution r = results.next();
				os.add(r.get("o").toString());
			}
		} catch (Exception e) {
			System.err.println("Query execution failed");
			e.printStackTrace();
		}
		dataset.end();
		return os;
	}

	public static List<String> getReachableClassifiers(Dataset dataset, String i, String root) {
		String query = "PREFIX : <http://myWikiTax.de/>\nSELECT DISTINCT ?cname WHERE{ \n?c :name ?cname . "
				+ "\n?c :classifies ?i ." + "\n?r :name \"" + root + "\" . "
				+ "\nFILTER EXISTS{?r :hasSubclassifier* ?c .}" + "\n?i :name ?iname . }";
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

	public static List<String> getReachableInstances(Dataset dataset, String i, String root) {
		String query = "PREFIX : <http://myWikiTax.de/>\nSELECT DISTINCT ?cname WHERE{ \n?c :name ?cname . "
				+ "\n?c :classifies ?i ." + "\n?r :name \"" + root + "\" . "
				+ "\nFILTER EXISTS{?r :hasSubclassifier* ?c .}" + "\n?i :name ?iname . }";
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

	public static ResultSet executeRootDependentQuery(Dataset dataset, String p, String root) {
		File smellFile = new File(System.getProperty("user.dir") + p);

		String queryString = null;
		try {
			queryString = FileUtils.readFileToString(smellFile);
		} catch (IOException e) {
			e.printStackTrace();
		}
		dataset.begin(ReadWrite.READ);
		System.out.println("-" + root + "-");
		Query query = QueryFactory.create(queryString.replaceAll("\\?root", "\"" + root + "\""), Syntax.syntaxARQ);
		dataset.end();
		return new QueryProcessor(query, dataset).query();
	}



}
