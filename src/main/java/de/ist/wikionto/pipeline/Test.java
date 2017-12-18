package de.ist.wikionto.research.temp;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.PriorityQueue;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

public class Test {

	public static void main(String[] args) {
		
//		Dataset da = createNewDataset("Computer_languages_Test","Computer_languages_Pipeline");
		Dataset da = TDBFactory.createDataset("Computer_languages_Test");
		TransformationUtil.transformFile(da, "/cleanUpClassifier0.sparql", new HashMap<String, String>());
	}
	
	public static Dataset createNewDataset(String newName, String oldName) {
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
		return TDBFactory.createDataset(newName);
	}
}
