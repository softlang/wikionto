/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki;

import java.io.File;
import java.io.IOException;
import java.util.Collections;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Queue;
import java.util.Set;
import java.util.concurrent.ConcurrentLinkedQueue;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.commons.io.FileUtils;

import de.ist.wikionto.triplestore.WikiTaxToJenaTDB;
import de.ist.wikionto.webwiki.model.Classifier;
import de.ist.wikionto.webwiki.model.Instance;

/**
 * Uses Wikipedia API to access Wikipedia categories, entities and their
 * infoboxes
 *
 * @author Marcel
 */
public class MyCrawlerManager {

	private String rootname;
	private Classifier root;
	private final Map<String, Classifier> classifierMap;
	private final Queue<Classifier> classifierQueue;
	private final Map<String, Instance> instanceMap;
	private Set<String> exclusionset;
	private int threadcounter;

	public MyCrawlerManager(String root, Set<String> excludedCategories) {
		rootname = root;
		exclusionset = excludedCategories;
		classifierQueue = new ConcurrentLinkedQueue<>();
		classifierMap = Collections.synchronizedMap(new HashMap<String, Classifier>());
		instanceMap = Collections.synchronizedMap(new HashMap<String, Instance>());
	}

	public void start(int maxDepth) {
		initialize(rootname);
		threadcounter = 0;
		crawl();
		WikiTaxToJenaTDB.createTripleStore(classifierMap.values(), instanceMap.values(), root);
		// WikiTaxToJenaTDB2.createTripleStore(classifierMap, instanceMap,
		// rootname);
	}

	public void crawl() {
		int threadnr = Runtime.getRuntime().availableProcessors() * 4;
		System.out.println("Starting with " + threadnr + " threads!");
		ExecutorService executor = Executors.newFixedThreadPool(threadnr);
		while (true) {

			if (!classifierQueue.isEmpty()) {
				incthreadcounter();
				executor.execute(new CategoryCrawler(this, popClassifier()));
			} else {
				if (threadcounter == 0) {
					System.out.println("Finished crawl at #C:" + classifierMap.size() + ", #I:" + instanceMap.size());
					System.out.println(new Date().toString());
					break;
				}
			}
		}

		executor.shutdown();
		while (!executor.isTerminated() && !executor.isShutdown()) {
			System.out.println("Awaiting termination");
		}
	}

	private void initialize(String name) {
		root = new Classifier();
		root.setName(name);
		offerClassifier(root);
		File dir = new File("./" + name.replaceAll(" ", ""));
		if (dir.exists()) {
			try {
				FileUtils.cleanDirectory(dir);
			} catch (IOException ex) {
				Logger.getLogger(WikiTaxToJenaTDB.class.getName()).log(Level.SEVERE, null, ex);
			}
		} else {
			boolean success = dir.mkdirs();
			if (!success) {
				System.err.println("Creating target directory failed");
				System.exit(0);
			}
		}

	}

	public static void main(String[] args0) {
		Set<String> exclusionset = new HashSet<>();
		exclusionset.add("Data types");
		exclusionset.add("Programming language topics");
		exclusionset.add("Web services");
		exclusionset.add("User BASIC");
		exclusionset.add("Lists of computer languages");
		exclusionset.add("Programming languages by creation date");
		exclusionset.add("Uncategorized programming languages");
		exclusionset.add("Wikipedia");
		exclusionset.add("Articles");
		exclusionset.add("software");
		exclusionset.add("Software that");
		exclusionset.add("Software for");
		exclusionset.add("Software programmed");
		exclusionset.add("Software written");
		exclusionset.add("Software by");
		exclusionset.add("conference");
		MyCrawlerManager a = new MyCrawlerManager("Computer languages", exclusionset);
		a.start(10);
		// System.out.println("Java : " + a.instanceMap.containsKey("Java
		// (programming language)"));
		// System.out.println(a.instanceMap.get("Java (programming
		// language)").getLinks().toString());
		// System.out.println("C : " + a.instanceMap.containsKey("C (programming
		// language)"));
		// System.out.println(a.instanceMap.get("C (programming
		// language)").getLinks().toString());
		// System.out.println("Haskell : " + a.instanceMap.containsKey("Haskell
		// (programming language)"));
		// System.out.println(a.instanceMap.get("Haskell (programming
		// language)").getLinks().toString());

	}

	public void offerClassifier(Classifier classifier) {
		if (classifierMap.size() % 100 == 0) {
			System.out.println("#C:" + classifierMap.size() + ", #I:" + instanceMap.size());
			System.out.println(new Date().toString());
		}
		classifierQueue.offer(classifier);
	}

	public Classifier popClassifier() {
		return classifierQueue.poll();
	}

	public Classifier getClassifierFromClassifierMap(String name) {
		return classifierMap.get(name);
	}

	public void putInClassifierMap(String name, Classifier classifier) {
		classifierMap.put(name, classifier);
	}

	public Instance getInstanceFromInstanceMap(String name) {
		return instanceMap.get(name);
	}

	public void putInInstanceMap(String name, Instance instance) {
		instanceMap.put(name, instance);
	}

	public boolean isExcludedCategoryName(String name) {
		boolean result = false;
		for (String ex : exclusionset) {
			if (name.contains(ex)) {
				result = true;
				break;
			}
		}
		return result;
	}

	public synchronized void incthreadcounter() {
		threadcounter++;
	}

	public synchronized void decthreadcounter() {
		threadcounter--;
	}

	public Classifier getRoot() {
		return root;
	}
}
