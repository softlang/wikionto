package de.ist.wikionto.research;

import java.io.StringReader;
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
import edu.stanford.nlp.process.CoreLabelTokenFactory;
import edu.stanford.nlp.process.PTBTokenizer;
import edu.stanford.nlp.process.Tokenizer;
import edu.stanford.nlp.process.TokenizerFactory;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.TypedDependency;

public abstract class ArticleChecker extends Transformation {
	LexicalizedParser lp;
	TokenizerFactory<CoreLabel> tokenizerFactory;
	GrammaticalStructureFactory gsf;

	public ArticleChecker(TransformationManager tm, List<QuerySolution> qss) {
		super(tm, qss);
		String parserModel1 = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		String parserModel2 = "edu/stanford/nlp/models/lexparser/englishFactored.ser.gz";
		lp = LexicalizedParser.loadModel(parserModel1);
		tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
		TreebankLanguagePack tlp = lp.treebankLanguagePack();
		gsf = tlp.grammaticalStructureFactory();
		// TODO Auto-generated constructor stub
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
			Matcher m = paradigm.matcher(e.text());
			result = result || m.find();
			m = influenced.matcher(e.text());
			result = result || m.find();
			m = typing.matcher(e.text());
			result = result || m.find();
			m = language.matcher(e.text());
			result = result || m.find();
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
		// l.logLn(text);
		tdl = stanford(text);
		List<TypedDependency> nmods = new ArrayList<>();
		List<TypedDependency> cops = new ArrayList<>();
		for (TypedDependency td : tdl) {
			if (td.reln().getShortName().equals("cop")) {
				cops.add(td);
			}
			if (td.reln().getShortName().contains("nmod")) {
				nmods.add(td);
			}
		}
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

	protected List<TypedDependency> stanford(String text) {
		Tokenizer<CoreLabel> tok = tokenizerFactory.getTokenizer(new StringReader(text));
		List<CoreLabel> rawWords2 = tok.tokenize();
		Tree parse = lp.apply(rawWords2);
		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
		return tdl;
	}

	private String getFirstSentence(String html) {
		Document doc = Jsoup.parse(html);
		Elements es = doc.select("div.mw-parser-output");
		for (Element e : es) {
			Elements childs = e.children();
			for (Element child : childs) {
				if (child.select("img").isEmpty() && child.select("table").isEmpty() && !child.is("div.hatnote")
						&& !child.is("div.noprint") && !child.is("dl"))
					return child.text();
			}
		}
		return "";
	}

}
