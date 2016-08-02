package de.ist.wikionto;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.swing.JFileChooser;
import javax.swing.JOptionPane;
import javax.swing.JToggleButton;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.gui.SupportFrame;
import de.ist.wikionto.triplestore.query.QueryUtil;
import de.ist.wikionto.triplestore.transform.Prune;

public class PruningTopology {

	private static Dataset dataset;

	private static String logPath;

	// contains all valid eponymous classifiers
	private static Set<String> valideC = new HashSet<>();

	// contains all valid semantic distant classifiers
	private static Set<String> validSDC = new HashSet<>();

	// contains all valid semantic distant instances
	private static Set<String> validSDI = new HashSet<>();

	// maps a double reachable classifier to valid top classifiers
	private static Map<String, Set<String>> validDRC = new HashMap<>();

	// maps a double reachable instance to valid top classifiers
	private static Map<String, Set<String>> validDRI = new HashMap<>();

	// contains all valid lazy classifiers
	private static Set<String> validLC = new HashSet<>();

	public static void clean() {

		JOptionPane.showMessageDialog(null, "Welcome to our GUI support for topology based pruning of a taxonomy."
				+ "\nClick on okay to proceed and select the folder, where the TDB files for the taxonomy are saved.");
		loadTaxonomy();
		JOptionPane.showMessageDialog(null,
				"The cleaning process is built around several things. \n"
						+ "First, you should know what kind of categories you want to include or exclude"
						+ "\nfor being feasible classifiers in your taxonomy."
						+ "\nSecond, the cleaning process will guide you through each bad smell. At first"
						+ "\na description of a bad smell will be given. Then, for each bad smell we provide"
						+ "\nGUI support helping in getting rid of confirmed issues."
						+ "Further, every action you take is logged for reproducibility.");
		initializeLog();
		JOptionPane.showMessageDialog(null,
				"We start with the bad smell `Eponymous Classifier'. "
						+ "\nIt matches those classifiers for which an instance exist with the same name"
						+ "\nor where the classifier's name is the plural form of the instance's name.");

		fixEponymousType();

		fixSemanticDistantClassifier();

		fixSemanticDistantInstance();

		fixDoubleReachableClassifier();

		fixDoubleReachableInstance();

		fixCyclicClassifier();

		fixLazyClassifier();

		fixRedundancies();
	}

	private static void fixEponymousType() {
		String p = "./sparql/smells/EponymousClassifier.sparql";
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String c = qs.getLiteral("cname").getString();
			if (valideC.contains(c))
				continue;
			else {
				String[] options = new String[] { "?", "Valid", "Abandon instance", "Abandon classifier" };
				String[] links = new String[2];
				links[0] = "https://en.wikipedia.org/wiki/" + c;
				links[1] = "https://en.wikipedia.org/wiki/Category:" + c;

				String info = "By clicking on the ? button you can open a browser with "
						+ "the corresponding Wikipedia page giving you decision ground." + "Three options are provided:"
						+ "First, you can do nothing if the existence of both " + "elements in the taxonomy is okay. "
						+ "Second, you can abandon the instance, if it does not "
						+ "correspond to something you want to classify. "
						+ "Third, you can abandon the classifier and carefully "
						+ "inspect the relevance of subclassifiers and classified "
						+ "instances. For each subclassifier and instance you can "
						+ "toggle the Aba button to make sure this element is abandoned "
						+ "as well or toggle the Del button to remove the relationship "
						+ "from the classifier to the element.";

				Map<String, List<String>> map = new HashMap<>();
				List<String> instances = QueryUtil.getInstances(dataset, c);
				List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, c);
				map.put("Classified instances", instances);
				map.put("Subclassifiers", subclassifiers);
				SupportFrame ps = new SupportFrame(options, map, links, true, true, info);
				ps.setVisible(true);
				int r = ps.getOption();
				ps.dispose();

				assert (r > 0 && r < 4);
				if (r == 1) {
					valideC.add(c);
					continue;
				}
				if (r == 2) {
					f = true;
					new Prune(dataset).abandonInstance(c);
					continue;
				}
				if (r == 3) {
					f = true;
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					List<JToggleButton> list1 = tm.get("Classified instances");
					List<String> list2 = map.get("Classified Instances");
					Iterator<JToggleButton> it = list1.iterator();
					for (String l2 : list2) {
						if (it.next().isSelected()) {
							new Prune(dataset).abandonInstance(l2);
						}
						if (it.next().isSelected()) {
							new Prune(dataset).removeInstance(l2, c);
						}
					}
					list1 = tm.get("Subclassifiers");
					list2 = map.get("Subclassifiers");
					for (String l2 : list2) {
						if (it.next().isSelected()) {
							new Prune(dataset).abandonClassifier(l2);
						}
						if (it.next().isSelected()) {
							new Prune(dataset).removeSubclassifier(c, l2);
						}
					}
					new Prune(dataset).collapseType(c);
				}
			}
		}
		if (f)
			fixEponymousType();
	}

	private static void fixSemanticDistantClassifier() {
		String p = "./sparql/smells/SemanticallyDistantClassifier.sparql";
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String c = qs.getLiteral("cname").getString();
			if (validSDC.contains(c))
				continue;
			else {
				String[] options = new String[] { "?", "Valid", "Abandon classifier" };
				String[] links = new String[1];
				links[0] = "https://en.wikipedia.org/wiki/Category:" + c;

				String info = "By clicking on the ? button you can open a browser with "
						+ "the corresponding Wikipedia page giving you decision ground." + "Three options are provided:"
						+ "First, you can do nothing if the existence the classifier is feasible. "
						+ "Second, you can abandon the classifier and carefully "
						+ "inspect the relevance of subclassifiers and classified "
						+ "instances. For each subclassifier and instance you can "
						+ "toggle the Aba button to make sure this element is abandoned "
						+ "as well or toggle the Del button to remove the relationship "
						+ "from the classifier to the element.";

				Map<String, List<String>> map = new HashMap<>();
				List<String> instances = QueryUtil.getInstances(dataset, c);
				List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, c);
				map.put("Classified instances", instances);
				map.put("Subclassifiers", subclassifiers);
				SupportFrame ps = new SupportFrame(options, map, links, true, true, info);
				ps.setVisible(true);
				int r = ps.getOption();
				ps.dispose();

				assert (r > 0 && r < 3);
				if (r == 1) {
					validSDC.add(c);
					continue;
				}
				if (r == 2) {
					f = true;
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					List<JToggleButton> list1 = tm.get("Classified instances");
					List<String> list2 = map.get("Classified Instances");
					Iterator<JToggleButton> it = list1.iterator();
					for (String l2 : list2) {
						if (it.next().isSelected()) {
							new Prune(dataset).abandonInstance(l2);
						}
						if (it.next().isSelected()) {
							new Prune(dataset).removeInstance(l2, c);
						}
					}
					list1 = tm.get("Subclassifiers");
					list2 = map.get("Subclassifiers");
					for (String l2 : list2) {
						if (it.next().isSelected()) {
							new Prune(dataset).abandonClassifier(l2);
						}
						if (it.next().isSelected()) {
							new Prune(dataset).removeSubclassifier(c, l2);
						}
					}
					new Prune(dataset).collapseType(c);
				}
			}
		}
		if (f)
			fixSemanticDistantClassifier();
	}

	private static void fixSemanticDistantInstance() {
		String p = "./sparql/smells/SemanticallyDistantInstance.sparql";
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String i = qs.getLiteral("iname").getString();
			if (validSDI.contains(i))
				continue;
			else {
				String[] options = new String[] { "?", "Valid", "Abandon Instance" };
				String[] links = new String[1];
				links[0] = "https://en.wikipedia.org/wiki/" + i;

				String info = "By clicking on the ? button you can open a browser with "
						+ "the corresponding Wikipedia page giving you decision ground." + "Three options are provided:"
						+ "First, you can do nothing if the existence the instance is feasible. "
						+ "Second, you can abandon the instance. The list of classifiers is provided.";

				Map<String, List<String>> map = new HashMap<>();
				List<String> classifiers = QueryUtil.getClassifiers(dataset, i);
				map.put("Classifiers", classifiers);
				SupportFrame ps = new SupportFrame(options, map, links, false, false, info);
				ps.setVisible(true);
				int r = ps.getOption();
				ps.dispose();

				assert (r > 0 && r < 3);
				if (r == 1) {
					validSDI.add(i);
					continue;
				}
				if (r == 2) {
					f = true;

					new Prune(dataset).abandonInstance(i);
				}
			}
		}
		if (f)
			fixSemanticDistantClassifier();
	}

	private static void fixDoubleReachableClassifier() {
		String p = "./sparql/smells/DoubleReachableClassifier.sparql";
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String t = qs.getLiteral("typename").getString();
			String top1 = qs.getLiteral("toptype1name").getString();
			String top2 = qs.getLiteral("toptype2name").getString();
			if (validDRC.containsKey(t) && validDRC.get(t).contains(top1) && validDRC.get(t).contains(top2))
				continue;
			else {
				String[] options = new String[] { "?", "Valid", "Remove selected relationships" };
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
				map.put("Path from top1", list1);
				map.put("Path from top2", list2);

				SupportFrame ps = new SupportFrame(options, map, links, false, true, info);
				ps.setVisible(true);
				int r = ps.getOption();
				ps.dispose();
				assert (r > 0 && r < 3);
				if (r == 1) {
					Set<String> s;
					if (validDRC.containsKey(t)) {
						s = validDRC.get(t);
						if (!s.contains(top1)) {
							s.add(top1);
						}
						if (!s.contains(top2)) {
							s.add(top2);
						}
					} else {
						s = new HashSet<>();
						s.add(top1);
						s.add(top2);
					}
					validDRC.put(t, s);
					continue;
				}
				if (r == 2) {
					f = true;
					Map<String, List<JToggleButton>> togglemap = ps.getToggleMap();
					List<JToggleButton> toggles1 = togglemap.get("Path from top1");
					List<JToggleButton> toggles2 = togglemap.get("Path from top2");
					if (toggles1.get(0).isSelected()) {
						new Prune(dataset).removeSubclassifier(top1, list1.get(0));
					}
					for (int i = 1; i < toggles1.size(); i++) {
						if (toggles1.get(i).isSelected()) {
							new Prune(dataset).removeSubclassifier(list1.get(i - 1), list1.get(i));
						}
					}
					if (toggles2.get(0).isSelected()) {
						new Prune(dataset).removeSubclassifier(top2, list2.get(0));
					}
					for (int i = 1; i < toggles2.size(); i++) {
						if (toggles2.get(i).isSelected()) {
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
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String dri = qs.getLiteral("typename").getString();
			String top1 = qs.getLiteral("toptype1name").getString();
			String top2 = qs.getLiteral("toptype2name").getString();
			if (validDRI.containsKey(dri) && validDRI.get(dri).contains(top1) && validDRI.get(dri).contains(top2))
				continue;
			else {
				String[] options = new String[] { "?", "Valid", "Remove selected relationships" };
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
				List<String> list2 = QueryUtil.getPathFromClassToInstance(dataset, top2, dri);
				map.put("Path from top1", list1);
				map.put("Path from top2", list2);

				SupportFrame ps = new SupportFrame(options, map, links, false, true, info);
				ps.setVisible(true);
				int r = ps.getOption();
				ps.dispose();
				assert (r > 0 && r < 3);
				if (r == 1) {
					Set<String> s;
					if (validDRI.containsKey(dri)) {
						s = validDRI.get(dri);
						if (!s.contains(top1)) {
							s.add(top1);
						}
						if (!s.contains(top2)) {
							s.add(top2);
						}
					} else {
						s = new HashSet<>();
						s.add(top1);
						s.add(top2);
					}
					validDRI.put(dri, s);
					continue;
				}
				if (r == 2) {
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
							new Prune(dataset).removeInstance(list1.get(list1.size() - 1), list1.get(list1.size() - 2));
						else
							new Prune(dataset).removeInstance(list1.get(0), top1);
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
							new Prune(dataset).removeInstance(list2.get(list2.size() - 1), list2.get(list2.size() - 2));
						else
							new Prune(dataset).removeInstance(list2.get(0), top2);
					}
				}
			}
		}

		if (f)
			fixDoubleReachableInstance();
	}

	private static void fixCyclicClassifier() {
		String p = "./sparql/smells/CyclicClassifier.sparql";
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			f = true;
			QuerySolution qs = rs.next();
			String cc = qs.getLiteral("typename").getString();

			String[] options = new String[] { "?", "Remove selected relationships" };
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
			map.put("Cycle path", list1);

			SupportFrame ps = new SupportFrame(options, map, links, false, true, info);
			ps.setVisible(true);
			int r = ps.getOption();
			ps.dispose();
			assert (r == 1);
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
		ResultSet rs = QueryUtil.executeQuery(dataset, p);
		boolean f = false;
		while (rs.hasNext()) {
			QuerySolution qs = rs.next();
			String c = qs.getLiteral("cname").getString();
			if (validLC.contains(c))
				continue;
			else {
				String[] options = new String[] { "?", "Valid", "Abandon classifier" };
				String[] ws = new String[2];
				ws[1] = "https://en.wikipedia.org/wiki/Category:" + c;

				String info = "By clicking on the ? button you can open a browser with "
						+ "the corresponding Wikipedia page giving you decision ground." + "Three options are provided:"
						+ "First, you can do nothing if the existence the classifier is feasible. "
						+ "Second, you can abandon the classifier and carefully "
						+ "inspect the relevance of subclassifiers and classified "
						+ "instances. For each subclassifier and instance you can "
						+ "toggle the Aba button to make sure this element is abandoned "
						+ "as well or toggle the Del button to remove the relationship "
						+ "from the classifier to the element.";

				Map<String, List<String>> map = new HashMap<>();
				List<String> instances = QueryUtil.getInstances(dataset, c);
				List<String> subclassifiers = QueryUtil.getSubclassifiers(dataset, c);
				map.put("Classified instances", instances);
				map.put("Subclassifiers", subclassifiers);
				SupportFrame ps = new SupportFrame(options, map, ws, true, true, info);
				ps.setVisible(true);
				int r = ps.getOption();
				ps.dispose();

				assert (r > 0 && r < 3);
				if (r == 1) {
					validLC.add(c);
					continue;
				}
				if (r == 2) {
					f = true;
					Map<String, List<JToggleButton>> tm = ps.getToggleMap();
					List<JToggleButton> list1 = tm.get("Classified instances");
					Iterator<JToggleButton> it = list1.iterator();
					for (String l2 : instances) {
						if (it.next().isSelected()) {
							new Prune(dataset).abandonInstance(l2);
						}
						if (it.next().isSelected()) {
							new Prune(dataset).removeInstance(l2, c);
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
					new Prune(dataset).collapseType(c);
				}
			}
		}
		if (f)
			fixSemanticDistantClassifier();

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
					"./evaluation/logs/log" + LocalDateTime.now().toString().replaceAll(":", "").replaceAll("\\.", ""));
			f.mkdir();
			JOptionPane.showMessageDialog(null, "Creating new log files in \n" + f.getAbsolutePath());
			logPath = f.getAbsolutePath();
		}
		if (b == 0) {
			JFileChooser fc = new JFileChooser();
			fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
			fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
			int returnVal = fc.showOpenDialog(null);
			if (returnVal == JFileChooser.APPROVE_OPTION) {
				logPath = fc.getSelectedFile().getAbsolutePath();
			} else {
				JOptionPane.showMessageDialog(null, "Loading log folder failed. Please restart!");
				System.exit(0);
			}
		}

	}

	public static void addLogBlock(String smellname, String queryresults) {
		String e = "\n" + queryresults;

		File f = new File(logPath + "/" + smellname + ".txt");
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

		File f = new File(logPath + "/" + smellname + ".txt");
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

	}
}
