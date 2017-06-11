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

import com.hp.hpl.jena.graph.Graph;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ParameterizedSparqlString;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;
import com.hp.hpl.jena.update.UpdateAction;

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
		for (Transformation t : trans) {
			int threadnr = Runtime.getRuntime().availableProcessors() * 1;
			threadnr = 32;
			System.out.println("Starting with " + threadnr + " threads!");
			log.logLn("Working with " + threadnr + " threads");
			ExecutorService executor = Executors.newFixedThreadPool(threadnr);
			checks = new HashMap<>();
			setName = newDataset(t.name, setName);
			log.logDate("Using " + t.name + " Transformation at database " + setName);
			Dataset dataset = TDBFactory.createDataset(setName);
			ResultSet rs = t.query(dataset);
			List<List<QuerySolution>> threads = splitSets(rs, threadnr);
			QuerySolution qs;
			for (List<QuerySolution> qss : threads) {
				incthreadcounter();
				executor.execute(t.newTransformation(this, qss));
			}
			executor.shutdown();
			while (true) {
				if (executor.isTerminated()) {
					System.out.println("Finish checking at " + new Date().toString());
					log.logDate("Finish ");
					break;
				}
			}
			checks.forEach((x, y) -> t.transform(dataset, x, y));
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

	public long transformFile(Dataset dataset, String tfilename, Map<String, String> parameter) {
		File tfile = new File(System.getProperty("user.dir") + "/sparql/transformations/" + tfilename);
		String transformation = "";
		try {
			transformation = FileUtils.readFileToString(tfile);
		} catch (IOException ex) {
			System.err.println("Exception reading:" + tfilename);
			ex.printStackTrace();
			return 0;
		}
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		long size = graph.size();
		ParameterizedSparqlString pss = new ParameterizedSparqlString();
		pss.setCommandText(transformation);
		for (String key : parameter.keySet()) {
			String query = pss.asUpdate().toString();
			if (!parameter.get(key).contains("http://"))
				pss.setLiteral(key, parameter.get(key).trim());
			else
				pss.setIri(key, parameter.get(key).trim());
			if (query.equals(pss.asUpdate().toString())) {
				// JOptionPane.showMessageDialog(null, "Querynames are flawed.
				// This should not happen.");
				System.err.println(pss.toString());
				dataset.abort();
				return 0;
			}
		}
		UpdateAction.execute(pss.asUpdate(), graph);
		size = graph.size() - size;
		dataset.commit();
		return size;
	}
}
