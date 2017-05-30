package de.ist.wikionto.research;

import java.util.HashMap;
import java.util.Map;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class DatabaseChecker {
	public static boolean checkEponymousCat(Dataset dataset) {
		return false;
	}

	public static Map<String, InstanceCheck> checkHypernym(Dataset dataset) {
		ResultSet rs = QueryUtil.executeQuery(dataset, "/sparql/queries/getAllReachableArticlesWithText.sparql");
		QuerySolution qs;
		Map<String, InstanceCheck> resultMap = new HashMap<String, InstanceCheck>();
		String text = null;
		String title = null;
		while (rs.hasNext()) {
			qs = rs.next();
			text = qs.get("?t").asLiteral().getString();
			title = qs.get("?n").asLiteral().getString();
			InstanceCheck ic = new InstanceCheck(title, text);
			resultMap.put(ic.getTitle(), ic);
		}
		return resultMap;
	}

	public static boolean checkSemanticallyDistantCat() {
		// TODO: Marcel implements check for Semantically Distant Cat
		return false;
	}

	public static void main(String[] args) {
		Dataset dataset = TDBFactory.createDataset("Computer_languages");
		Map<String, InstanceCheck> resultMap = checkHypernym(dataset);
		resultMap.forEach((x, y) -> System.out.println(x + ": " + y.result()));
	}
}
