package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import com.fasterxml.jackson.core.JsonGenerationException;
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
	private List<String> infoChecks = new ArrayList<>();
	private List<String> contentChecks = new ArrayList<>();
	private List<String> articles = new ArrayList<>();
	private LexicalizedParser lp;
	private TokenizerFactory<CoreLabel> tokenizerFactory;
	private GrammaticalStructureFactory gsf;
	static MyLogger l = new MyLogger("logs/", "articleCheck");

	public List<String> getTextChecks() {
		return contentChecks;
	}

	public static List<String> getTextChecks(Dataset ds)
			throws JsonGenerationException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = new File("content.json");
		ObjectMapper mapper = new ObjectMapper();
		List<String> result = new ArrayList<>();
		if (!json.exists()) {
			ArticleCheckManager acm = new ArticleCheckManager();
			acm.checkArticles(ds);
		} else {
			l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(json, new TypeReference<List<String>>() {
		});
		return result;
	}

	public List<String> getInfoboxChecks() {
		return infoChecks;
	}

	public static List<String> getInfoboxChecks(Dataset ds)
			throws JsonParseException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = new File("info.json");
		ObjectMapper mapper = new ObjectMapper();
		List<String> result = new ArrayList<>();
		if (!json.exists()) {
			ArticleCheckManager acm = new ArticleCheckManager();
			acm.checkArticles(ds);
		} else {
			l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(json, new TypeReference<List<String>>() {
		});
		return result;
	}

	public List<String> getArticles() {
		return articles;
	}

	public static List<String> getArticles(Dataset ds) throws JsonParseException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = new File("all.json");
		ObjectMapper mapper = new ObjectMapper();
		List<String> result = new ArrayList<>();
		if (!json.exists()) {
			ArticleCheckManager acm = new ArticleCheckManager();
			acm.checkArticles(ds);
		} else {
			l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(json, new TypeReference<List<String>>() {
		});
		return result;
	}

	public void setInfoChecks(List<String> infoChecks) {
		this.infoChecks = infoChecks;
	}

	public void addArticles(String name) {
		this.articles.add(name);
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

		File info = new File("info.json");
		File content = new File("content.json");
		File all = new File("all.json");
		ObjectMapper mapper = new ObjectMapper();
		try {
			mapper.writeValue(info, this.infoChecks);
			mapper.writeValue(content, this.contentChecks);
			mapper.writeValue(all, this.articles);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		this.l.logDate("Write infobox checks to " + info.getPath());
		this.l.logDate("Write content checks to " + content.getPath());
		this.l.logDate("Write article checks to " + all.getPath());
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
		ObjectMapper mapper = new ObjectMapper();
		try {
			mapper.writeValue(new File("test.json"), acm.articles);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
