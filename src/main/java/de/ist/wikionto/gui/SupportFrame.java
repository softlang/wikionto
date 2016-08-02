package de.ist.wikionto.gui;

import java.awt.GridBagLayout;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JToggleButton;

public class SupportFrame extends JFrame {

	private static final long serialVersionUID = 1L;
	private int chosenoption = -1;

	private final String queryResult;
	private final String[] options;
	private final Map<String, List<String>> labelledlists;
	private final Map<String, List<JToggleButton>> toggleMap;
	private final String[] websites;
	private final boolean aba;
	private final boolean del;
	private final String info;

	public SupportFrame(String queryResult,String[] options, Map<String, List<String>> labelledlists, String[] websites, boolean aba,
			boolean del, String info) {
		this.queryResult = queryResult;
		this.options = options;
		this.labelledlists = labelledlists;
		this.toggleMap = new HashMap<>();
		this.websites = websites;
		this.aba = aba;
		this.del = del;
		this.info = info;
		initializeComponents();
	}

	/**
	 * Scrollbars are titled
	 * 
	 */
	private void initializeComponents() {
		setTitle("Interactive Pruning Support");
		setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
		getContentPane().setLayout(new GridBagLayout());
		
		JLabel qResult = new JLabel();
		qResult.setText(queryResult);
		GUIUtil.addComponentToContainer(0, 0, 1, 1, 0, 0, getContentPane(), qResult);
		
		
		JPanel listspanel = new JPanel();
		listspanel.setLayout(new GridBagLayout());
		GUIUtil.addComponentToContainer(0, 1, 1, 1, 0, 0, getContentPane(), listspanel);

		JPanel buttonpanel = new JPanel();
		buttonpanel.setLayout(new GridBagLayout());
		GUIUtil.addComponentToContainer(0, 2, 1, 1, 0, 0, getContentPane(), buttonpanel);
		int i = 1;
		if (options[0].equals("?")) {
			JButton ob = new JButton("?");
			ob.addActionListener(e -> {
				for (String w : websites) {
					try {
						java.awt.Desktop.getDesktop().browse(new URI(w.replaceAll(" ", "_")));
						Thread.sleep(1000);
					} catch (InterruptedException | IOException | URISyntaxException a) {
						System.err.println("Failed to open " + w);
						a.printStackTrace();
					}
				}
			});
			GUIUtil.addComponentToContainer(0, 0, 1, 1, 10, 10, buttonpanel, ob);
		} else {
			i = 0;
		}
		// options to buttons
		for (; i < options.length; i++) {
			String o = options[i];
			JButton ob = new JButton(o);
			final int j = i;
			ob.addActionListener(e -> {
				System.out.println(j);
				chosenoption = j;
			});
			GUIUtil.addComponentToContainer(i, 0, 1, 1, 10, 10, buttonpanel, ob);
		}

		JButton infob = new JButton("Help");
		infob.setToolTipText("Provides information on what to do.");
		infob.addActionListener(e -> JOptionPane.showMessageDialog(this, info));
		GUIUtil.addComponentToContainer(options.length, 0, 1, 1, 10, 10, buttonpanel, infob);

		int j = 0;
		for (String l : labelledlists.keySet()) {
			if(labelledlists.get(l).isEmpty()){
				continue;
			}else{
				System.out.println("Not Empty laballists "+labelledlists.get(l).size());
				labelledlists.get(l).forEach(la -> System.out.println(la));
			}
			List<JToggleButton> toggleList = new ArrayList<>();
			JScrollPane scrollList = new JScrollPane();
			
			scrollList.setBorder(javax.swing.BorderFactory.createTitledBorder(l));
			JPanel listpanel = new JPanel();
			listpanel.setLayout(new GridBagLayout());
			scrollList.setViewportView(listpanel);
			scrollList.setMinimumSize(new java.awt.Dimension(500, 200));
			GUIUtil.addComponentToContainer(j, 1, 1, 1, 0, 0, listspanel, scrollList);
			

			int k = 0;
			for (String e : labelledlists.get(l)) {
				JLabel label = new JLabel(getName(e));
				GUIUtil.addComponentToContainer(0, k, 1, 1, 0, 0, listpanel, label);

				JButton wb = new JButton("?");
				wb.addActionListener(ev -> {
					try {
						java.awt.Desktop.getDesktop().browse(new URI(e.replaceAll(" ", "_")));
						Thread.sleep(100);
					} catch (InterruptedException | IOException | URISyntaxException a) {
						System.err.println("Failed to open " + e);
						a.printStackTrace();
					}
				});
				GUIUtil.addComponentToContainer(1, k, 1, 1, 0, 0, listpanel, wb);

				if (aba) {
					JToggleButton abutton = new javax.swing.JToggleButton("Aba");
					abutton.setToolTipText("The member is abandoned, if this button is toggled.");
					GUIUtil.addComponentToContainer(2, k, 1, 1, 0, 0, listpanel, abutton);
					toggleList.add(abutton);
				}

				if (del) {
					JToggleButton dbutton = new javax.swing.JToggleButton("Del");
					dbutton.setToolTipText("Removes relationship to this member.");
					GUIUtil.addComponentToContainer(3, k, 1, 1, 0, 0, listpanel, dbutton);
					toggleList.add(dbutton);
				}
				k++;

			}
			toggleMap.put(l, toggleList);
			j++;
		}
		setMaximumSize(new java.awt.Dimension(100,100));
		
		pack();
	}

	public Map<String, List<JToggleButton>> getToggleMap() {
		return toggleMap;
	}

	public int getOption() {
		System.out.println("Calling getOption");
		while (chosenoption == -1) {
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		return chosenoption;
	}

	private String getName(String link) {
		String r = link.replace("https://en.wikipedia.org/wiki/", "").replace("Category:", "").replaceAll("_", " ");
		return r;
	}

	public static void main(String[] args) {
		Map<String, List<String>> m = new HashMap<>();
		String l = "Instances";
		List<String> vs = new ArrayList<>();
		for(int i = 0; i<50;i++){
			vs.add("https://en.wikipedia.org/wiki/Haskell_(programming_language)");
			vs.add("https://en.wikipedia.org/wiki/Java_(programming_language)");
		}
		m.put(l, vs);
		l = "Subclassifiers";
		vs = new ArrayList<>();
		vs.add("https://en.wikipedia.org/wiki/Category:JVM_programming_languages");
		vs.add("https://en.wikipedia.org/wiki/Category:Concurrent_programming_languages");
		m.put(l, vs);
		SupportFrame ps = new SupportFrame("Haskell is a lazy category.",new String[] { "?", "Yes", "No" }, m,
				new String[] { "https://en.wikipedia.org/wiki/Main Page" }, true, true, "info");
		ps.setVisible(true);
		int o = ps.getOption();
		ps.dispose();
		System.out.println(o);
		Map<String, List<JToggleButton>> tm = ps.getToggleMap();
		for (String s : tm.keySet()) {
			System.out.println(s);
			for (JToggleButton t : tm.get(s)) {
				System.out.println(t.isSelected());
			}
		}
	}
}
