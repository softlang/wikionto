package de.ist.wikionto;

import java.util.Iterator;
import java.util.List;

import javax.swing.JToggleButton;

import com.hp.hpl.jena.query.Dataset;

import de.ist.wikionto.triplestore.clean.Prune;

public class PruneUtil {

	static void abandonSelected(List<JToggleButton> subaba, List<JToggleButton> insaba, List<String> subclassifiers,
			List<String> instances, String logname, Dataset dataset) {
		Iterator<JToggleButton> abait = insaba.iterator();
		for (String l2 : instances)
			if (abait.next().isSelected()) {
				new Prune(dataset).abandonInstance(l2);
				PruningTopology.addLogEntry(logname, "\tAbandon instance " + l2);
			}
		abait = subaba.iterator();
		for (String l2 : subclassifiers)
			if (abait.next().isSelected()) {
				new Prune(dataset).abandonClassifier(l2);
				PruningTopology.addLogEntry(logname, "\tAbandon classifier " + l2);
			}
	}

	static void removeClassifierRelationships(List<JToggleButton> subdel, List<JToggleButton> insdel,
			List<String> subclassifiers, List<String> instances, String c, String logname, Dataset dataset) {
		Iterator<JToggleButton> delit = insdel.iterator();
		for (String l2 : instances)
			if (delit.next().isSelected()) {
				new Prune(dataset).removeClassifies(l2, c);
				PruningTopology.addLogEntry(logname, "\tRemove : " + c + " classifies " + l2);
			}
		delit = subdel.iterator();
		for (String l2 : subclassifiers)
			if (delit.next().isSelected()) {
				new Prune(dataset).removeSubclassifier(c, l2);
				PruningTopology.addLogEntry("EponymousClassifier", "\tRemove : " + c + " has subclassifier " + l2);
			}
	}
}
