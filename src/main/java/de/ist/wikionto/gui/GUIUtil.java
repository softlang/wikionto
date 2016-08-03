package de.ist.wikionto.gui;

import java.awt.Component;
import java.awt.Container;
import java.awt.GridBagConstraints;

public class GUIUtil {

	public static void addComponentToContainer(int x, int y, int widthx, int widthy, int ipadx, int ipady, Container a,
			Component c) {
		GridBagConstraints gc = new GridBagConstraints();
		gc.gridx = x;
		gc.gridy = y;
		gc.gridwidth = widthx;
		gc.weighty = widthy;
		gc.anchor = java.awt.GridBagConstraints.NORTHWEST;
		gc.ipadx = ipadx;
		gc.ipady = ipady;
		gc.insets = new java.awt.Insets(1, 1, 1, 1);
		gc.fill = java.awt.GridBagConstraints.NORTH;
		a.add(c, gc);
	}
}
