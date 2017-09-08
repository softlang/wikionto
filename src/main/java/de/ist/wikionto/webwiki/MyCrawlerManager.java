/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki;

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
	private int maxDepth;
	private Set<String> exclusionset;
	private Set<String> stubs;
	private int threadcounter;

	public MyCrawlerManager(String root, Set<String> excludedCategories) {
		rootname = root;
		exclusionset = excludedCategories;
		classifierQueue = new ConcurrentLinkedQueue<>();
		classifierMap = Collections.synchronizedMap(new HashMap<String, Classifier>());
		instanceMap = Collections.synchronizedMap(new HashMap<String, Instance>());
	}

	public void start(int maxDepth) {
		initialize(rootname, maxDepth);
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

	private void initialize(String name, int maxDepth) {
		this.maxDepth = maxDepth;
		root = new Classifier();
		root.setName(name);
		classifierMap.put(name, root);
		offerClassifier(root);
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
		
		// new exclusion criteria
//		exclusionset.add("Programming languages created in");
		
//		stubs.add("Programming language topic stubs");
//		stubs.add("Markup language stubs");

		
		MyCrawlerManager a = new MyCrawlerManager("Computer languages", exclusionset);
		a.start(5);
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

	public boolean isExcludedCategoryNamew2(String name) {
		boolean result = false;
		for (String ex : exclusionset) {
			if (name.contains(ex)) {
				result = true;
				break;
			}
		}
		return result;
	}
	
	public boolean isExcludedCategoryName(String name) {
		return exclusionset.stream().anyMatch(name::contains);
	}
	
	public boolean isStubCategory(String name) {
		return name.contains("stubs");
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

	public int getMaxDepth() {
		return maxDepth;
	}
}
