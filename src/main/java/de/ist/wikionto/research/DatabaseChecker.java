package de.ist.wikionto.research;

import java.util.HashMap;
import java.util.Map;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.triplestore.query.QueryUtil;
import de.ist.wikionto.webwiki.CategoryCrawler;

public class DatabaseChecker {
	static MyLogger l = new MyLogger("logs/", "database"); 
	
	public static boolean checkEponymousCat(Dataset dataset) {
		return false;
	}

	public static Map<String, InstanceCheck> checkHypernym(Dataset dataset) {
		ResultSet rs = QueryUtil.executeQuery(dataset, "/sparql/queries/getAllReachableArticlesWithText.sparql");
		QuerySolution qs;
		Map<String, InstanceCheck> resultMap = new HashMap<String, InstanceCheck>();
		String text = null;
		String title = null;
		String first = null;
		while (rs.hasNext()) {
			qs = rs.next();
			text = qs.get("?t").asLiteral().getString();
			title = qs.get("?n").asLiteral().getString();
			first = qs.get("?f").asLiteral().getString();
			l.logLn(title + ": " + first);
			InstanceCheck ic = new InstanceCheck(title, text);
			resultMap.put(ic.getTitle(), ic);
		}
		return resultMap;
	}
	
	private static String getFirstSentence(String html) {
		Document doc = Jsoup.parse(html);
		Element first = doc.select("div.mw-parser-output").first();
		for (Element e : first.children()) {
				if (e.select("img").isEmpty() && !e.is("table") && !e.is("div.hatnote") && !e.is("div.noprint")
						&& !e.is("dl"))
					return e.text();
			}
		
		return "";
	}

	public static boolean checkSemanticallyDistantCat() {
		// TODO: Marcel implements check for Semantically Distant Cat
		return false;
	}

	public static void main(String[] args) {
		Dataset dataset = TDBFactory.createDataset("Computer_languages");
		Map<String, InstanceCheck> resultMap = checkHypernym(dataset);
//		resultMap.forEach((x, y) -> System.out.println(x + ": " + y.result()));
	}
}
