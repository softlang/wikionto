package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Properties;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import com.fasterxml.jackson.core.JsonGenerationException;
import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.IndexedWord;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.BasicDependenciesAnnotation;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.EnhancedPlusPlusDependenciesAnnotation;
import edu.stanford.nlp.semgraph.SemanticGraphEdge;
import edu.stanford.nlp.util.CoreMap;

public class NewArticleCheckManager{
	private String queryPath = "/sparql/queries/getAllReachableArticlesWithText.sparql";
	private List<String> infoCboxChecks = new ArrayList<>();
	private List<String> textChecks = new ArrayList<>();
	private List<String> articles = new ArrayList<>();
	private List<String> languages = new ArrayList<>();
	private List<String> dialects = new ArrayList<>();
	private List<String> formats = new ArrayList<>();
	
	private Map<String,String> keywords = new HashMap<>();
	
	static MyLogger l = new MyLogger("logs/", "newArticleCheck");
	
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
	
	private StanfordCoreNLP pipeline = null;
	
	static File infoFile = new File("newinfo.json");
	static File contentFile = new File("newcontent.json");
	static File articlesFile = new File("newall.json");
	
	public NewArticleCheckManager(){
		super();
	}
	
	public boolean addTextCheck(String title){
		return this.textChecks.add(title);
	}
	
	public boolean addLanguage(String title){
		return this.languages.add(title);
	}
	
	public boolean addFormat(String title){
		return this.formats.add(title);
	}
	
	public boolean addDialect(String title){
		return this.dialects.add(title);
	}
	
	public boolean addArticle(String title){
		return this.articles.add(title);
	}
	
	public boolean addInfoboxCheck(String title){
		return this.infoCboxChecks.add(title);
	}

	public List<String> getTextChecks() {
		return textChecks;
	}
	
	public static List<String> getTextChecks(Dataset ds)
			throws JsonGenerationException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = contentFile;
		ObjectMapper mapper = new ObjectMapper();
		List<String> result = new ArrayList<>();
		if (!json.exists()) {
			NewArticleCheckManager acm = new NewArticleCheckManager();
			acm.checkArticles(ds);
		} else {
			l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(json, new TypeReference<List<String>>() {});
		return result;
	}

	public List<String> getInfoboxChecks() {
		return infoCboxChecks;
	}

	public static List<String> getInfoboxChecks(Dataset ds)
			throws JsonParseException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = infoFile;
		ObjectMapper mapper = new ObjectMapper();
		List<String> result = new ArrayList<>();
		if (!json.exists()) {
			NewArticleCheckManager acm = new NewArticleCheckManager();
			acm.checkArticles(ds);
		} else {
			l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(json, new TypeReference<List<String>>() {});
		return result;
	}

	public List<String> getArticles() {
		return articles;
	}

	public static List<String> getArticles(Dataset ds) throws JsonParseException, JsonMappingException, IOException {
		// TODO: Add time stamp check
		File json = articlesFile;
		ObjectMapper mapper = new ObjectMapper();
		List<String> result = new ArrayList<>();
		if (!json.exists()) {
			NewArticleCheckManager acm = new NewArticleCheckManager();
			acm.checkArticles(ds);
		} else {
			l.logDate("Read article checks from " + json.getPath());
		}
		result = mapper.readValue(json, new TypeReference<List<String>>() {});
		return result;
	}
	
	public boolean checkTitle(String title) {
		return title.contains("language");
	}

	public boolean checkInfobox(String text) {
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
			this.addArticle(this.title);
			this.addInfoboxCheck(this.title);
			this.addFormat(this.title);
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
		}
		return result;
	}
	
	public boolean checkContent(String text){
		return stanford(text, this.pipeline);
	}

	public boolean stanford(String text, StanfordCoreNLP pipeline){
		Annotation doc = new Annotation(text.toLowerCase());
		pipeline.annotate(doc);
		List<CoreMap> sentences = doc.get(SentencesAnnotation.class);
		if (sentences.size() <= 0) {
			return false;
		}
		CoreMap sentence = doc.get(SentencesAnnotation.class).get(0);
		SemanticGraph sg = sentence.get(BasicDependenciesAnnotation.class);
		Boolean result = false;
		
		List<IndexedWord> cops = sg.edgeListSorted()
			.stream()
			.filter(edge -> {
				String name = edge.getRelation().getShortName();
				return name.contains("cop");
			})
			.map(SemanticGraphEdge::getGovernor)
			.collect(Collectors.toList());
		
		List<IndexedWord> langs = sg.getAllNodesByWordPattern("(languages?)|(formats?)|(dsls?)|(dialects?)");

		for(IndexedWord cop : cops){
			if (result){
				break;
			}
			result = hasPath(sg, cop, langs);
			
		}
		return result;
	}
	
	public boolean hasPath(SemanticGraph graph, IndexedWord source, List<IndexedWord> langs){
		boolean result = false;
		if (langs.contains(source)){
			this.keyword = source.originalText();
			return true;
		}
		List<IndexedWord> nmods = graph.outgoingEdgeList(source)
			.stream()
			.filter(edge -> edge.getRelation().getShortName().contains("nmod"))
			.map(edge -> {
				return edge.getDependent();
				})
			.collect(Collectors.toList());
		if (nmods.isEmpty())
			return false;
		else
			return nmods.stream().anyMatch(nmod -> hasPath(graph, nmod, langs));
	}

	
	public void checkArticles(Dataset ds) {
		l.logDate("Start article checking");
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,depparse");
		pipeline = new StanfordCoreNLP(props);
		ResultSet resultSet = QueryUtil.executeQuery(ds, queryPath);
		
		resultSet.forEachRemaining(qs -> {
			String text = qs.get("?t").asLiteral().getString();
			String title = qs.get("?n").asLiteral().getString();
			String first = qs.get("?f").asLiteral().getString();
			this.title = title;
			this.keyword = null;
			this.infoCheck = this.checkInfobox(text);
			this.textCheck = this.checkContent(first);
			this.addArticle(title);
			if (infoCheck)
				this.addInfoboxCheck(title);
			if (textCheck)
				this.addTextCheck(title);
			if (this.keyword != null)
				if (this.keyword.contains("language"))
					this.addLanguage(title);
				else
					if (this.keyword.contains("format"))
						this.addFormat(title);
					else
						if (this.keyword.contains("dialect"))
							this.addLanguage(title);
						else
							if (this.keyword.contains("dsl"))
								this.addLanguage(title);
			NewArticleCheckManager.l.logLn(
					this.title + ": " + this.keyword 
					+ "\n  Content Check: " + textCheck
					+ "\n  Infobox Check: " + infoCheck);
		});
		
		ObjectMapper mapper = new ObjectMapper();
		try {
			mapper.writeValue(NewArticleCheckManager.infoFile, this.infoCboxChecks);
			mapper.writeValue(NewArticleCheckManager.contentFile, this.textChecks);
			mapper.writeValue(NewArticleCheckManager.articlesFile, this.articles);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		l.logDate("Write infobox checks to " + NewArticleCheckManager.infoFile.getPath());
		l.logDate("Write content checks to " + NewArticleCheckManager.contentFile.getPath());
		l.logDate("Write article checks to " + NewArticleCheckManager.articlesFile.getPath());
		l.logDate("Finish Article Checking");
	}

	
	
	
	
	
	


}
