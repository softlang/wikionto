package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

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

	Pattern paradigm = Pattern.compile("paradigm", Pattern.CASE_INSENSITIVE);
	Pattern influenced = Pattern.compile("influencd", Pattern.CASE_INSENSITIVE);
	Pattern typing = Pattern.compile("typing", Pattern.CASE_INSENSITIVE);
	Pattern language = Pattern.compile("infox programming language", Pattern.CASE_INSENSITIVE);
	
	Pattern extension = Pattern.compile("filename extension", Pattern.CASE_INSENSITIVE);
	Pattern type = Pattern.compile("type of format", Pattern.CASE_INSENSITIVE);
	Pattern open = Pattern.compile("open format", Pattern.CASE_INSENSITIVE);
	
	private String title;
	private String keyword;
	
	private boolean textCheck = false;
	private boolean infoCheck = false;
	
	private Set<String> langs = new HashSet<>();
	
	public ArticleChecker(QuerySolution qs, ArticleCheckManager acm) {
		this.acm = acm;
		this.qs = qs;
	}

	public boolean checkTitle(String title) {
		return title.contains("language");
	}

	public boolean checkInfoBox(String text) {
		Boolean result = false;
		Document doc = Jsoup.parse(text);
		Elements infos = doc.getElementsByClass("infobox");
		for (Element e : infos) {
			result = result || checkInfoboxLanguage(e) || checkInfoboxFormat(e);
		}
		return result;
	}

	private boolean checkInfoboxFormat(Element e) {
		Boolean result = false;
		result = result || extension.matcher(e.text()).find();
		result = result || type.matcher(e.text()).find();
		result = result || open.matcher(e.text()).find();
		if (result){
			this.keyword = "format";
			acm.putInKeywords(title, "format");
		}
		return result;
	}

	private boolean checkInfoboxLanguage(Element e) {
		Boolean result = false;
		Matcher m1 = paradigm.matcher(e.text());
		result = result || m1.find();
		Matcher m2 = influenced.matcher(e.text());
		result = result || m2.find();
		Matcher m3 = typing.matcher(e.text());
		result = result || m3.find();
		Matcher m4 = language.matcher(e.text());
		result = result || m4.find();
		if (result) {
			this.keyword = "language";
			acm.putInKeywords(title, "language");
		}
		return result;
	}

	public boolean checkText(String first) {
		langs.add("language");
		langs.add("dsl");
		langs.add("dialect");
		langs.add("format");
		langs = langs.stream().map(String::toLowerCase).collect(Collectors.toSet());
		String text = first;
		// String text = first.replaceAll("\\(.*?\\)", "");
		text = text.replaceAll("\\[.*?\\]", " ");
		String[] all = text.split("\\. ", 0);
		text = all[0];
		List<TypedDependency> tdl = acm.stanford(text);
		List<TypedDependency> nmods = new ArrayList<>();
		List<IndexedWord> cops = new ArrayList<>();
		tdl.forEach(td -> {
			if (td.reln().getShortName().equals("cop")) {
				cops.add(td.gov());
			}
			if (td.reln().getShortName().contains("nmod")) {
				nmods.add(td);
			}
		});
		for (String lang : langs) {
			for (IndexedWord cop : cops) {
				if (cop.originalText().toLowerCase().equals(lang.toLowerCase())){
					acm.putInKeywords(title, lang);
					this.keyword = lang;
					return true;
				}
				else if (checkNMods(lang, cop, nmods)){
					return true;
				}
			}

		}
		return false;
	}
	
	public boolean checkText2(String first) {
		langs.add("language");
		langs.add("dsl");
		langs.add("dialect");
		langs.add("format");
		langs = langs.stream().map(String::toLowerCase).collect(Collectors.toSet());
		String text = first;
		// String text = first.replaceAll("\\(.*?\\)", "");
		text = text.replaceAll("\\[.*?\\]", " ");
		String[] all = text.split("\\. ", 0);
		text = all[0];
		List<TypedDependency> tdl = acm.stanford(text);
		List<TypedDependency> nmods = new ArrayList<>();
		List<IndexedWord> cops = new ArrayList<>();
		tdl.forEach(td -> {
			if (td.reln().getShortName().equals("cop")) {
				cops.add(td.gov());
			}
			if (td.reln().getShortName().contains("nmod")) {
				nmods.add(td);
			}
		});
		textCheck = cops.stream()
				.map(x -> x.originalText().toLowerCase())
				.anyMatch(gov -> {
					if (langs.contains(gov)){
						this.keyword = gov;
						acm.putInKeywords(this.title, gov);
						return true;
					} else
						return false;
				});
		List<IndexedWord> base = nmods.stream().map(TypedDependency::dep).collect(Collectors.toList());
		if (!textCheck)
			cops.stream()
				.filter(base::contains)
				.forEach(gov -> {
					checkNMods(langs, gov, nmods);
				});
			
		return textCheck;
	}
	 
	
	private boolean checkNMods(String lang, IndexedWord gov, List<TypedDependency> nmods) {
		for (TypedDependency nmod : nmods) {
			if (nmod.gov().equals(gov)) {
				if (nmod.dep().originalText().toLowerCase().contains(lang)){
					this.keyword = lang;
					this.acm.putInKeywords(this.title, lang);
					return true;
				} else {
					return checkNMods(lang, nmod.dep(), nmods);
				}
			}

		}
		return false;
	}
	
	private void checkNMods(Set<String> langs, IndexedWord gov, List<TypedDependency> nmods) {
		langs.forEach(lang -> {
			if (checkNMods(lang, gov, nmods)) {
				this.textCheck = true;
				this.keyword = lang;
				this.acm.putInKeywords(title, lang);
			}
		});
	}

	public boolean check(QuerySolution qs) {
		String text = qs.get("?text").asLiteral().getString();
		String title = qs.get("?name").asLiteral().getString();
		this.title = title;
		String first = qs.get("?first").asLiteral().getString();
		boolean textC = this.checkText(first);
		boolean infoC = this.checkInfoBox(text);
		acm.addArticles(title);
		ArticleCheckManager.l.logLn(title + ":\n	textCheck: " + textC + "\n	infoboxCheck: " + infoC);
		return textC || infoC;
	}

	@Override
	public void run() {
		String text = qs.get("?t").asLiteral().getString();
		String title = qs.get("?n").asLiteral().getString();
		this.title = title;
		this.keyword = null;
		String first = qs.get("?f").asLiteral().getString();
		boolean textC = this.checkText(first);
		boolean infoC = this.checkInfoBox(text);
		if (infoC)
			acm.getInfoboxChecks().add(title);
		if (textC)
			acm.getTextChecks().add(title);
		acm.getArticles().add(title);
		ArticleCheckManager.l.logLn(title + ": " + keyword + "\n	textCheck: " + textC + "\n	infoboxCheck: " + infoC);
	}

}
