/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki.model;

import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author Marcel
 */
public class Instance extends Element {

	private String text;
	private final Set<Element> links;
	// private final List<Information> informationList;

	public Instance() {
		super();
		this.text = null;
		this.links = new HashSet<>();
		// informationList = new ArrayList<>();
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public Set<Element> getLinks() {
		return links;
	}

	public void addLink(Element e) {
		links.add(e);
	}

	/**
	 * public List<Information> getInformationList() { return
	 * Collections.unmodifiableList(informationList); }
	 * 
	 * public void addInformation(Information information) {
	 * informationList.add(information); }
	 **/
}
