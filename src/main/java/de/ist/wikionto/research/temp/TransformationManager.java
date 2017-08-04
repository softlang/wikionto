package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Queue;
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
	private List<Transformation> transList = new LinkedList<>();
	private Queue<QuerySolution> queryQueue;
	private String storeName = "Computer_languages";
	private Dataset store;
	private Dataset oldStore;

	private Map<String, Boolean> articleChecks;
	private int threadcounter;
	// MyLogger log = new MyLogger("logs/", "Transformation");

	public void transform() {
		// open base store
		threadcounter = 0;
		// storeName = "Computer_languages_Eponymous";
		store = TDBFactory.createDataset(storeName);
		oldStore = store;
		try {
			// get article checks
			this.articleChecks = new ArticleCheckManager().getArticleChecks(store);
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		for (Transformation t : transList) {
			queryQueue = new LinkedList<>();
			int threadnr = Runtime.getRuntime().availableProcessors() * 2;
			System.out.println("Starting with " + threadnr + " threads!");
			ExecutorService executor = Executors.newFixedThreadPool(threadnr);
			// prepare new store
			storeName = newDatasetName(t.name, storeName);
			oldStore = store;

			store = TDBFactory.createDataset(storeName);
			t.log.logDate("Working with " + threadnr + " threads");
			t.log.logLn("Write transformation " + t.name + " to store " + storeName);

			// get transformation values from store
			ResultSet rs = t.query(store);

			// perform transformation
			rs.forEachRemaining(x -> {
				queryQueue.offer(x);
			});
			// hängt sich manchmal auf ka warum
			while (true) {
				if (!queryQueue.isEmpty()) {
					incthreadcounter();
					executor.execute(new TransformationThread(t, this, queryQueue.poll()));
				} else {
					if (threadcounter <= 0) {
						executor.shutdown();
						System.out.println("Finish checking at " + new Date().toString());
						t.log.logDate("Finish Transformation " + t.name);
						break;
					}

				}
			}
			// close threadpool
			executor.shutdown();
			while (!executor.isTerminated() && !executor.isShutdown())
				;

		}
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
		tm.transList.add(new EponymousTransformation(tm));
		tm.transList.add(new DistanctCallTransformation(tm));
		tm.transform();

	}

	public boolean offer(QuerySolution arg0) {
		return queryQueue.offer(arg0);
	}

}
