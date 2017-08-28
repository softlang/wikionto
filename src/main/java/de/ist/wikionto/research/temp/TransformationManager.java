package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.research.MyLogger;

public class TransformationManager {
	private Map<String, Boolean> relevant = new HashMap<>();
	private List<String> seed = new ArrayList<String>();
	private List<String> textC = new ArrayList<String>();
	private List<String> infoboxC = new ArrayList<String>();
	private List<String> articles = new ArrayList<String>();
	private List<Transformation> transList = new LinkedList<>();
	private String storeName = "Computer_languages";
	private Dataset store;
	private Dataset oldStore;

	private MyLogger log = new MyLogger("logs/", "Result");

	// MyLogger log = new MyLogger("logs/", "Transformation");

	public void transform() {
		System.out.println("Start pipeline at " + new Date().toString());
		log.logDate("Start pipeline");
		// open base store
		this.relevant = new HashMap<>();
		store = TDBFactory.createDataset(storeName);
		oldStore = store;
		// get check lists
		try {
			this.articles = ArticleCheckManager.getArticles(store);
			this.infoboxC = ArticleCheckManager.getInfoboxChecks(store);
			this.textC = ArticleCheckManager.getTextChecks(store);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		articles.forEach(x -> relevant.put(x, false));
		// Seed-Based
		SeedAnnotation sa = new SeedAnnotation(this);
		sa.annotate();
		// Hypernym
		HypernymAnnotation ha = new HypernymAnnotation(this);
		ha.annotate();
		// Eponymous
		EponymousTransformation et = new EponymousTransformation(this);
		et.transform();
		// Semantically Distant
		SemanticallyDistanstAnnotation sda = new SemanticallyDistanstAnnotation(this);
		sda.annotate();
		ChildrenBased cb = new ChildrenBased(this);
		cb.annotate();
		List<String> base = relevant.keySet().stream().filter(relevant::get).sorted().collect(Collectors.toList());
		base.stream().forEach(log::logLn);
		log.logLn("Total number of relevant articles: " + base.stream().count());
		System.out.println("Finish pipeline at " + new Date().toString());
		log.logDate("Finish pipeline");

	}

	public void createNewDatasetName(String transName, String setName) {
		String newName = setName + "_" + transName;
		File oldDir = new File("./" + setName);
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
		this.oldStore = store;
		this.store = TDBFactory.createDataset(newName);
		this.storeName = newName;
	}

	public static void main(String[] args) {
		TransformationManager tm = new TransformationManager();
//		tm.transList.add(new Hypernym(tm));
//		tm.transList.add(new EponymousTransformation(tm));
//		tm.transList.add(new SemanticallyDistanst(tm));
//		tm.transList.add(new ChildrenBased(tm));
		tm.transform();
	}

	public Dataset getOldStore() {
		return oldStore;
	}

	public void setOldStore(Dataset oldStore) {
		this.oldStore = oldStore;
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

	public Boolean putInRelevant(String arg0, Boolean arg1) {
		return relevant.put(arg0, arg1);
	}

	public Boolean getFromRelevant(String key) {
		return relevant.get(key);
	}

}
