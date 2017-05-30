package de.ist.wikionto.research;

import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.webwiki.Wiki;

public class ArticleChecker {

	public static boolean checkTitle(String title) {
		return title.contains("language");
	}

	public static boolean checkInfoBox(String text) {
		Pattern paradigm = Pattern.compile("paradigm", Pattern.CASE_INSENSITIVE);
		Pattern influenced = Pattern.compile("influencd", Pattern.CASE_INSENSITIVE);
		Pattern typing = Pattern.compile("typing", Pattern.CASE_INSENSITIVE);
		Pattern lanuage = Pattern.compile("infox programming language", Pattern.CASE_INSENSITIVE);
		Boolean result = false;
		Document doc = Jsoup.parse(text);
		Elements infos = doc.getElementsByClass("infobox");
		for (Element e : infos) {
			Matcher m = paradigm.matcher(e.text());
			result = result || m.find();
			m = influenced.matcher(e.text());
			result = result || m.find();
			m = typing.matcher(e.text());
			result = result || m.find();
			m = lanuage.matcher(e.text());
			result = result || m.find();
		}
		return result;
	}

	public static boolean checkText(String text) {
		Document doc = Jsoup.parse(text);
		Elements es = doc.getElementsByTag("p");
		boolean result = false;
		Pattern isA = Pattern.compile("is a",
				Pattern.CASE_INSENSITIVE | Pattern.MULTILINE | Pattern.UNICODE_CHARACTER_CLASS);
		Pattern lang = Pattern.compile("language|dsl",
				Pattern.CASE_INSENSITIVE | Pattern.MULTILINE | Pattern.UNICODE_CHARACTER_CLASS);
		int lineNum = 3;
		if (es.size() < lineNum + 1)
			lineNum = es.size();
		for (int i = 0; i < lineNum; i++) {
			// System.out.println(es.get(i).text());
			String[] lines = es.get(i).text().split("\\.");
			for (String line : lines) {
				// System.out.println(line);
				Matcher a = isA.matcher(line);

				if (a.find()) {
					line = line.substring(a.start());
					// System.out.println(line);
					Matcher b = lang.matcher(line);
					if (b.find()) {
						// System.out.println(line);
						return true;
					}
				}
			}
		}
		return false;
	}

	public static void main(String[] args) throws IOException {
		Dataset set = TDBFactory.createDataset("Computer_languages");
		Wiki w = new Wiki();
		String text = w.getRenderedText("Haskell (programming language)");
		String text2 = w.getRenderedText("Oak_(programming_language)");
		// System.out.println(checkTitle("Haskell (programming language)"));
		// System.out.println(checkInfoBox(text));
		// System.out.println(checkTitle("Oak_(programming_language)"));
		// System.out.println(checkInfoBox(text2));
		Document doc = Jsoup.parse(text);
		Elements es = doc.getElementsByTag("p");
		es.forEach(x -> System.out.println(x.text()));

		// ResultSet rs = QueryUtil.executeQuery(set,
		// "/sparql/queries/getAllReachableArticlesWithText.sparql");
		// QuerySolution qs;
		// String text = null;
		// String title;
		// while (rs.hasNext()) {
		// qs = rs.next();
		// text = qs.get("?t").asLiteral().getString();
		// title = qs.get("?n").asLiteral().getString();
		// System.out.println(title + ": " + checkInfoBox(text));
		// }
	}

}
