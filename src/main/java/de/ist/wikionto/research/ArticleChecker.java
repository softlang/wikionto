package de.ist.wikionto.research;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;;

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

}
