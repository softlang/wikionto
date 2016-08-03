package de.ist.wikionto;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.JToggleButton;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.gui.SupportFrame;
import de.ist.wikionto.triplestore.clean.Prune;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class PruningTopology {

    private static Dataset dataset;
    private static String logPath;
    private static final String wURI = "https://en.wikipedia.org/wiki/";
    private static final String cURI = wURI + "Category:";

    public static void clean() {

	JOptionPane.showMessageDialog(null, "Welcome to our GUI support for topology based pruning of a taxonomy."
		+ "\nClick on okay to proceed and select the folder, where the TDB files for the taxonomy are saved.");
	loadTaxonomy();
	JOptionPane.showMessageDialog(null,
		"The cleaning process is built around several things. \n"
			+ "First, you should know what kind of categories you want to include or exclude"
			+ "\nas classifiers in your taxonomy."
			+ "\nSecond, the cleaning process will guide you through each bad smell. At first"
			+ "\na description of a bad smell will be given. Then, for each bad smell we provide"
			+ "\nGUI support helping in getting rid of confirmed issues."
			+ "Further, every action you take is logged for reproducibility.");
	initializeLog();
	// JOptionPane.showMessageDialog(null,
	// "We start with the bad smell `Eponymous Classifier'. "
	// + "\nIt matches those classifiers for which an instance exist with
	// the same name"
	// + "\nor where the classifier's name is the plural form of the
	// instance's name.");

	// fixEponymousType();

	// JOptionPane.showMessageDialog(null,
	// "We continue with the bad smell `Semantically Distant Classifier'. "
	// + "\nIt matches those classifiers that have less superclassifiers
	// that"
	// + "are subclassifiers of the root than superclassifiers that
	// aren't.");
	// fixSemanticDistantClassifier();

	// JOptionPane.showMessageDialog(null,
	// "We continue with the bad smell `Semantically Distant Instance'. "
	// + "\nIt matches those classified entities that have less classifiers
	// that"
	// + "are subclassifiers of the root than classifiers that aren't.");

	// fixSemanticDistantInstance();

	JOptionPane.showMessageDialog(null, "We continue with the bad smell `Double Reachable Classifier'. "
		+ "\nIt matches those classifiers that are reachable by two " + "\ndirect subclassifiers of the root.");

	fixDoubleReachableClassifier();

	// fixDoubleReachableInstance();

	// fixCyclicClassifier();

	// fixLazyClassifier();

	// fixRedundancies();
    }

    private static void fixEponymousType() {
	String p = "./sparql/smells/EponymousClassifier.sparql";
	File logFile = new File(logPath + "EponymousClassifier.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    QuerySolution qs = rs.next();
	    String c = qs.getLiteral("cname").getString();
	    String log = null;
	    try {
		log = FileUtils.readFileToString(logFile);
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	    if (log.contains(c + " is valid"))
		continue;
	    else {
		String[] options = new String[] { "Valid", "Abandon instance", "Abandon classifier" };
		String[] links = new String[2];
		links[0] = wURI + c;
		links[1] = cURI + c;

		String info = "By clicking on the ? button you can open a browser with "
			+ "\nthe corresponding Wikipedia page giving you decision ground."
			+ "Three options are provided:" + "\nFirst, you can do nothing if the existence of both "
			+ "elements in the taxonomy is okay. "
			+ "\nSecond, you can abandon the instance, if it does not "
			+ "\ncorrespond to something you want to classify. "
			+ "\nThird, you can abandon the classifier and carefully "
			+ "\ninspect the relevance of subclassifiers and classified "
			+ "\ninstances. For each subclassifier and instance you can "
			+ "\ntoggle the Aba button to make sure this element is abandoned "
			+ "\nas well or toggle the Del button to remove the relationship "
			+ "\nfrom the classifier to the element.";

		Map<String, List<String>> map = new HashMap<>();
		List<String> instances = QueryUtil.getInstances(dataset, c);
		List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, c);
		List<String> linkedInstances = instances.stream().map(i -> wURI + i).collect(Collectors.toList());
		List<String> linkedSubclassifiers = subclassifiers.stream().map(sc -> cURI + sc)
			.collect(Collectors.toList());
		map.put("Classified instances", linkedInstances);
		map.put("Subclassifiers", linkedSubclassifiers);
		String qmsg = c + " is an eponymous classifier";
		SupportFrame ps = new SupportFrame(qmsg, options, map, links, true, true, info);
		ps.setVisible(true);
		int r = ps.getOption();
		System.out.println("Disposing");
		ps.dispose();
		addLogBlock("EponymousClassifier", qmsg);
		assert r >= 0 && r < 3;
		if (r == 0) {
		    addLogEntry("EponymousClassifier", c + " is valid");
		    continue;
		}
		if (r == 1) {
		    f = true;
		    new Prune(dataset).abandonInstance(c);
		    addLogEntry("EponymousClassifier", "Abandon instance : " + c);
		    continue;
		}
		if (r == 2) {
		    f = true;
		    Map<String, List<JToggleButton>> tm = ps.getToggleMap();
		    List<JToggleButton> list1 = tm.get("Classified instances");
		    Iterator<JToggleButton> it = list1.iterator();
		    addLogEntry("EponymousClassifier", "Abandon classifier :" + c);
		    for (String l2 : instances) {
			if (it.next().isSelected()) {
			    new Prune(dataset).abandonInstance(l2);
			    addLogEntry("EponymousClassifier", "\tAbandon instance " + l2);
			}
			if (it.next().isSelected()) {
			    new Prune(dataset).removeClassifies(l2, c);
			    addLogEntry("EponymousClassifier", "\tRemove : " + c + " classifies " + l2);
			}
		    }
		    list1 = tm.get("Subclassifiers");
		    it = list1.iterator();
		    for (String l2 : subclassifiers) {
			if (it.next().isSelected()) {
			    new Prune(dataset).abandonClassifier(l2);
			    addLogEntry("EponymousClassifier", "\tAbandon classifier " + l2);
			}
			if (it.next().isSelected()) {
			    new Prune(dataset).removeSubclassifier(c, l2);
			    addLogEntry("EponymousClassifier", "\tRemove : " + c + " has subclassifier " + l2);
			}
		    }
		    new Prune(dataset).collapseClassifier(c);
		}
	    }
	}
	if (f)
	    fixEponymousType();
    }

    private static void fixSemanticDistantClassifier() {
	String p = "./sparql/smells/SemanticallyDistantClassifier.sparql";
	File logFile = new File(logPath + "SemanticallyDistantClassifier.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    QuerySolution qs = rs.next();
	    String c = qs.getLiteral("cname").getString();
	    String log = null;
	    try {
		log = FileUtils.readFileToString(logFile);
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	    if (log.contains(c + " is valid"))
		continue;
	    else {
		String qmsg = c + " is a semantically distant classifier";
		addLogBlock("SemanticallyDistantClassifier", qmsg);
		String[] options = new String[] { "Valid", "Abandon classifier" };
		String[] links = new String[1];
		links[0] = "https://en.wikipedia.org/wiki/Category:" + c;

		String info = "By clicking on the ? button you can open a browser with "
			+ "\nthe corresponding Wikipedia page giving you decision ground."
			+ "\nThree options are provided:"
			+ "\nFirst, you can do nothing if the existence the classifier is feasible. "
			+ "\nSecond, you can abandon the classifier and carefully "
			+ "\ninspect the relevance of subclassifiers and classified "
			+ "\ninstances. For each subclassifier and instance you can "
			+ "\ntoggle the Aba button to make sure this element is abandoned "
			+ "\nas well or toggle the Del button to remove the relationship "
			+ "\nfrom the classifier to the element.";

		Map<String, List<String>> map = new HashMap<>();
		List<String> instances = QueryUtil.getInstances(dataset, c);
		List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, c);
		map.put("Classified instances", instances.stream().map(i -> wURI + i).collect(Collectors.toList()));
		map.put("Subclassifiers", subclassifiers.stream().map(i -> cURI + i).collect(Collectors.toList()));
		SupportFrame ps = new SupportFrame(qmsg, options, map, links, true, true, info);
		ps.setVisible(true);
		int r = ps.getOption();
		ps.dispose();

		assert r >= 0 && r < 2;
		if (r == 0) {
		    addLogEntry("SemanticallyDistantClassifier", c + " is valid");
		    continue;
		}
		if (r == 1) {
		    f = true;
		    addLogEntry("SemanticallyDistantClassifier", "Abandon classifier " + c);
		    Map<String, List<JToggleButton>> tm = ps.getToggleMap();
		    List<JToggleButton> list1 = tm.get("Classified instances");
		    Iterator<JToggleButton> it = list1.iterator();
		    for (String l2 : instances) {
			if (it.next().isSelected()) {
			    addLogEntry("SemanticallyDistantClassifier", "\tAbandon instance " + l2);
			    new Prune(dataset).abandonInstance(l2);
			}
			if (it.next().isSelected()) {
			    addLogEntry("SemanticallyDistantClassifier", "\tRemove : " + c + " classifies " + l2);
			    new Prune(dataset).removeClassifies(l2, c);
			}
		    }
		    list1 = tm.get("Subclassifiers");
		    it = list1.iterator();
		    for (String l2 : subclassifiers) {
			if (it.next().isSelected()) {
			    addLogEntry("SemanticallyDistantClassifier", "\tAbandon classifier " + l2);
			    new Prune(dataset).abandonClassifier(l2);
			}
			if (it.next().isSelected()) {
			    addLogEntry("SemanticallyDistantClassifier",
				    "\tRemove : " + c + " has subclassifier " + l2);
			    new Prune(dataset).removeSubclassifier(c, l2);
			}
		    }
		    new Prune(dataset).collapseClassifier(c);
		}
	    }
	}
	if (f)
	    fixSemanticDistantClassifier();
    }

    private static void fixSemanticDistantInstance() {
	String p = "./sparql/smells/SemanticallyDistantInstance.sparql";
	File logFile = new File(logPath + "SemanticallyDistantInstance.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    QuerySolution qs = rs.next();
	    String i = qs.getLiteral("iname").getString();
	    String log = null;
	    try {
		log = FileUtils.readFileToString(logFile);
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	    if (log.contains(i + " is valid"))
		continue;
	    else {
		String[] options = new String[] { "Valid", "Abandon Instance" };
		String[] links = new String[1];
		links[0] = "https://en.wikipedia.org/wiki/" + i;

		String info = "By clicking on the ? button you can open a browser with "
			+ "\nthe corresponding Wikipedia page giving you decision ground."
			+ "\nTwo options are provided:"
			+ "\nFirst, you can do nothing if the existence the instance is feasible. "
			+ "\nSecond, you can abandon the instance. The list of classifiers is provided.";

		Map<String, List<String>> map = new HashMap<>();
		List<String> classifiers = QueryUtil.getClassifiers(dataset, i);
		map.put("Classifiers", classifiers.stream().map(cl -> cURI + cl).collect(Collectors.toList()));
		String qmsg = i + " is a semantically distant instance";
		addLogBlock("SemanticallyDistantInstance", qmsg);
		SupportFrame ps = new SupportFrame(qmsg, options, map, links, false, false, info);
		ps.setVisible(true);
		int r = ps.getOption();
		ps.dispose();

		assert r >= 0 && r < 2;
		if (r == 0) {
		    addLogEntry("SemanticallyDistantInstance", i + " is valid");
		    continue;
		}
		if (r == 1) {
		    f = true;
		    addLogEntry("SemanticallyDistantInstance", "Abandon instance " + i);
		    new Prune(dataset).abandonInstance(i);
		}
	    }
	}
	if (f)
	    fixSemanticDistantInstance();
    }

    private static void fixDoubleReachableClassifier() {
	String p = "./sparql/smells/DoubleReachableClassifier.sparql";
	File logFile = new File(logPath + "DoubleReachableClassifier.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    QuerySolution qs = rs.next();
	    String t = qs.getLiteral("classifiername").getString();
	    String top1 = qs.getLiteral("topclassifier1name").getString();
	    String top2 = qs.getLiteral("topclassifier2name").getString();
	    String log = null;
	    try {
		log = FileUtils.readFileToString(logFile);
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	    if (log.contains(t + " having top classifiers " + top1 + " & " + top2 + " is valid"))
		continue;
	    else {
		String[] options = new String[] { "Valid", "Remove selected relationships" };
		String[] links = new String[3];
		links[0] = "https://en.wikipedia.org/wiki/Category:" + t;
		links[1] = "https://en.wikipedia.org/wiki/Category:" + top1;
		links[2] = "https://en.wikipedia.org/wiki/Category:" + top2;

		String info = "By clicking on the ? button you can open a browser with \n"
			+ "the corresponding Wikipedia page giving you decision ground. \n"
			+ "Two options are provided: \n"
			+ "First, you can do nothing if the double reachability of the classifier " + t
			+ " is feasible. \n " + "Second, the possible paths from the top classifiers to " + t
			+ " are presented.\n" + "You can toggle the DEL button for a classifier in the path. \n"
			+ "This will remove the subclassifier relationship from the selected to its"
			+ "superclassifier.";

		Map<String, List<String>> map = new HashMap<>();
		List<String> list1 = QueryUtil.getPathFromClassToClass(dataset, top1, t);
		List<String> list2 = QueryUtil.getPathFromClassToClass(dataset, top2, t);
		map.put("Path from " + top1, list1.stream().map(i -> cURI + i).collect(Collectors.toList()));
		map.put("Path from " + top2, list2.stream().map(i -> cURI + i).collect(Collectors.toList()));
		// TODO Add proper links in the map
		String qmsg = t + " is a double reachable classifier with top classifiers:" + top1 + " & " + top2;
		addLogBlock("DoubleReachableClassifier", qmsg);
		SupportFrame ps = new SupportFrame(qmsg, options, map, links, false, true, info);
		ps.setVisible(true);
		int r = ps.getOption();
		ps.dispose();
		assert r >= 0 && r < 2;
		if (r == 0) {
		    addLogEntry("DoubleReachableClassifier",
			    t + " having top classifiers " + top1 + " & " + top2 + " is valid");
		    continue;
		}
		if (r == 1) {
		    addLogEntry("DoubleReachableClassifier", "Remove classifications for " + t);
		    f = true;
		    Map<String, List<JToggleButton>> togglemap = ps.getToggleMap();
		    List<JToggleButton> toggles1 = togglemap.get("Path from top1");
		    List<JToggleButton> toggles2 = togglemap.get("Path from top2");
		    if (toggles1.get(0).isSelected()) {
			addLogEntry("DoubleReachableClassifier",
				"\tRemove : " + top1 + " has subclassifier " + list1.get(0));
			new Prune(dataset).removeSubclassifier(top1, list1.get(0));
		    }
		    for (int i = 1; i < toggles1.size(); i++) {
			if (toggles1.get(i).isSelected()) {
			    addLogEntry("DoubleReachableClassifier",
				    "\tRemove : " + list1.get(i - 1) + " has subclassifier " + list1.get(i));
			    new Prune(dataset).removeSubclassifier(list1.get(i - 1), list1.get(i));
			}
		    }
		    if (toggles2.get(0).isSelected()) {
			addLogEntry("DoubleReachableClassifier",
				"\tRemove : " + top2 + " has subclassifier " + list2.get(0));
			new Prune(dataset).removeSubclassifier(top2, list2.get(0));
		    }
		    for (int i = 1; i < toggles2.size(); i++) {
			if (toggles2.get(i).isSelected()) {
			    addLogEntry("DoubleReachableClassifier",
				    "\tRemove : " + list2.get(i - 1) + " has subclassifier " + list2.get(i));
			    new Prune(dataset).removeSubclassifier(list2.get(i - 1), list2.get(i));
			}
		    }
		}
	    }
	}
	if (f)
	    fixDoubleReachableClassifier();
    }

    private static void fixDoubleReachableInstance() {
	String p = "./sparql/smells/DoubleReachableInstance.sparql";
	File logFile = new File(logPath + "DoubleReachableInstance.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    QuerySolution qs = rs.next();
	    String dri = qs.getLiteral("typename").getString();
	    String top1 = qs.getLiteral("toptype1name").getString();
	    String top2 = qs.getLiteral("toptype2name").getString();
	    String log = null;
	    try {
		log = FileUtils.readFileToString(logFile);
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	    if (log.contains(dri + " having top classifiers " + top1 + " & " + top2 + " is valid"))
		continue;
	    else {
		String[] options = new String[] { "Valid", "Remove selected relationships" };
		String[] links = new String[3];
		links[0] = "https://en.wikipedia.org/wiki/Category:" + dri;
		links[1] = "https://en.wikipedia.org/wiki/Category:" + top1;
		links[2] = "https://en.wikipedia.org/wiki/Category:" + top2;

		String info = "By clicking on the ? button you can open a browser with \n"
			+ "the corresponding Wikipedia page giving you decision ground. \n"
			+ "Two options are provided: \n"
			+ "First, you can do nothing if the double reachability of the instance " + dri
			+ " is feasible. \n " + "Second, the possible paths from the top classifiers to " + dri
			+ " are presented.\n" + "You can toggle the DEL button for a classifier in the path. \n"
			+ "This will remove the relationship to the next parent.";

		Map<String, List<String>> map = new HashMap<>();
		List<String> list1 = QueryUtil.getPathFromClassToInstance(dataset, top1, dri);
		list1 = list1.stream().map(i -> cURI + i).collect(Collectors.toList());
		String inst = list1.get(list1.size() - 1).replace("Category:", "");
		list1.remove(list1.size() - 1);
		list1.add(inst);
		List<String> list2 = QueryUtil.getPathFromClassToInstance(dataset, top2, dri);
		list2 = list2.stream().map(i -> cURI + i).collect(Collectors.toList());
		inst = list2.get(list2.size() - 1).replace("Category:", "");
		list2.remove(list2.size() - 1);
		list2.add(inst);
		map.put("Path from top1", list1);
		map.put("Path from top2", list2);
		// TODO Add proper links in the map
		String qmsg = dri + "is a double reachable instance with top classifiers:" + top1 + " & " + top2;
		SupportFrame ps = new SupportFrame(qmsg, options, map, links, false, true, info);
		ps.setVisible(true);
		int r = ps.getOption();
		ps.dispose();
		assert r >= 0 && r < 2;
		if (r == 0) {

		    continue;
		}
		if (r == 1) {
		    f = true;
		    Map<String, List<JToggleButton>> togglemap = ps.getToggleMap();
		    List<JToggleButton> toggles1 = togglemap.get("Path from top1");
		    List<JToggleButton> toggles2 = togglemap.get("Path from top2");
		    if (toggles1.get(0).isSelected()) {
			new Prune(dataset).removeSubclassifier(top1, list1.get(0));
		    }
		    for (int i = 1; i < toggles1.size() - 1; i++) {
			if (toggles1.get(i).isSelected()) {
			    new Prune(dataset).removeSubclassifier(list1.get(i - 1), list1.get(i));
			}
		    }
		    if (toggles1.get(toggles1.size() - 1).isSelected()) {
			if (toggles1.size() > 1)
			    new Prune(dataset).removeClassifies(list1.get(list1.size() - 1),
				    list1.get(list1.size() - 2));
			else
			    new Prune(dataset).removeClassifies(list1.get(0), top1);
		    }
		    if (toggles2.get(0).isSelected()) {
			new Prune(dataset).removeSubclassifier(top2, list2.get(0));
		    }
		    for (int i = 1; i < toggles2.size() - 1; i++) {
			if (toggles2.get(i).isSelected()) {
			    new Prune(dataset).removeSubclassifier(list2.get(i - 1), list2.get(i));
			}
		    }
		    if (toggles2.get(toggles2.size() - 1).isSelected()) {
			if (toggles2.size() > 1)
			    new Prune(dataset).removeClassifies(list2.get(list2.size() - 1),
				    list2.get(list2.size() - 2));
			else
			    new Prune(dataset).removeClassifies(list2.get(0), top2);
		    }
		}
	    }
	}

	if (f)
	    fixDoubleReachableInstance();
    }

    private static void fixCyclicClassifier() {
	String p = "./sparql/smells/CyclicClassifier.sparql";
	File logFile = new File(logPath + "CyclicClassifier.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    f = true;
	    QuerySolution qs = rs.next();
	    String cc = qs.getLiteral("typename").getString();

	    String[] options = new String[] { "Remove selected relationships" };
	    String[] links = new String[3];
	    links[0] = "https://en.wikipedia.org/wiki/Category:" + cc;

	    String info = "By clicking on the ? button you can open a browser with \n"
		    + "the corresponding Wikipedia page giving you decision ground. \n" + "Two options are provided: \n"
		    + "First, you can do nothing if the double reachability of the instance " + cc + " is feasible. \n "
		    + "Second, the possible paths from the top classifiers to " + cc + " are presented.\n"
		    + "You can toggle the DEL button for a classifier in the path. \n"
		    + "This will remove the relationship to the next parent.";

	    Map<String, List<String>> map = new HashMap<>();
	    List<String> list1 = QueryUtil.getPathFromClassToInstance(dataset, cc, cc);
	    map.put("Cycle path", list1.stream().map(i -> cURI + i).collect(Collectors.toList()));
	    // TODO Add proper links in the map
	    SupportFrame ps = new SupportFrame(cc + " is a cyclic classifier", options, map, links, false, true, info);
	    ps.setVisible(true);
	    int r = ps.getOption();
	    ps.dispose();
	    assert r == 0;
	    Map<String, List<JToggleButton>> togglemap = ps.getToggleMap();
	    List<JToggleButton> toggles1 = togglemap.get("Cycle path");
	    if (toggles1.get(0).isSelected()) {
		new Prune(dataset).removeSubclassifier(cc, list1.get(0));
	    }
	    for (int i = 1; i < toggles1.size(); i++) {
		if (toggles1.get(i).isSelected()) {
		    new Prune(dataset).removeSubclassifier(list1.get(i - 1), list1.get(i));
		}
	    }
	}
	if (f)
	    fixCyclicClassifier();
    }

    private static void fixLazyClassifier() {
	String p = "./sparql/smells/LazyClassifier.sparql";
	File logFile = new File(logPath + "LazyClassifier.txt");
	if (!logFile.exists()) {
	    System.out.println("Creating log file " + logFile.getAbsolutePath());
	    try {
		FileUtils.write(logFile, "");
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	}
	ResultSet rs = QueryUtil.executeQuery(dataset, p);
	boolean f = false;
	while (rs.hasNext()) {
	    QuerySolution qs = rs.next();
	    String c = qs.getLiteral("cname").getString();
	    String log = null;
	    try {
		log = FileUtils.readFileToString(logFile);
	    } catch (IOException e) {
		e.printStackTrace();
	    }
	    if (log.contains(c + " is valid"))
		continue;
	    else {
		String[] options = new String[] { "Valid", "Abandon classifier" };
		String[] ws = new String[2];
		ws[1] = "https://en.wikipedia.org/wiki/Category:" + c;

		String info = "By clicking on the ? button you can open a browser with "
			+ "\nthe corresponding Wikipedia page giving you decision ground."
			+ "Three options are provided:"
			+ "\nFirst, you can do nothing if the existence the classifier is feasible. "
			+ "\nSecond, you can abandon the classifier and carefully "
			+ "\ninspect the relevance of subclassifiers and classified "
			+ "\ninstances. For each subclassifier and instance you can "
			+ "\ntoggle the Aba button to make sure this element is abandoned "
			+ "\nas well or toggle the Del button to remove the relationship "
			+ "\nfrom the classifier to the element.";

		Map<String, List<String>> map = new HashMap<>();
		List<String> instances = QueryUtil.getInstances(dataset, c);
		List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, c);
		map.put("Classified instances", instances.stream().map(i -> wURI + i).collect(Collectors.toList()));
		map.put("Subclassifiers", subclassifiers.stream().map(i -> cURI + i).collect(Collectors.toList()));
		// TODO Add proper links in the map
		SupportFrame ps = new SupportFrame(c + " is a lazy classifier", options, map, ws, true, true, info);
		ps.setVisible(true);
		int r = ps.getOption();
		ps.dispose();

		assert r >= 0 && r < 2;
		if (r == 0) {
		    continue;
		}
		if (r == 1) {
		    f = true;
		    Map<String, List<JToggleButton>> tm = ps.getToggleMap();
		    List<JToggleButton> list1 = tm.get("Classified instances");
		    Iterator<JToggleButton> it = list1.iterator();
		    for (String l2 : instances) {
			if (it.next().isSelected()) {
			    new Prune(dataset).abandonInstance(l2);
			}
			if (it.next().isSelected()) {
			    new Prune(dataset).removeClassifies(l2, c);
			}
		    }
		    list1 = tm.get("Subclassifiers");
		    for (String l2 : subclassifiers) {
			if (it.next().isSelected()) {
			    new Prune(dataset).abandonClassifier(l2);
			}
			if (it.next().isSelected()) {
			    new Prune(dataset).removeSubclassifier(c, l2);
			}
		    }
		    new Prune(dataset).collapseClassifier(c);
		}
	    }
	}
	if (f)
	    fixLazyClassifier();

    }

    private static void fixRedundancies() {
	JOptionPane.showMessageDialog(null, "At last, all existing redundancies will be automatically removed.");
	Prune p = new Prune(dataset);
	p.removeRedundantSubtypes();
	p.removeRedundantInstances();
    }

    public static void loadTaxonomy() {
	JFileChooser fc = new JFileChooser();
	fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
	fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	int returnVal = fc.showOpenDialog(null);
	if (returnVal == JFileChooser.APPROVE_OPTION) {
	    dataset = TDBFactory.createDataset(fc.getSelectedFile().toString());
	} else {
	    JOptionPane.showMessageDialog(null, "Loading ontology failed");
	    loadTaxonomy();
	}
    }

    public static void initializeLog() {
	int b = JOptionPane.showConfirmDialog(null, "Do you want to use existing log-files?");
	if (b == 2) {
	    JOptionPane.showMessageDialog(null, "Restart the program to proceed.");
	    System.exit(0);
	}
	if (b == 1) {
	    File f = new File(
		    "evaluation/logs/log" + LocalDateTime.now().toString().replaceAll(":", "").replaceAll("\\.", ""));
	    f.mkdirs();
	    JOptionPane.showMessageDialog(null, "Creating new log files in \n" + f.getAbsolutePath());
	    logPath = f.getAbsolutePath() + "/";
	}
	if (b == 0) {
	    JFileChooser fc = new JFileChooser();
	    fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
	    fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
	    int returnVal = fc.showOpenDialog(null);
	    if (returnVal == JFileChooser.APPROVE_OPTION) {
		logPath = fc.getSelectedFile().getAbsolutePath() + "/";
	    } else {
		JOptionPane.showMessageDialog(null, "Loading log folder failed. Please restart!");
		System.exit(0);
	    }
	}

    }

    public static void addLogBlock(String smellname, String queryresults) {
	String e = "\n" + queryresults;

	File f = new File(logPath + smellname + ".txt");
	try {
	    String s = FileUtils.readFileToString(f);
	    s += e;
	    FileUtils.writeStringToFile(f, s);
	} catch (IOException e1) {
	    System.err.println("Reading failed for " + f.getAbsolutePath());
	    e1.printStackTrace();
	}
    }

    public static void addLogEntry(String smellname, String entry) {
	String e = "\n\t" + entry;

	File f = new File(logPath + smellname + ".txt");
	try {
	    String s = FileUtils.readFileToString(f);
	    s += e;
	    FileUtils.writeStringToFile(f, s);
	} catch (IOException e1) {
	    System.err.println("Reading failed for " + f.getAbsolutePath());
	    e1.printStackTrace();
	}
    }

    public static void main(String[] args) {
	clean();
    }
}
