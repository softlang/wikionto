package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.hp.hpl.jena.query.QuerySolution;

import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.TypedDependency;

public class ArticleChecker implements Runnable {
	String queryPath = "sparql/queries/getAllReachableArticlesWithText.sparql";
	LexicalizedParser lp;
	TokenizerFactory<CoreLabel> tokenizerFactory;
	GrammaticalStructureFactory gsf;
	List<QuerySolution> qss;

	ArticleCheckManager acm;
	QuerySolution qs;

	public ArticleChecker(QuerySolution qs, ArticleCheckManager acm) {
		this.acm = acm;
		this.qs = qs;
	}

	public boolean checkTitle(String title) {
		return title.contains("language");
	}

	public boolean checkInfoBox(String text) {
		Pattern paradigm = Pattern.compile("paradigm", Pattern.CASE_INSENSITIVE);
		Pattern influenced = Pattern.compile("influencd", Pattern.CASE_INSENSITIVE);
		Pattern typing = Pattern.compile("typing", Pattern.CASE_INSENSITIVE);
		Pattern language = Pattern.compile("infox programming language", Pattern.CASE_INSENSITIVE);
		Boolean result = false;
		Document doc = Jsoup.parse(text);
		Elements infos = doc.getElementsByClass("infobox");
		for (Element e : infos) {
			Matcher m1 = paradigm.matcher(e.text());
			result = result || m1.find();
			Matcher m2 = influenced.matcher(e.text());
			result = result || m2.find();
			Matcher m3 = typing.matcher(e.text());
			result = result || m3.find();
			Matcher m4 = language.matcher(e.text());
			result = result || m4.find();
		}
		// l.logLn("infobox test: " + result);
		return result;
	}

	public boolean checkText(String first) {
		Set<String> langs = new HashSet<>();
		langs.add("language");
		langs.add("dsl");
		List<TypedDependency> tdl;
		String text = first;
		// String text = first.replaceAll("\\(.*?\\)", "");
		text = text.replaceAll("\\[.*?\\]", " ");
		String[] all = text.split("\\. ", 0);
		text = all[0];
		tdl = acm.stanford(text);
		List<TypedDependency> nmods = new ArrayList<>();
		List<TypedDependency> cops = new ArrayList<>();
		tdl.forEach(td -> {
			if (td.reln().getShortName().equals("cop")) {
				cops.add(td);
			}
			if (td.reln().getShortName().contains("nmod")) {
				nmods.add(td);
			}
		});
		for (String lang : langs) {
			for (TypedDependency cop : cops) {
				// System.out.println(cop);
				if (cop.gov().originalText().equals(lang))
					return true;
				else if (checkNMods(lang, cop.gov(), nmods))
					return true;
			}

		}
		return false;
	}

	private boolean checkNMods(String lang, IndexedWord gov, List<TypedDependency> nmods) {
		for (TypedDependency nmod : nmods) {
			if (nmod.gov().equals(gov)) {
				if (nmod.dep().originalText().contains(lang))
					return true;
				else
					return checkNMods(lang, nmod.dep(), nmods);
			}

		}
		return false;
	}

	public boolean check(QuerySolution qs) {
		String text = qs.get("?text").asLiteral().getString();
		String title = qs.get("?name").asLiteral().getString();
		String first = qs.get("?first").asLiteral().getString();
		boolean textC = this.checkText(first);
		boolean infoC = this.checkInfoBox(text);
		acm.putArticleCheck(title, textC || infoC);
		acm.l.logLn(title + ":\n	textCheck: " + textC + "\n	infoboxCheck: " + infoC);
		return textC || infoC;
	}

	@Override
	public void run() {
		String text = qs.get("?t").asLiteral().getString();
		String title = qs.get("?n").asLiteral().getString();
		String first = qs.get("?f").asLiteral().getString();
		boolean textC = this.checkText(first);
		boolean infoC = this.checkInfoBox(text);
		acm.putArticleCheck(title, textC || infoC);
		acm.l.logLn(title + ":\n	textCheck: " + textC + "\n	infoboxCheck: " + infoC);
	}

}
