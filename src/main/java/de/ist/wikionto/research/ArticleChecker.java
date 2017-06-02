package de.ist.wikionto.research;

import java.io.IOException;
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

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.triplestore.query.QueryUtil;
import edu.stanford.nlp.ling.CoreLabel;
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

public class ArticleChecker {
	static MyLogger l = new MyLogger("logs/", "test");

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

	public static boolean checkText(String first) {
		Set<String> langs = new HashSet<>();
		langs.add("language");
		langs.add("dsl");
		List<TypedDependency> tdl;
		tdl = stanford(first.replaceAll("\\(.*?\\)", ""));
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
				if (cop.gov().originalText().contains(lang))
					return true;
				for (TypedDependency nmod : nmods) {
					if (nmod.gov().equals(cop.gov()))
						if (nmod.dep().originalText().contains(lang))
							return true;

				}
			}

		}

		return false;
	}

	static List<TypedDependency> stanford(String text) {
		String parserModel = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		LexicalizedParser lp = LexicalizedParser.loadModel(parserModel);
		TokenizerFactory<CoreLabel> tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
		TreebankLanguagePack tlp = lp.treebankLanguagePack();
		GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
		Tokenizer<CoreLabel> tok = tokenizerFactory.getTokenizer(new StringReader(text));
		List<CoreLabel> rawWords2 = tok.tokenize();
		Tree parse = lp.apply(rawWords2);
		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
		return tdl;
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

	public static void main(String[] args) {
		String parserModel = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		LexicalizedParser lp = LexicalizedParser.loadModel(parserModel);
		String sent2 = "Ada is a structured, statically typed, imperative, wide-spectrum, and object-oriented high-level computer programming language, extended from Pascal and other languages. It has built-in language support for design-by-contract, extremely strong typing, explicit concurrency, offering tasks, synchronous message passing, protected objects, and non-determinism. Ada improves code safety and maintainability by using the compiler to find errors in favor of runtime errors. Ada is an international standard; the current version (known as Ada 2012[7]) is defined by ISO/IEC 8652:2012.[8]";
		TokenizerFactory<CoreLabel> tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
		Tokenizer<CoreLabel> tok = tokenizerFactory.getTokenizer(new StringReader(sent2));
		List<CoreLabel> rawWords2 = tok.tokenize();
		Tree parse = lp.apply(rawWords2);

		TreebankLanguagePack tlp = lp.treebankLanguagePack(); // PennTreebankLanguagePack
																// for English
		GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
		for (TypedDependency td : tdl) {
			if (td.reln().getShortName().equals("cop"))
				System.out.println(td.gov());
			System.out.println(td.gov() + " depends on " + td.dep() + " by using " + td.reln());
		}

		String text = "Ada is a structured, statically typed, imperative, wide-spectrum, and object-oriented high-level computer programming language, extended from Pascal and other languages. It has built-in language support for design-by-contract, extremely strong typing, explicit concurrency, offering tasks, synchronous message passing, protected objects, and non-determinism. Ada improves code safety and maintainability by using the compiler to find errors in favor of runtime errors. Ada is an international standard; the current version (known as Ada 2012[7]) is defined by ISO/IEC 8652:2012.[8]";
		Pattern a = Pattern.compile("\\(.*?\\)");
		Matcher b = a.matcher(text);
		text = text.replaceAll("\\(.*?\\)", "");
		System.out.println(checkText(text));
	}

	public static void main2(String[] args) throws IOException {
		Dataset set = TDBFactory.createDataset("Computer_languages");
		ResultSet rs = QueryUtil.executeQuery(set, "/sparql/queries/getEponymousInstances.sparql");
		QuerySolution qs;
		String text = null;
		String title;
		String first;

		while (rs.hasNext()) {
			qs = rs.next();
			text = qs.get("?text").asLiteral().getString();
			title = qs.get("?name").asLiteral().getString();
			first = qs.get("?first").asLiteral().getString();
			l.logLn(title + ": " + checkText(first));
		}
	}

}
