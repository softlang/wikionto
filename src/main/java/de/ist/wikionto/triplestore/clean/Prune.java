/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.triplestore.clean;

import java.util.HashMap;
import java.util.Map;

import com.hp.hpl.jena.query.Dataset;

/**
 *
 * @author Marcel
 */
public class Prune {

	private final TransformationProcessor proc;

	public Prune(Dataset dataset) {
		this.proc = new TransformationProcessor(dataset);
	}

	public void removeRedundantInstances() {
		HashMap<String, String> pmap = new HashMap<>();
		long size = proc.transform("removeRedundantClassifies.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);
	}

	public void removeRedundantSubtypes() {
		HashMap<String, String> pmap = new HashMap<>();
		long size = proc.transform("removeRedundantSubclassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);
	}

	public void abandonInstance(String n) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("name", n);
		long size = proc.transform("abandonInstance.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

	void cleanUpUnreachableAll() {
		Map<String, String> pmap = new HashMap<>();
		long tsize = 0;
		long size = 1;
		while (size != 0) {
			size = proc.transform("cleanUpTypes.sparql", pmap);
			System.out.println("cleaned up types: " + size);
			size += proc.transform("cleanUpEntities.sparql", pmap);
			System.out.println("cleaned up entities: " + size);
			size += proc.transform("cleanUpInformation.sparql", pmap);
			System.out.println("cleaned up information: " + size);
			size += proc.transform("cleanUpProperties.sparql", pmap);
			System.out.println("cleaned up properties: " + size);
			tsize += size;
		}

		System.out.println("Transformation successful! \n Model size difference: " + tsize);
	}

	void cleanUpUnreachableType() {
		Map<String, String> pmap = new HashMap<>();
		long tsize = 0;
		long size = 1;
		while (size != 0) {
			size = proc.transform("cleanUpTypes.sparql", pmap);
			System.out.println("cleaned up types: " + size);
			tsize += size;
		}

		System.out.println("Transformation successful! \n Model size difference: " + tsize);
	}

	void cleanUpUnreachableEnt() {
		Map<String, String> pmap = new HashMap<>();
		long tsize = 0;
		long size = 1;
		while (size != 0) {
			size += proc.transform("cleanUpEntities.sparql", pmap);
			System.out.println("cleaned up entities: " + size);
			tsize += size;
		}

		System.out.println("Transformation successful! \n Model size difference: " + tsize);
	}

	public void removeClassifies(String ename, String tname) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("classifiername", tname);
		pmap.put("entityname", ename);
		long size = proc.transform("deleteClassifies.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

	public void removeSubclassifier(String sup, String sub) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("subclassifiername", sub);
		pmap.put("oldsuperclassifiername", sup);
		long size = proc.transform("deleteHasSubclassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

	public void collapseClassifier(String name) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("name", name);
		long size = proc.transform("collapseClassifier.sparql", pmap);
		pmap.clear();
		pmap.put("name", name);
		size += proc.transform("abandonClassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);
	}

	public void abandonClassifier(String n) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("name", n);
		long size = proc.transform("abandonClassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

}
