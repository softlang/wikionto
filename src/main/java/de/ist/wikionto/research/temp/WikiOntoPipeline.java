package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class WikiOntoPipeline {
	private Map<String, Boolean> relevantArticles = new HashMap<>();
	private Map<String, Boolean> relevantCategories = new HashMap<>();
	private Map<String, Set<Annotation>> articleAnnotations = new HashMap<>();
	private Map<String, Set<Annotation>> categoryAnnotations = new HashMap<>();
	private List<String> seed = new ArrayList<String>();
	private List<String> textC = new ArrayList<String>();
	private List<String> infoboxC = new ArrayList<String>();
	private List<String> articles = new ArrayList<String>();
//	private List<Transformation> transList = new LinkedList<>();
	private String storeName = "Computer_languages";
	private Dataset store;
	private Dataset sourceStore;

	private MyLogger log = new MyLogger("logs/", "Result");

	public static void main(String[] args) {
		WikiOntoPipeline tm = new WikiOntoPipeline();
		tm.executePipeline();
	}
	
	public void executePipeline() {
		System.out.println("Start pipeline at " + new Date().toString());
		log.logDate("Start pipeline");
		// open base store
		this.relevantArticles = new HashMap<>();
		sourceStore = TDBFactory.createDataset(storeName);
		store = createNewDataset(storeName + "_Pipeline", storeName);
		// get check lists
		try {
			this.articles = NewArticleCheckManager.getArticles(store);
			this.infoboxC = NewArticleCheckManager.getInfoboxChecks(store);
			this.textC = NewArticleCheckManager.getTextChecks(store);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		articles.forEach(x -> relevantArticles.put(x, false));
		// Seed-Based
		SeedAnnotator sa = new SeedAnnotator(this);
		sa.execute();
		// Hypernym
		HypernymAnnotator ha = new HypernymAnnotator(this);
		ha.execute();
		// Eponymous
		EponymousTransformation et = new EponymousTransformation(this);
		et.execute();
		// Semantically Distant
		SemanticallyDistanstAnnotator sda = new SemanticallyDistanstAnnotator(this);
		sda.execute();
		// Children-based Category
		ChildrenBasedAnnotator cb = new ChildrenBasedAnnotator(this);
		cb.execute();
		RelevantArticlesTransformation aa = new RelevantArticlesTransformation(this);
		aa.execute();
		// Clean up
		CleanUp cu = new CleanUp(this);
		cu.execute();
		
		List<String> base = QueryUtil.getReachableClassifiers(this.getStore()).stream()
				.filter(this::getFromRelevantCategories)
				.collect(Collectors.toList());
		
		log.logLn("Total number of relevant categories: " + base.stream().count() + "\n\n");
		log.logLn("Reachable categories: ");
		base.stream().sorted().forEach(log::logLn);
		
		base = QueryUtil.getReachableArticles(this.getStore()).stream()
				.filter(this::getFromRelevantArticles)
				.collect(Collectors.toList());
		log.logLn("Total number of relevant articles: " + base.stream().count());
		log.logLn("Reachable articles: ");
		base.stream().sorted().forEach(log::logLn);
		System.out.println("Finish pipeline at " + new Date().toString());
		log.logDate("Finish pipeline");
		log.close();
		Annotation.log.logLn("Article name: Annotations");
		articleAnnotations.forEach((x,y) -> {
			Annotation.log.log(x + ": ");
			String s = String.join(", ", y.stream().map(Annotation::toString).collect(Collectors.toList()));
			Annotation.log.logLn(s);
		});
	}

	public Dataset createNewDataset(String newName, String oldName) {
		File oldDir = new File("./" + oldName);
		File newDir = new File("./" + newName);
		try {
			if (newDir.exists()) {
				FileUtils.cleanDirectory(newDir);
			} else {
				if (!newDir.mkdirs())
					System.err.println("Failed to create directory: " + newDir.getPath());
			}
			FileUtils.copyDirectory(oldDir, newDir);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.storeName = newName;
		return TDBFactory.createDataset(newName);
	}

	public Dataset getSourceStore() {
		return sourceStore;
	}

	public void setSourceStore(Dataset oldStore) {
		this.sourceStore = oldStore;
	}

	public String getStoreName() {
		return storeName;
	}

	public void setStoreName(String storeName) {
		this.storeName = storeName;
	}

	public Dataset getStore() {
		return store;
	}

	public void setStore(Dataset store) {
		this.store = store;
	}

	public List<String> getArticles() {
		return articles;
	}

	public void setArticleChecks(List<String> articles) {
		this.articles = articles;
	}

	public List<String> getSeed() {
		return seed;
	}

	public void setSeed(List<String> seed) {
		this.seed = seed;
	}

	public List<String> getTextC() {
		return textC;
	}

	public void setTextC(List<String> textC) {
		this.textC = textC;
	}

	public List<String> getInfoboxC() {
		return infoboxC;
	}

	public void setInfoboxC(List<String> infoboxC) {
		this.infoboxC = infoboxC;
	}

	public Set<String> keySetFromRelevantArticles(){
		return this.relevantArticles.keySet();
	}
	
	public Boolean putInRelevantArticles(String arg0, Boolean arg1) {
		return relevantArticles.put(arg0, arg1);
	}	

	public Boolean getFromRelevantArticles(String key) {
		if (relevantArticles.containsKey(key))
			return relevantArticles.get(key);
		else
			return false;
	}
	
	public Set<String> keySetFromRelevantCategories(){
		return this.relevantCategories.keySet();
	}

	public Boolean putInRelevantCategories(String arg0, Boolean arg1) {
		return relevantCategories.put(arg0, arg1);
	}

	public Boolean getFromRelevantCategories(String key) {
		if (relevantCategories.containsKey(key))
			return relevantCategories.get(key);
		else
			return false;
	}
	
	public Boolean addArticleAnnotation(String article,Annotation annotation){
		if (!articleAnnotations.containsKey(article))
			articleAnnotations.put(article, new HashSet<>());
		return articleAnnotations.get(article).add(annotation);
	}
	
	public Boolean addCategoryAnnotation(String cat,Annotation annotation){
		if (!categoryAnnotations.containsKey(cat))
			categoryAnnotations.put(cat, new HashSet<>());
		return categoryAnnotations.get(cat).add(annotation);
	}

	public boolean removeArticleAnnotation(String article, Annotation anno) {
		if (!articleAnnotations.containsKey(article))
			articleAnnotations.put(article, new HashSet<>());
		return articleAnnotations.get(article).remove(anno);
		
	}
	
	public boolean removeArticleCategory(String cat, Annotation anno) {
		if (!categoryAnnotations.containsKey(cat))
			categoryAnnotations.put(cat, new HashSet<>());
		return categoryAnnotations.get(cat).remove(anno);
	}

}
