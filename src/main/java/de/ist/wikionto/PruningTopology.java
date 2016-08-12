package de.ist.wikionto;

import java.io.File;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.JToggleButton;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.Syntax;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.gui.SupportFrame;
import de.ist.wikionto.triplestore.clean.Prune;
import de.ist.wikionto.triplestore.clean.TransformationProcessor;
import de.ist.wikionto.triplestore.query.QueryProcessor;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class PruningTopology {

	private static Dataset dataset;
	private static String logPath;
	private static final String wURI = "https://en.wikipedia.org/wiki/";
	private static final String cURI = wURI + "Category:";
	private static String root;

	public static void clean() {
		if (root == null) {
			System.err.println("No root classifier has been set");
			return;
		}
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
		JOptionPane.showMessageDialog(null, "We start with the bad smell `Eponymous Classifier'. "
				+ "\nIt matches those classifiers for which an instance exist with the same name.");

		fixEponymousType();

		JOptionPane.showMessageDialog(null,
				"We continue with the bad smell `Semantically Distant Classifier'. "
						+ "\nIt matches those classifiers that have less superclassifiers that"
						+ "\nare subclassifiers of the root than superclassifiers that aren't.");
		fixSemanticDistantClassifier();

		JOptionPane.showMessageDialog(null,
				"We continue with the bad smell `Semantically Distant Instance'. "
						+ "\nIt matches those classified entities that have less classifiers that"
						+ "are subclassifiers of the root than classifiers that aren't.");

		fixSemanticDistantInstance();

		new Prune(dataset).cleanUpUnreachableAll();
		System.out.println("Cleaned up");

		JOptionPane.showMessageDialog(null,
				"We continue with the bad smell `Double Reachable Classifier'. "
						+ "\nIt matches those classifiers that are reachable by two "
						+ "\ndistinct subclassifiers of the root.");

		fixDoubleReachableClassifier();

		JOptionPane.showMessageDialog(null,
				"We continue with the bad smell `Double Reachable Instance'. "
						+ "\nIt matches those instances that are classified by two "
						+ "\ndistinct subclassifiers of the root.");
		fixDoubleReachableInstance();

		JOptionPane.showMessageDialog(null, "We continue with the bad smell `Cyclic classifier'. "
				+ "\nIt identifies the existence of a classifier that is" + "\na subclassifier of itself.");
		fixCyclicClassifier();

		JOptionPane.showMessageDialog(null,
				"We continue with the bad smell `Lazy classifier'. "
						+ "\nIt identifies all classifiers that have less than n subclassifiers and classified instances. In the next"
						+ "\ndialog you have to set a value for n based on your own observations."
						+ "\na subclassifier of itself.");
		String n = JOptionPane.showInputDialog("Please enter the threshold for lazy classifiers. Classifiers"
				+ "\nwith less subclassifiers and instances will be matched.");
		fixLazyClassifier(n);

		JOptionPane.showMessageDialog(null, "We continue with the bad smell `Redundancy'. "
				+ "\nIt identifies redundant relationships and removes them automatically.");
		fixRedundancies();
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
			if (log.contains(c + " is valid") || QueryUtil.getPathFromClassToClass(dataset, root, c).isEmpty()) {
				continue;
			} else {
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
				map.put("Classified instances", instances.stream().map(i -> wURI + i).collect(Collectors.toList()));
				map.put("Subclassifiers", subclassifiers.stream().map(sc -> cURI + sc).collect(Collectors.toList()));
				String qmsg = c + " is an eponymous classifier";
				SupportFrame ps = new SupportFrame(qmsg, options, map, links, true, true, info);
				int r = ps.getOption();
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
					addLogEntry("EponymousClassifier", "Abandon classifier :" + c);
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					PruneUtil.abandonSelected(tm.get("SubclassifiersABA"), tm.get("Classified instancesABA"),
							subclassifiers, instances, "EponymousClassifier", dataset);
					PruneUtil.removeClassifierRelationships(tm.get("SubclassifiersDEL"),
							tm.get("Classified instancesDEL"), subclassifiers, instances, c, "EponymousClassifier",
							dataset);
					new Prune(dataset).collapseClassifier(c);
				}
			}
		}
		if (f) {
			fixEponymousType();
		}
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
		ResultSet rs = QueryUtil.executeRootDependentQuery(dataset, p, root);
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
			if (log.contains(c + " is valid") || QueryUtil.getPathFromClassToClass(dataset, root, c).isEmpty()) {
				continue;
			} else {
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
					PruneUtil.abandonSelected(tm.get("SubclassifiersABA"), tm.get("Classified instancesABA"),
							subclassifiers, instances, "SemanticallyDistantClassifier", dataset);
					PruneUtil.removeClassifierRelationships(tm.get("SubclassifiersDEL"),
							tm.get("Classified instancesDEL"), subclassifiers, instances, c,
							"SemanticallyDistantClassifier", dataset);
					new Prune(dataset).collapseClassifier(c);
				}
			}
		}
		if (f) {
			fixSemanticDistantClassifier();
		}
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
		ResultSet rs = QueryUtil.executeRootDependentQuery(dataset, p, root);
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
			if (log.contains(i + " is valid") || QueryUtil.getPathFromClassToInstance(dataset, root, i).isEmpty()) {
				continue;
			} else {
				String[] options = new String[] { "Valid", "Abandon Instance" };
				String[] links = new String[1];
				links[0] = "https://en.wikipedia.org/wiki/" + i;

				String info = "By clicking on the ? button you can open a browser with "
						+ "\nthe corresponding Wikipedia page giving you decision ground."
						+ "\nTwo options are provided:"
						+ "\nFirst, you can do nothing if the existence the instance is feasible. "
						+ "\nSecond, you can abandon the instance. The list of classifiers is provided. From"
						+ "\nthis list you may also select classifiers that should be abandoned.";

				Map<String, List<String>> map = new HashMap<>();
				List<String> classifiers = QueryUtil.getReachableClassifiers(dataset, i, root);
				map.put("Classifiers", classifiers.stream().map(cl -> cURI + cl).collect(Collectors.toList()));
				String qmsg = i + " is a semantically distant instance";
				addLogBlock("SemanticallyDistantInstance", qmsg);
				SupportFrame ps = new SupportFrame(qmsg, options, map, links, true, false, info);

				int r = ps.getOption();
				ps.dispose();

				assert r >= 0 && r < 2;
				if (r == 0) {
					addLogEntry("SemanticallyDistantInstance", i + " is valid");
					continue;
				}
				if (r == 1) {
					f = true;
					List<JToggleButton> abatog = ps.getToggleMap().get("ClassifiersABA");
					PruneUtil.abandonSelected(abatog, new ArrayList<JToggleButton>(), classifiers,
							new ArrayList<String>(), "SemanticallyDistantInstance", dataset);
					addLogEntry("SemanticallyDistantInstance", "Abandon instance " + i);
					new Prune(dataset).abandonInstance(i);
				}
			}
		}
		if (f) {
			fixSemanticDistantInstance();
		}
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
		ResultSet rs = QueryUtil.executeRootDependentQuery(dataset, p, root);
		// save abandoned classifiers
		Set<String> acs = new HashSet<>();
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String t = qs.getLiteral("classifiername").getString();
			if (acs.contains(t)) {
				continue;
			}
			String top1 = qs.getLiteral("topclassifier1name").getString();
			String top2 = qs.getLiteral("topclassifier2name").getString();
			String log = null;
			try {
				log = FileUtils.readFileToString(logFile);
			} catch (IOException e) {
				e.printStackTrace();
			}
			if (log.contains(t + " having top classifiers " + top1 + " & " + top2 + " is valid")) {
				continue;
			} else {
				String[] options = new String[] { "Valid", "Prune paths", "Abandon classifier" };
				String[] links = new String[3];
				links[0] = "https://en.wikipedia.org/wiki/Category:" + t;
				links[1] = "https://en.wikipedia.org/wiki/Category:" + top1;
				links[2] = "https://en.wikipedia.org/wiki/Category:" + top2;

				String info = "By clicking on the ? button you can open a browser with \n"
						+ "the corresponding Wikipedia page giving you decision ground. \n"
						+ "Three options are provided: \n"
						+ "First, you can do nothing if the double reachability of the classifier " + t
						+ " is feasible. \n " + "Second, the possible paths from the top classifiers to " + t
						+ " are presented.\n" + "You can toggle the DEL button for a classifier in the path. \n"
						+ "This will remove the subclassifier relationship from the selected to its\n"
						+ "superclassifier.\n"
						+ "Third, the classifier may simply be overcategorized and is not relevant at all.\n"
						+ "In this case, it should be abandoned completely.";

				Map<String, List<String>> map = new HashMap<>();
				List<String> path1 = QueryUtil.getPathFromClassToClass(dataset, top1, t);
				if (path1.isEmpty()) {
					continue;
				}
				List<String> path2 = QueryUtil.getPathFromClassToClass(dataset, top2, t);
				if (path2.isEmpty()) {
					continue;
				}
				List<String> instances = QueryUtil.getInstances(dataset, t);
				List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, t);
				map.put("Path from " + top1, path1.stream().map(i -> cURI + i).collect(Collectors.toList()));
				map.put("Path from " + top2, path2.stream().map(i -> cURI + i).collect(Collectors.toList()));
				map.put("Classified instances", instances.stream().map(i -> wURI + i).collect(Collectors.toList()));
				map.put("Subclassifiers", subclassifiers.stream().map(c -> wURI + c).collect(Collectors.toList()));

				String qmsg = t + " is a double reachable classifier with top classifiers:" + top1 + " & " + top2;
				addLogBlock("DoubleReachableClassifier", qmsg);
				SupportFrame ps = new SupportFrame(qmsg, options, map, links, true, true, info);

				int r = ps.getOption();
				ps.dispose();
				assert r >= 0 && r < 3;
				if (r == 0) {
					addLogEntry("DoubleReachableClassifier",
							t + " having top classifiers " + top1 + " & " + top2 + " is valid");
					continue;
				}
				if (r == 1) {
					addLogEntry("DoubleReachableClassifier", "Prune paths to " + t);
					f = true;
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					List<JToggleButton> toggles1DEL = tm.get("Path from " + top1 + "DEL");
					List<JToggleButton> toggles2DEL = tm.get("Path from " + top2 + "DEL");
					List<JToggleButton> toggles1ABA = tm.get("Path from " + top1 + "ABA");
					List<JToggleButton> toggles2ABA = tm.get("Path from " + top2 + "ABA");
					if (toggles1DEL.get(0).isSelected()) {
						addLogEntry("DoubleReachableClassifier",
								"\tRemove : " + top1 + " has subclassifier " + path1.get(0));
						new Prune(dataset).removeSubclassifier(top1, path1.get(0));
					}
					if (toggles1ABA.get(0).isSelected()) {
						addLogEntry("DoubleReachableClassifier", "\tAbandon classifier " + path1.get(0));
						new Prune(dataset).abandonClassifier(path1.get(0));
					}
					for (int i = 1; i < path1.size(); i++) {
						if (toggles1DEL.get(i).isSelected()) {
							addLogEntry("DoubleReachableClassifier",
									"\tRemove : " + path1.get(i - 1) + " has subclassifier " + path1.get(i));
							new Prune(dataset).removeSubclassifier(path1.get(i - 1), path1.get(i));
						}
						if (toggles1ABA.get(i).isSelected()) {
							addLogEntry("DoubleReachableClassifier", "\tAbandon classifier " + path1.get(i));
							new Prune(dataset).abandonClassifier(path1.get(i));
						}
					}
					if (toggles2DEL.get(0).isSelected()) {
						addLogEntry("DoubleReachableClassifier",
								"\tRemove : " + top2 + " has subclassifier " + path2.get(0));
						new Prune(dataset).removeSubclassifier(top2, path2.get(0));
					}
					if (toggles2ABA.get(0).isSelected()) {
						addLogEntry("DoubleReachableClassifier", "\tAbandon classifier " + path2.get(0));
						new Prune(dataset).abandonClassifier(path2.get(0));
					}
					for (int i = 1; i < toggles2DEL.size(); i++) {
						if (toggles2DEL.get(i).isSelected()) {
							addLogEntry("DoubleReachableClassifier",
									"\tRemove : " + path2.get(i - 1) + " has subclassifier " + path2.get(i));
							new Prune(dataset).removeSubclassifier(path2.get(i - 1), path2.get(i));
						}
						if (toggles2ABA.get(i).isSelected()) {
							addLogEntry("DoubleReachableClassifier", "\tAbandon classifier " + path2.get(i));
							new Prune(dataset).abandonClassifier(path2.get(i));
						}
					}

					if (QueryUtil.getPathFromClassToClass(dataset, root, t).isEmpty()) {
						String rep = "INSERT { ?t <http://myWikiTax.de/hasSubclassifier> ?r . }"
								+ "\nWHERE{ ?t <http://myWikiTax.de/name> \"" + t + "\" ."
								+ "\n ?r <http://myWikiTax.de/name> \"" + root + "\" .}";
						long s = new TransformationProcessor(dataset).transformString(rep);
						System.out.println("Saving complete with " + s);
					}
				}
				if (r == 2) {
					f = true;
					addLogEntry("DoubleReachableClassifier", "Abandon classifier " + t);
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					PruneUtil.abandonSelected(tm.get("SubclassifiersABA"), tm.get("Classified instancesABA"),
							subclassifiers, instances, "DoubleReachableClassifier", dataset);
					PruneUtil.removeClassifierRelationships(tm.get("SubclassifiersDEL"),
							tm.get("Classified instancesDEL"), subclassifiers, instances, t,
							"DoubleReachableClassifier", dataset);
					acs.add(t);
					new Prune(dataset).collapseClassifier(t);
				}
			}
		}
		if (f) {
			fixDoubleReachableClassifier();
		}

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
		// we need an extra set with abandoned instances
		Set<String> ais = new HashSet<>();
		ResultSet rs = QueryUtil.executeRootDependentQuery(dataset, p, root);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String dri = qs.getLiteral("name").getString();
			if (ais.contains(dri)) {
				continue;
			}
			String top1 = qs.getLiteral("top1name").getString();
			String top2 = qs.getLiteral("top2name").getString();
			try {
				String log = FileUtils.readFileToString(logFile);
				if (log.contains(dri + " having top classifiers " + top1 + " & " + top2 + " is valid")) {
					continue;
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
			String[] options = new String[] { "Valid", "Prune paths", "Abandon instance" };
			String[] links = new String[3];
			links[0] = "https://en.wikipedia.org/wiki/" + dri;
			links[1] = "https://en.wikipedia.org/wiki/Category:" + top1;
			links[2] = "https://en.wikipedia.org/wiki/Category:" + top2;

			String info = "By clicking on the ? button you can open a browser with \n"
					+ "the corresponding Wikipedia page giving you decision ground. \n" + "Two options are provided: \n"
					+ "First, you can do nothing if the double reachability of the instance " + dri
					+ " is feasible. \n " + "Second, the possible paths from the top classifiers to " + dri
					+ " are presented.\n" + "You can toggle the DEL button for a classifier in the path. \n"
					+ "This will remove the relationship to the next parent.";

			Map<String, List<String>> map = new HashMap<>();
			List<String> list1 = QueryUtil.getPathFromClassToInstance(dataset, top1, dri);
			if (list1.isEmpty()) {
				System.out.println("No way from " + top1 + " to " + dri);
				continue;
			}
			List<String> list1links = list1.stream().map(i -> cURI + i).collect(Collectors.toList());

			String inst = null;
			try {
				inst = list1links.get(list1.size() - 1).replace("Category:", "");
			} catch (Exception e) {
				System.err.println("Size : " + list1links.size());
				System.err.println("Elements:");
				list1links.forEach(l -> System.err.println(l));
				System.err.println("top1:" + top1 + ", dri:" + dri);
				System.exit(0);
			}
			list1links.remove(list1.size() - 1);
			list1links.add(inst);
			List<String> list2 = QueryUtil.getPathFromClassToInstance(dataset, top2, dri);
			if (list2.isEmpty()) {
				System.out.println("No way from " + top2 + " to " + dri);
				continue;
			}
			List<String> list2links = list2.stream().map(i -> cURI + i).collect(Collectors.toList());
			inst = list2links.get(list2.size() - 1).replace("Category:", "");
			list2links.remove(list2links.size() - 1);
			list2links.add(inst);
			map.put("Path from " + top1, list1links);
			map.put("Path from " + top2, list2links);
			String qmsg = dri + " is a double reachable instance with top classifiers:" + top1 + " & " + top2;
			addLogBlock("DoubleReachableInstance", qmsg);
			SupportFrame ps = new SupportFrame(qmsg, options, map, links, true, true, info);

			int r = ps.getOption();
			ps.dispose();
			assert r >= 0 && r < 3;
			if (r == 0) {
				addLogEntry("DoubleReachableInstance",
						dri + " having top classifiers " + top1 + " & " + top2 + " is valid");
				continue;
			}
			if (r == 1) {
				f = true;
				addLogEntry("DoubleReachableInstance", "Prune paths to " + dri);
				Map<String, List<JToggleButton>> tm = ps.getToggleMap();
				// Abandon selected categories
				List<JToggleButton> ptt1Aba = tm.get("Path from " + top1 + "ABA");
				ptt1Aba.remove(ptt1Aba.size() - 1);
				List<JToggleButton> ptt2Aba = tm.get("Path from " + top2 + "ABA");
				ptt2Aba.remove(ptt2Aba.size() - 1);
				List<String> cats1 = new ArrayList<>();
				cats1.addAll(map.get("Path from " + top1));
				cats1.remove(cats1.size() - 1);
				List<String> cats2 = new ArrayList<>();
				cats2.addAll(map.get("Path from " + top2));
				cats2.remove(cats2.size() - 1);
				PruneUtil.abandonSelected(ptt1Aba, new ArrayList<JToggleButton>(), cats1, new ArrayList<String>(),
						"DoubleReachableInstance", dataset);
				PruneUtil.abandonSelected(ptt1Aba, new ArrayList<JToggleButton>(), cats1, new ArrayList<String>(),
						"DoubleReachableInstance", dataset);
				// Remove selected relationships
				List<JToggleButton> ptt1Del = tm.get("Path from " + top1 + "DEL");
				List<JToggleButton> ptt2Del = tm.get("Path from " + top2 + "DEL");
				if (ptt1Del.get(0).isSelected() && ptt1Del.size() > 1) {
					addLogEntry("DoubleReachableInstance", "\tRemove :" + top1 + " has subclassifier " + list1.get(0));
					new Prune(dataset).removeSubclassifier(top1, list1.get(0));
				}
				for (int i = 1; i < ptt1Del.size() - 1; i++) {
					if (ptt1Del.get(i).isSelected()) {
						addLogEntry("DoubleReachableInstance",
								"\tRemove :" + list1.get(i - 1) + " has subclassifier " + list1.get(i));
						new Prune(dataset).removeSubclassifier(list1.get(i - 1), list1.get(i));
					}
				}
				if (ptt1Del.get(ptt1Del.size() - 1).isSelected()) {
					if (ptt1Del.size() > 1) {
						addLogEntry("DoubleReachableInstance", "\tRemove :" + list1.get(list1.size() - 2)
								+ " classifies " + list1.get(list1.size() - 1));
						new Prune(dataset).removeClassifies(list1.get(list1.size() - 1), list1.get(list1.size() - 2));
					} else {
						addLogEntry("DoubleReachableInstance", "\tRemove :" + top1 + " classifies " + list1.get(0));
						new Prune(dataset).removeClassifies(list1.get(0), top1);
					}
				}
				if (ptt2Del.get(0).isSelected() && ptt2Del.size() > 1) {
					addLogEntry("DoubleReachableInstance", "\tRemove :" + top2 + " has subclassifier " + list2.get(0));
					new Prune(dataset).removeSubclassifier(top2, list2.get(0));
				}
				for (int i = 1; i < ptt2Del.size() - 1; i++) {
					if (ptt2Del.get(i).isSelected()) {
						addLogEntry("DoubleReachableInstance",
								"\tRemove :" + list2.get(i - 1) + " has subclassifier " + list2.get(i));
						new Prune(dataset).removeSubclassifier(list2.get(i - 1), list2.get(i));
					}
				}
				if (ptt2Del.get(ptt2Del.size() - 1).isSelected()) {
					if (ptt2Del.size() > 1) {
						addLogEntry("DoubleReachableInstance", "\tRemove :" + list2.get(list2.size() - 2)
								+ " classifies " + list2.get(list2.size() - 1));
						new Prune(dataset).removeClassifies(list2.get(list2.size() - 1), list2.get(list2.size() - 2));
					} else {
						addLogEntry("DoubleReachableInstance", "\tRemove :" + top2 + " classifies " + list2.get(0));
						new Prune(dataset).removeClassifies(list2.get(0), top2);
					}
				}
			}
			if (r == 2) {
				f = true;
				new Prune(dataset).abandonInstance(dri);
				ais.add(dri);
				addLogEntry("DoubleReachableInstance", "Abandon instance : " + dri);
			}
		}
		if (f) {
			fixDoubleReachableInstance();
		}
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
			List<String> list1 = QueryUtil.getPathFromClassToClass(dataset, cc, cc);
			if (list1.isEmpty()) {
				continue;
			}
			map.put("Cycle path", list1.stream().map(i -> cURI + i).collect(Collectors.toList()));

			String qmsg = cc + " is a cyclic classifier";
			SupportFrame ps = new SupportFrame(qmsg, options, map, links, false, true, info);

			int r = ps.getOption();
			ps.dispose();
			assert r == 0;
			addLogBlock("CyclicClassifier", qmsg);
			addLogEntry("CyclicClassifier", "Lift Cycle");
			Map<String, List<JToggleButton>> togglemap = ps.getToggleMap();
			List<JToggleButton> toggles1 = togglemap.get("Cycle pathDEL");
			if (toggles1.get(0).isSelected()) {
				addLogEntry("CyclicClassifier", "Remove : " + cc + " has subclassifier " + list1.get(0));
				new Prune(dataset).removeSubclassifier(cc, list1.get(0));
			}
			for (int i = 1; i < toggles1.size(); i++) {
				if (toggles1.get(i).isSelected()) {
					addLogEntry("CyclicClassifier",
							"Remove : " + list1.get(i - 1) + " has subclassifier " + list1.get(i));
					new Prune(dataset).removeSubclassifier(list1.get(i - 1), list1.get(i));
				}
			}
		}
		if (f) {
			fixCyclicClassifier();
		}
	}

	private static void fixLazyClassifier(String n) {
		File lf = new File("./sparql/smells/LazyClassifier.sparql");
		File logFile = new File(logPath + "LazyClassifier.txt");
		if (!logFile.exists()) {
			System.out.println("Creating log file " + logFile.getAbsolutePath());
			try {
				FileUtils.write(logFile, "");
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		String queryString = null;
		try {
			queryString = FileUtils.readFileToString(lf);
		} catch (IOException e1) {
			e1.printStackTrace();
			System.exit(-1);
		}
		Query query = QueryFactory.create(queryString.replace("?n", n), Syntax.syntaxARQ);
		ResultSet rs = new QueryProcessor(query, dataset).query();
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
			if (log.contains(c + " is valid") || QueryUtil.getPathFromClassToClass(dataset, root, c).isEmpty()) {
				continue;
			} else {
				String qmsg = c + " is a lazy classifier";
				addLogBlock("LazyClassifier", qmsg);
				String[] options = new String[] { "Valid", "Abandon classifier" };
				String[] ws = new String[1];
				ws[0] = "https://en.wikipedia.org/wiki/Category:" + c;

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

				SupportFrame ps = new SupportFrame(qmsg, options, map, ws, true, true, info);

				int r = ps.getOption();
				ps.dispose();

				assert r >= 0 && r < 2;
				if (r == 0) {
					addLogEntry("LazyClassifier", c + " is valid");
					continue;
				}
				if (r == 1) {
					addLogEntry("LazyClassifier", "Abandon classifier : " + c);
					f = true;
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					PruneUtil.abandonSelected(tm.get("SubclassifiersABA"), tm.get("Classified instancesABA"),
							subclassifiers, instances, "LazyClassifier", dataset);
					PruneUtil.removeClassifierRelationships(tm.get("SubclassifiersDEL"),
							tm.get("Classified instancesDEL"), subclassifiers, instances, c, "LazyClassifier", dataset);
					new Prune(dataset).collapseClassifier(c);
				}
			}
		}
		if (f) {
			fixLazyClassifier(n);
		}

	}

	private static void fixRedundancies() {
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
		PruningTopology.root = "Computer languages";
		clean();
	}
}
