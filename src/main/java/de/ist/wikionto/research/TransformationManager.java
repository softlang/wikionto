package de.ist.wikionto.research;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

public class TransformationManager {
	List<Transformation> trans = new LinkedList<>();
	Map<String, Boolean> checks;
	private int threadcounter;
	MyLogger log = new MyLogger("logs/", "Transformation");

	public static void main(String[] args) {
		TransformationManager tm = new TransformationManager();
		tm.trans.add(new EponymousTransformation(tm, null));
		tm.transform();
	}

	public void transform() {
		String setName = "Computer_languages";
		int threadnr = Runtime.getRuntime().availableProcessors() * 1;
		threadnr = 32;
		System.out.println("Starting with " + threadnr + " threads!");
		log.logLn("Working with " + threadnr + " threads");
		ExecutorService executor = Executors.newFixedThreadPool(threadnr);
		for (Transformation t : trans) {
			checks = new HashMap<>();
			setName = newDataset(t.name, setName);
			log.logDate("Using " + t.name + " Transformation at database " + setName);
			Dataset set = TDBFactory.createDataset(setName);
			ResultSet rs = t.query(set);
			List<List<QuerySolution>> threads = splitSets(rs, threadnr);
			QuerySolution qs;
			for (List<QuerySolution> qss : threads) {
				incthreadcounter();
				executor.execute(t.newTransformation(this, qss));
				if (threadcounter == 0) {
					// System.out.println("Finished crawl at #C:" +
					// classifierMap.size() + ", #I:" + instanceMap.size());
					System.out.println("Finish transformation at " + new Date().toString());
					break;
				}
			}
		}
		executor.shutdown();
		while (true) {
			if (executor.isTerminated()) {
				System.out.println("Finish checking at " + new Date().toString());
				log.logDate("Finish ");
				break;
			}
		}

	}

	public String newDataset(String transName, String setName) {
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

	private List<List<QuerySolution>> splitSets(ResultSet rs, int threads) {
		List<List<QuerySolution>> result = new ArrayList<>();
		for (int i = 0; i < threads; i++)
			result.add(new ArrayList<>());
		int i = 0;
		QuerySolution qs;
		while (rs.hasNext()) {
			qs = rs.next();
			result.get(i % threads).add(qs);
			i++;
		}
		return result;
	}

	public synchronized void incthreadcounter() {
		threadcounter++;
	}

	public synchronized void decthreadcounter() {
		threadcounter--;
	}
}
