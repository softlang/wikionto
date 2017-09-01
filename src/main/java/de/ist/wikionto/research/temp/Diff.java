package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class Diff {
	private static String gold = "Computer_languages_gold";
	private static MyLogger log = new MyLogger("logs/", "Diff");
	
	private static String matchName(String name){
		return name.replaceAll(" ", "_");
	}
	
	public static List<String> getGoldClassifiers() {
		Dataset dataset = TDBFactory.createDataset(gold);
		List<String> result = new ArrayList<>();
		String sparql = "PREFIX : <http://myWikiTax.de/> SELECT DISTINCT ?name WHERE {   ?root :name \"Computer languages\".   ?root :hasSubclassifier* ?c.   ?c :name ?name.} ORDER BY ASC (?name)";
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(sparql);
		ResultSet rs = QueryExecutionFactory.create(query, dataset).execSelect();
		rs.forEachRemaining(qs -> {
			result.add(qs.get("name").asLiteral().getString());
		});
		dataset.end();
		return result;
	}
	
	public static List<String> getGoldArticles() {
		Dataset dataset = TDBFactory.createDataset(gold);
		List<String> result = new ArrayList<>();
		String sparql = "PREFIX : <http://myWikiTax.de/> SELECT DISTINCT ?name WHERE {   ?c :classifies ?i.   ?root :name \"Computer languages\".   ?root :hasSubclassifier* ?c.   ?i :name ?name.} ORDER BY ASC (?name)";
		dataset.begin(ReadWrite.READ);
		Query query = QueryFactory.create(sparql);
		ResultSet rs = QueryExecutionFactory.create(query, dataset).execSelect();
		rs.forEachRemaining(qs -> {
			result.add(qs.get("name").asLiteral().getString());
		});
		dataset.end();
		return result;
	}
	
	public static void stats(Dataset dataset){
		List<String> articles = QueryUtil.getReachableArticles(dataset);
		List<String> categories = QueryUtil.getReachableClassifiers(dataset);
		List<String> gold_articles = getGoldArticles();
		List<String> gold_categories = getGoldClassifiers();
		
		long category_count = gold_categories.stream().filter(name -> categories.contains(matchName(name))).count();
		long article_count = gold_articles.stream().filter(name -> articles.contains(matchName(name))).count();
		log.logLn("Number of article in gold standard : " + gold_articles.size());
		log.logLn("Number of article in own store : " + articles.size());
		log.logLn("Number of article in both: " + article_count);
		log.logLn("Article precision = " + (article_count/(double)articles.stream().count()));
		log.logLn("Article recall = " + (article_count/(double)gold_articles.stream().count()));
		log.logLn("Number of categories in gold standard : " + gold_categories.size());
		log.logLn("Number of categories in own store : " + categories.size());
		log.logLn("Number of categories in both: " + category_count);
		log.logLn("Category precision = " + (category_count/(double)categories.stream().count()));
		log.logLn("Category recall = " + (category_count/(double)gold_categories.stream().count()));
		
	}

	public static void diffClassifier(Dataset dataset){
		List<String> categories = QueryUtil.getReachableClassifiers(dataset);
		List<String> gold_categories = getGoldClassifiers();
		List<String> union = gold_categories.stream().map(Diff::matchName).filter(name -> categories.contains(name)).collect(Collectors.toList());
		log.logLn("Categories in gold standard and not in own store: ");
		gold_categories.stream()
			.sorted()
			.map(Diff::matchName)
			.filter(name -> !union.contains(name))
			.forEach(log::logLn);
		
		log.logLn("\nCategories in own store and not in gold standard: ");
		categories.stream()
			.sorted()
			.filter(name -> !union.contains(name))
			.forEach(log::logLn);
	}
	
	public static void diffInstances(Dataset dataset){
		List<String> articles = QueryUtil.getReachableArticles(dataset);
		List<String> gold_articles = getGoldArticles();
		List<String> union = gold_articles.stream().map(Diff::matchName).filter(name -> articles.contains(name)).collect(Collectors.toList());
		log.logLn("Articles in gold standard and not in own store: ");
		gold_articles.stream()
			.sorted()
			.map(Diff::matchName)
			.filter(name -> !union.contains(name))
			.forEach(log::logLn);
		
		log.logLn("\nArticles in own store and not in gold standard: ");
		articles.stream()
			.sorted()
			.filter(name -> !union.contains(name))
			.forEach(log::logLn);

	}
	
	
	public static void main(String[] args) {
		Dataset ds = TDBFactory.createDataset("Computer_languages_Eponymous_ChildrenBased_CleanUp");
		log.logDate("Start diff");
		stats(ds);
		log.logLn("");
		diffClassifier(ds);
		log.logLn("");
		diffInstances(ds);
		log.logDate("Finish diff");
	}
}
