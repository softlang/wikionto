/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.triplestore.clean;

import java.util.HashMap;
import java.util.Map;

import javax.swing.JOptionPane;

import com.hp.hpl.jena.query.Dataset;

import de.ist.wikionto.gui.DissolveGUI;

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
		long size = proc.transform("removeRedundantInstances.sparql", pmap);
		JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);
	}

	public void removeRedundantSubtypes() {
		HashMap<String, String> pmap = new HashMap<>();
		long size = proc.transform("removeRedundantSubtypes.sparql", pmap);
		JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);
	}

	public void abandonInstance(String n) {
		if (null != n) {
			Map<String, String> pmap = new HashMap<>();
			pmap.put("name", n);
			long size = proc.transform("abandonInstance.sparql", pmap);
			JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);
		} else {
			JOptionPane.showMessageDialog(null, "Transformation failed! " + n);
		}
	}

	public void abandonClassifier(String n) {
		new DissolveGUI(proc.getDataset(), n).setVisible(true);
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

		JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + tsize);
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

		JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + tsize);
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

		JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + tsize);
	}

	public void removeInstance(String ename, String tname) {
		String namee = "";
		String namet = "";
		if (ename == null || tname == null) {
			namee = JOptionPane.showInputDialog("Name the entity:");
			namet = JOptionPane.showInputDialog("Name the type:");
		} else {
			namee = ename;
			namet = tname;
		}
		if (null != namee && null != namet) {
			Map<String, String> pmap = new HashMap<>();
			pmap.put("typename", namet);
			pmap.put("entityname", namee);
			long size = proc.transform("deleteHasInstance.sparql", pmap);
			if (ename == null && tname == null)
				JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);

		} else {
			JOptionPane.showMessageDialog(null, "Transformation failed!");
		}
	}

	public void removeSubclassifier(String sup, String sub) {
		String supname = "";
		String subname = "";
		if (sup == null || sub == null) {
			supname = JOptionPane.showInputDialog(null, "Name the supertype:");
			subname = JOptionPane.showInputDialog(null, "Name the subtype that should be removed from the type:");
		}
		if (supname != null && subname != null) {
			Map<String, String> pmap = new HashMap<>();
			pmap.put("subtypename", subname);
			pmap.put("oldsupertypename", supname);
			long size = proc.transform("deleteHasSubtype.sparql", pmap);
			if (sup == null && sub == null)
				JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);
		} else {
			JOptionPane.showMessageDialog(null, "Transformation failed!");
		}
	}

	public void collapseClassifier(String n) {
		String name = "";
		if (n != null)
			name = n;
		else
			name = JOptionPane.showInputDialog(null, "Name the dissolvable type:");
		if (null != name) {
			Map<String, String> pmap = new HashMap<>();
			pmap.put("name", name);
			long size = proc.transform("collapseClassifier.sparql", pmap);
			pmap.clear();
			pmap.put("name", name);
			size += proc.transform("abandonClassifier.sparql", pmap);
			if (n == null)
				JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);
		} else {
			JOptionPane.showMessageDialog(null, "Transformation failed!" + name);
		}
	}

}
