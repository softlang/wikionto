/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.triplestore.clean;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.graph.Graph;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ParameterizedSparqlString;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.tdb.TDBFactory;
import com.hp.hpl.jena.update.UpdateAction;

/**
 *
 * @author Marcel
 */
public class TransformationProcessor {

	private final Dataset dataset;

	public TransformationProcessor(Dataset dataset) {
		this.dataset = dataset;
	}

	public long transformString(String transform) {
		dataset.begin(ReadWrite.WRITE);
		Graph graph = dataset.asDatasetGraph().getDefaultGraph();
		long size = graph.size();
		UpdateAction.parseExecute(transform, dataset);
		dataset.commit();
		return graph.size() - size;
	}

	public long transformFile(String tfilename, Map<String, String> parameter) {
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
				JOptionPane.showMessageDialog(null, "Querynames are flawed. This should not happen.");
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

	public Dataset getDataset() {
		return dataset;
	}

	/*
	 * This executes redundancy removal
	 */
	public static void main(String[] args0) {
		// load dataset
		Dataset dataset;
		JFileChooser fc = new JFileChooser();
		fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
		fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		int returnVal = fc.showOpenDialog(null);
		if (returnVal == JFileChooser.APPROVE_OPTION) {
			dataset = TDBFactory.createDataset(fc.getSelectedFile().toString());
			TransformationProcessor tp = new TransformationProcessor(dataset);
			Map<String, String> pmap = new HashMap<>();
			tp.transformFile("deletex.sparql", pmap);
		}
	}

}
