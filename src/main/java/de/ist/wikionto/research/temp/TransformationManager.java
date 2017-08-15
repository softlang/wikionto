package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.research.MyLogger;

public class TransformationManager {
	private Map<String, Boolean> relevant;
	private List<String> seed;
	private List<Transformation> transList = new LinkedList<>();
	private String storeName = "Computer_languages";
	private Dataset store;
	private Dataset oldStore;
	private Map<String, Boolean> articleChecks;
	private int threadcounter;
	private MyLogger log = new MyLogger("logs/", "Result");

	// MyLogger log = new MyLogger("logs/", "Transformation");

	public void transform() {
		// open base store
		setRelevant(new HashMap());
		store = TDBFactory.createDataset(storeName);
		oldStore = store;
		// Seed-Based
		this.setSeed(GitSeed.readLanguages());
		// Hypernym
		try {
			this.articleChecks = new ArticleCheckManager().getArticleChecks(store);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

		for (Transformation t : transList) {
			System.out.println("Start " + t.name);
			// prepare new store
			storeName = newDatasetName(t.name, storeName);
			oldStore = store;

			store = TDBFactory.createDataset(storeName);
			t.log.logDate("Write transformation " + t.name + " to store " + storeName);

			// perform transformation
			t.transform();

			System.out.println("Finish checking at " + new Date().toString());
			t.log.logDate("Finish Transformation " + t.name);

		}
		relevant.keySet().stream().filter(relevant::get).forEach(log::logLn);

	}

	public String newDatasetName(String transName, String setName) {
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
		return newName;
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

	public Map<String, Boolean> getArticleChecks() {
		return articleChecks;
	}

	public void setArticleChecks(Map<String, Boolean> articleChecks) {
		this.articleChecks = articleChecks;
	}

	public synchronized void incthreadcounter() {
		threadcounter++;
	}

	public synchronized void decthreadcounter() {
		threadcounter--;
	}

	public static void main(String[] args) {
		TransformationManager tm = new TransformationManager();
		tm.transList.add(new Hypernym(tm));
		tm.transList.add(new EponymousTransformation(tm));
		tm.transList.add(new SemanticallyDistanst(tm));
		tm.transList.add(new ChildrenBased(tm));
		tm.transform();

	}

	public Map<String, Boolean> getRelevant() {
		return relevant;
	}

	public void setRelevant(Map<String, Boolean> relevant) {
		this.relevant = relevant;
	}

	public List<String> getSeed() {
		return seed;
	}

	public void setSeed(List<String> seed) {
		this.seed = seed;
	}

}
