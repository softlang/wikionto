package de.ist.wikionto.gui;

import java.awt.GridBagLayout;
import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import javax.swing.GroupLayout.ParallelGroup;
import javax.swing.GroupLayout.SequentialGroup;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTabbedPane;
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

	public SupportFrame(String queryResult, String[] options, Map<String, List<String>> labelledlists,
			String[] websites, boolean aba, boolean del, String info) {
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

	private void initializeComponents() {
		setTitle("Interactive Pruning Support");
		setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);
		JPanel qrPanel = new JPanel();
		qrPanel.setBorder(javax.swing.BorderFactory.createTitledBorder("Bad Smell Match"));
		// qrPanel.setLayout(new GridBagLayout());
		JLabel qResult = new JLabel();
		qResult.setText(queryResult);
		qrPanel.add(qResult);

		JTabbedPane tabPane = new JTabbedPane();

		JPanel buttonpanel = new JPanel();
		buttonpanel.setBorder(javax.swing.BorderFactory.createTitledBorder("Options"));

		javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
		getContentPane().setLayout(layout);
		layout.setHorizontalGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup().addContainerGap()
						.addGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.TRAILING)
								.addComponent(qrPanel, javax.swing.GroupLayout.Alignment.LEADING,
										javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE,
										Short.MAX_VALUE)
								.addComponent(tabPane, javax.swing.GroupLayout.DEFAULT_SIZE, 500, 500)
								.addComponent(buttonpanel, javax.swing.GroupLayout.Alignment.LEADING,
										javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE,
										Short.MAX_VALUE))
						.addContainerGap()));
		layout.setVerticalGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
				.addGroup(layout.createSequentialGroup()
						.addComponent(qrPanel, javax.swing.GroupLayout.PREFERRED_SIZE,
								javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
						.addComponent(tabPane, javax.swing.GroupLayout.PREFERRED_SIZE, 500, 500)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
						.addComponent(buttonpanel, javax.swing.GroupLayout.PREFERRED_SIZE,
								javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
						.addContainerGap(javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)));

		// options to buttons
		buttonpanel.setLayout(new GridBagLayout());
		JButton infob = new JButton("Instructions");
		infob.setToolTipText("Provides information on what to do.");
		infob.addActionListener(e -> JOptionPane.showMessageDialog(this, info));
		GUIUtil.addComponentToContainer(0, 0, 1, 1, 10, 10, buttonpanel, infob);
		JButton b = new JButton("Wiki");
		b.addActionListener(e -> {
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
		GUIUtil.addComponentToContainer(1, 0, 1, 1, 10, 10, buttonpanel, b);
		for (int i = 0; i < options.length; i++) {
			String o = options[i];
			JButton ob = new JButton(o);
			int j = i;
			ob.addActionListener(e -> {
				chosenoption = j;
			});
			GUIUtil.addComponentToContainer(2 + i, 0, 1, 1, 10, 10, buttonpanel, ob);
		}

		// filling in taxonomic relationships
		for (String l : labelledlists.keySet()) {

			JPanel listpanel = new JPanel();
			layout = new javax.swing.GroupLayout(listpanel);
			listpanel.setLayout(layout);
			JScrollPane scroll = new JScrollPane(listpanel);
			tabPane.addTab(l, scroll);

			List<JToggleButton> toggleList = new ArrayList<>();

			ParallelGroup pargroup = layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING);
			SequentialGroup seqgroup = layout.createSequentialGroup();
			for (String e : labelledlists.get(l)) {
				JLabel label = new JLabel(getName(e));
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
				SequentialGroup hgroup = layout.createSequentialGroup();
				hgroup = hgroup.addComponent(label, javax.swing.GroupLayout.DEFAULT_SIZE, 63, Short.MAX_VALUE)
						.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED).addComponent(wb);
				ParallelGroup vgroup = layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
						.addComponent(label).addComponent(wb);

				if (aba) {
					JToggleButton abutton = new javax.swing.JToggleButton("Aba");
					abutton.setToolTipText("The member is abandoned, if this button is toggled.");
					hgroup = hgroup.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
							.addComponent(abutton);
					vgroup = vgroup.addComponent(abutton);
					toggleList.add(abutton);
				}

				if (del) {
					JToggleButton dbutton = new javax.swing.JToggleButton("Del");
					dbutton.setToolTipText("Removes relationship to this member.");
					hgroup = hgroup.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
							.addComponent(dbutton);
					vgroup = vgroup.addComponent(dbutton);
					toggleList.add(dbutton);
				}
				// add horizontal group to layout
				pargroup = pargroup.addGroup(hgroup);
				// add vertical group to layout
				seqgroup = seqgroup.addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
						.addGroup(vgroup);
			}
			seqgroup = seqgroup.addContainerGap();
			layout.setHorizontalGroup(layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
					.addGroup(layout.createSequentialGroup().addGap(5, 5, 5).addGroup(pargroup).addContainerGap(5,
							Short.MAX_VALUE)));
			layout.setVerticalGroup(
					layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING).addGroup(seqgroup));
			toggleMap.put(l, toggleList);
		}

		pack();
	}

	public Map<String, List<JToggleButton>> getToggleMap() {
		return toggleMap;
	}

	public int getOption() {
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
}
