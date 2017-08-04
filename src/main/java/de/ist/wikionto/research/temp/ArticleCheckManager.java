package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.research.MyLogger;
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

public class ArticleCheckManager {
	private String queryPath = "/sparql/queries/getAllReachableArticlesWithText.sparql";
	private Map<String, Boolean> articleChecks = new HashMap<String, Boolean>();
	private LexicalizedParser lp;
	private TokenizerFactory<CoreLabel> tokenizerFactory;
	private GrammaticalStructureFactory gsf;
	MyLogger l = new MyLogger("logs/", "articleCheck");

	public void putArticleCheck(String name, Boolean check) {
		this.articleChecks.put(name, check);
	}

	public Map<String, Boolean> getArticleChecks() {
		return articleChecks;
	}

	public Map<String, Boolean> getArticleChecks(Dataset ds)
			throws JsonParseException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = new File("test.json");
		ObjectMapper mapper = new ObjectMapper();
		Map<String, Boolean> result = new HashMap<>();
		if (!json.exists()) {
			this.checkArticles(ds);
			mapper.writeValue(json, this.articleChecks);
			this.l.logDate("Write article checks to " + json.getPath());
		} else {
			this.l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(new File("test.json"), new TypeReference<Map<String, Boolean>>() {
		});
		return result;
	}

	public ArticleCheckManager(String queryPath) {
		String parserModel1 = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		String parserModel2 = "edu/stanford/nlp/models/lexparser/englishFactored.ser.gz";
		lp = LexicalizedParser.loadModel(parserModel1);
		tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
		TreebankLanguagePack tlp = lp.treebankLanguagePack();
		gsf = tlp.grammaticalStructureFactory();
		this.queryPath = queryPath;
	}

	public ArticleCheckManager() {
		String parserModel1 = "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz";
		String parserModel2 = "edu/stanford/nlp/models/lexparser/englishFactored.ser.gz";
		lp = LexicalizedParser.loadModel(parserModel1);
		tokenizerFactory = PTBTokenizer.factory(new CoreLabelTokenFactory(), "");
		TreebankLanguagePack tlp = lp.treebankLanguagePack();
		gsf = tlp.grammaticalStructureFactory();
	}

	public void checkArticles(Dataset ds) {
		l.logDate("Start article checking");
		ResultSet rs = query(ds);
		int threads = Runtime.getRuntime().availableProcessors() * 2;
		ExecutorService es = Executors.newFixedThreadPool(threads);
		int i = 0;
		rs.forEachRemaining(x -> {
			es.execute(new ArticleChecker(x, this));
		});
		es.shutdown();
		while (true)
			if (es.isTerminated())
				break;
		l.logDate("Finish Article Checking");
	}

	public ResultSet query(Dataset dataset) {
		ResultSet rs = QueryUtil.executeQuery(dataset, queryPath);
		return rs;
	}

	public List<TypedDependency> stanford(String text) {
		Tokenizer<CoreLabel> tok = tokenizerFactory.getTokenizer(new StringReader(text));
		List<CoreLabel> rawWords2 = tok.tokenize();
		Tree parse = lp.apply(rawWords2);
		GrammaticalStructure gs = gsf.newGrammaticalStructure(parse);
		List<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
		return tdl;
	}

	public static void main(String[] args) {
		Dataset dataset = TDBFactory.createDataset("Computer_languages");
		ArticleCheckManager acm = new ArticleCheckManager();
		acm.checkArticles(dataset);
		HashMap<String, Boolean> a = new HashMap<>();
		a.put("a", true);
		a.put("b", false);
		a.put("c", false);
		Map<String, Boolean> b = new HashMap<>();
		ObjectMapper mapper = new ObjectMapper();
		try {
			mapper.writeValue(new File("test.json"), acm.articleChecks);
			b = mapper.readValue(new File("test.json"), new TypeReference<Map<String, Boolean>>() {
			});
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		b.forEach((x, y) -> {
			System.out.println(x + " : " + y);
		});
	}

}
