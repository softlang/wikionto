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
		long size = proc.transformFile("removeRedundantClassifies.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);
	}

	public void removeRedundantSubtypes() {
		HashMap<String, String> pmap = new HashMap<>();
		long size = proc.transformFile("removeRedundantSubclassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);
	}

	public void abandonInstance(String n) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("name", n);
		long size = proc.transformFile("abandonInstance.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

	void cleanUpUnreachableAll() {
		Map<String, String> pmap = new HashMap<>();
		long tsize = 0;
		long size = 1;
		while (size != 0) {
			size = proc.transformFile("cleanUpTypes.sparql", pmap);
			System.out.println("cleaned up types: " + size);
			size += proc.transformFile("cleanUpEntities.sparql", pmap);
			System.out.println("cleaned up entities: " + size);
			size += proc.transformFile("cleanUpInformation.sparql", pmap);
			System.out.println("cleaned up information: " + size);
			size += proc.transformFile("cleanUpProperties.sparql", pmap);
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
			size = proc.transformFile("cleanUpTypes.sparql", pmap);
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
			size += proc.transformFile("cleanUpEntities.sparql", pmap);
			System.out.println("cleaned up entities: " + size);
			tsize += size;
		}

		System.out.println("Transformation successful! \n Model size difference: " + tsize);
	}

	public void removeClassifies(String ename, String tname) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("classifiername", tname);
		pmap.put("entityname", ename);
		long size = proc.transformFile("deleteClassifies.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

	public void removeSubclassifier(String sup, String sub) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("subclassifiername", sub);
		pmap.put("oldsuperclassifiername", sup);
		long size = proc.transformFile("deleteHasSubclassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

	public void collapseClassifier(String name) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("name", name);
		long size = proc.transformFile("collapseClassifier.sparql", pmap);
		pmap.clear();
		pmap.put("name", name);
		size += proc.transformFile("abandonClassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);
	}

	public void abandonClassifier(String n) {
		Map<String, String> pmap = new HashMap<>();
		pmap.put("name", n);
		long size = proc.transformFile("abandonClassifier.sparql", pmap);
		System.out.println("Transformation successful! \n Model size difference: " + size);

	}

}
