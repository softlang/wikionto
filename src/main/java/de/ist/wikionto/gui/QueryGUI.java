package de.ist.wikionto.gui;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Date;
import java.util.List;

import javax.swing.JButton;
import javax.swing.JEditorPane;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryFactory;
import com.hp.hpl.jena.query.QueryParseException;
import com.hp.hpl.jena.query.Syntax;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.triplestore.query.QueryAreaStream;
import de.ist.wikionto.triplestore.query.QueryProcessor;

public class QueryGUI extends JFrame {

	private static final long serialVersionUID = -3569182093322580096L;

	private Dataset dataset;
	private JLabel lolabel;
	private JLabel lqlabel;
	private Path queryPath;
	private JEditorPane queryResultArea;

	public QueryGUI() {
		initComponents();
		setVisible(true);
	}

	private void initComponents() {
		setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
		getContentPane().setLayout(new java.awt.GridBagLayout());

		lolabel = new javax.swing.JLabel();
		lqlabel = new javax.swing.JLabel();

		JScrollPane scroll = new javax.swing.JScrollPane();
		GUIUtil.addComponentToContainer(0, 2, 3, 1, 800, 600, getContentPane(), scroll);
		queryResultArea = new JEditorPane();
		scroll.setViewportView(queryResultArea);

		JButton lo = new javax.swing.JButton();
		lo.setText("load ontology");
		lo.addActionListener(e -> loadOntology());
		GUIUtil.addComponentToContainer(0, 0, 1, 1, 10, 10, getContentPane(), lo);

		JButton lq = new javax.swing.JButton();
		lq.setText("load query");
		lq.addActionListener(e -> loadQuery());
		GUIUtil.addComponentToContainer(1, 0, 1, 1, 10, 10, getContentPane(), lq);

		JButton q = new javax.swing.JButton();
		q.setText("query");
		q.addActionListener(e -> query());
		GUIUtil.addComponentToContainer(2, 0, 1, 1, 10, 10, getContentPane(), q);

		lolabel.setText("<loaded ontology>");
		GUIUtil.addComponentToContainer(0, 1, 1, 1, 10, 10, getContentPane(), lolabel);

		lqlabel.setText("<loaded query>");
		GUIUtil.addComponentToContainer(1, 1, 1, 1, 10, 10, getContentPane(), lqlabel);

		pack();
	}

	private void loadOntology() {
		if (null != dataset) {
			dataset.end();
		}
		JFileChooser fc = new JFileChooser();
		fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
		fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
		int returnVal = fc.showOpenDialog(this);
		if (returnVal == JFileChooser.APPROVE_OPTION) {
			dataset = TDBFactory.createDataset(fc.getSelectedFile().toString());
			lolabel.setText(fc.getSelectedFile().getName());
		} else {
			JOptionPane.showMessageDialog(this, "Loading ontology failed");
		}
	}

	private void loadQuery() {// GEN-FIRST:event_loadQuery
		JFileChooser fc = new JFileChooser();
		fc.setCurrentDirectory(new File(System.getProperty("user.dir") + "/sparql"));
		int returnVal = fc.showOpenDialog(this);
		if (returnVal == JFileChooser.APPROVE_OPTION) {
			queryPath = fc.getSelectedFile().toPath();

			lqlabel.setText(fc.getSelectedFile().getName());
		} else {
			JOptionPane.showMessageDialog(this, "Loading query failed");
		}
	}

	private void query() {
		List<String> lines = null;
		try {
			lines = Files.readAllLines(queryPath);
		} catch (IOException ex) {
			JOptionPane.showMessageDialog(this, "Query failed");
		}
		String queryString = "";
		for (String line : lines) {
			queryString += line + System.lineSeparator();
		}
		try {
			Query query = QueryFactory.create(queryString, Syntax.syntaxARQ);
			queryResultArea.setText("Starting query: " + queryPath.toFile().getName() + "\n");
			new QueryProcessor(query, dataset).stream(new QueryAreaStream(queryResultArea));
			System.out.println("Query end at " + new Date().toString());
		} catch (QueryParseException e) {
			queryResultArea.setText(e.getMessage());
			e.printStackTrace();
		}
	}

	public static void main(String[] args) {
		new QueryGUI();
	}
}
