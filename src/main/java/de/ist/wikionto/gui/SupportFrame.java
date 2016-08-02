package de.ist.wikionto.gui;

import java.awt.GridBagConstraints;
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

	private final String[] options;
	private final Map<String, List<String>> labelledlists;
	private final Map<String, List<JToggleButton>> toggleMap;
	private final String[] websites;
	private final boolean aba;
	private final boolean del;
	private final String info;

	public SupportFrame(String[] options, Map<String, List<String>> labelledlists, String[] websites, boolean aba,
			boolean del, String info) {
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
		java.awt.GridBagConstraints gc;
		setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
		getContentPane().setLayout(new GridBagLayout());

		JPanel listspanel = new JPanel();
		listspanel.setLayout(new GridBagLayout());
		gc = new GridBagConstraints();
		gc.gridx = 0;
		gc.gridy = 0;
		gc.anchor = GridBagConstraints.NORTHWEST;
		gc.weightx = 1;
		gc.weighty = 1;
		getContentPane().add(listspanel, gc);

		JPanel buttonpanel = new JPanel();
		buttonpanel.setLayout(new GridBagLayout());
		gc = new GridBagConstraints();
		gc.gridx = 0;
		gc.gridy = 1;
		gc.anchor = GridBagConstraints.NORTHWEST;
		gc.weightx = 1;
		gc.weighty = 1;
		getContentPane().add(buttonpanel, gc);
		int i = 1;
		if (options[0].equals("?")) {
			JButton ob = new JButton("?");
			ob.addActionListener(e -> {
				for (String w : websites) {
					try {
						java.awt.Desktop.getDesktop().browse(new URI(w.replaceAll(" ", "_")));
					} catch (IOException | URISyntaxException a) {
						System.err.println("Failed to open " + w);
						a.printStackTrace();
					}
				}
			});
			gc = new GridBagConstraints();
			gc.gridx = 0;
			gc.gridy = 0;
			gc.anchor = GridBagConstraints.NORTHWEST;
			gc.ipadx = 10;
			gc.ipady = 10;
			gc.insets = new java.awt.Insets(10, 10, 10, 10);
			buttonpanel.add(ob, gc);
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
			gc = new GridBagConstraints();
			gc.gridx = i;
			gc.gridy = 0;
			gc.anchor = GridBagConstraints.NORTHWEST;
			gc.ipadx = 10;
			gc.ipady = 10;
			gc.insets = new java.awt.Insets(10, 10, 10, 10);
			buttonpanel.add(ob, gc);
		}

		JButton infob = new JButton("Help");
		infob.setToolTipText("Provides information on what to do.");
		infob.addActionListener(e -> JOptionPane.showMessageDialog(this, info));
		gc = new GridBagConstraints();
		gc.gridx = options.length;
		gc.gridy = 0;
		gc.anchor = GridBagConstraints.NORTHWEST;
		gc.ipadx = 10;
		gc.ipady = 10;
		gc.insets = new java.awt.Insets(10, 10, 10, 10);
		buttonpanel.add(infob, gc);

		int j = 0;

		for (String l : labelledlists.keySet()) {
			List<JToggleButton> toggleList = new ArrayList<>();
			JScrollPane scrollList = new JScrollPane();
			scrollList.setBorder(javax.swing.BorderFactory.createTitledBorder(l));
			JPanel listpanel = new JPanel();
			listpanel.setLayout(new GridBagLayout());

			scrollList.setViewportView(listpanel);
			gc = new GridBagConstraints();
			gc.gridx = j;
			gc.gridy = 1;
			gc.anchor = GridBagConstraints.NORTHWEST;
			gc.ipadx = 10;
			gc.ipady = 10;
			gc.insets = new java.awt.Insets(10, 10, 10, 10);
			listspanel.add(scrollList, gc);

			int k = 0;
			for (String e : labelledlists.get(l)) {
				JLabel label = new JLabel(getName(e));
				gc = new GridBagConstraints();
				gc.gridx = 0;
				gc.gridy = k;
				gc.anchor = GridBagConstraints.NORTHWEST;
				gc.ipadx = 10;
				gc.ipady = 10;
				gc.insets = new java.awt.Insets(10, 10, 10, 10);
				listpanel.add(label, gc);

				JButton wb = new JButton("?");
				wb.addActionListener(ev -> {
					try {
						java.awt.Desktop.getDesktop().browse(new URI(e));
					} catch (IOException | URISyntaxException a) {
						System.err.println("Failed to open " + e);
						a.printStackTrace();
					}
				});
				gc = new GridBagConstraints();
				gc.gridx = 1;
				gc.gridy = k;
				gc.anchor = GridBagConstraints.NORTHWEST;
				gc.ipadx = 10;
				gc.ipady = 10;
				gc.insets = new java.awt.Insets(10, 10, 10, 10);
				listpanel.add(wb, gc);

				if (aba) {
					JToggleButton abutton = new javax.swing.JToggleButton("Aba");
					abutton.setToolTipText("The member is abandoned, if this button is toggled.");
					gc = new GridBagConstraints();
					gc.gridx = 2;
					gc.gridy = k;
					gc.anchor = GridBagConstraints.NORTHWEST;
					gc.ipadx = 10;
					gc.ipady = 10;
					gc.insets = new java.awt.Insets(10, 10, 10, 10);
					listpanel.add(abutton, gc);
					toggleList.add(abutton);
				}

				if (del) {
					JToggleButton dbutton = new javax.swing.JToggleButton("Del");
					dbutton.setToolTipText("Removes relationship to this member.");
					gc = new GridBagConstraints();
					gc.gridx = 3;
					gc.gridy = k;
					gc.anchor = GridBagConstraints.NORTHWEST;
					gc.ipadx = 10;
					gc.ipady = 10;
					gc.insets = new java.awt.Insets(10, 10, 10, 10);
					listpanel.add(dbutton, gc);
					toggleList.add(dbutton);
				}

				k++;

			}

			toggleMap.put(l, toggleList);
			j++;
		}

		pack();
	}

	public Map<String, List<JToggleButton>> getToggleMap() {
		return toggleMap;
	}

	public int getOption() {
		System.out.println("Calling getOption");
		long time = System.nanoTime();
		long timed = 0;
		long time2;
		while (chosenoption == -1) {
			time2 = System.nanoTime();
			timed += time2 - time;
			time = time2;
		}
		System.out.println("Time needed : " + timed);
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
		vs.add("https://en.wikipedia.org/wiki/Haskell_(programming_language)");
		vs.add("https://en.wikipedia.org/wiki/Java_(programming_language)");
		m.put(l, vs);
		l = "Subclassifiers";
		vs = new ArrayList<>();
		vs.add("https://en.wikipedia.org/wiki/Category:JVM_programming_languages");
		vs.add("https://en.wikipedia.org/wiki/Category:Concurrent_programming_languages");
		m.put(l, vs);
		SupportFrame ps = new SupportFrame(new String[] { "?", "Yes", "No" }, m,
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
