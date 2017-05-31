/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki.model;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author Marcel
 */
public class Instance extends Element {

	private String text;
	private String first;
	private Set<String> links;
	// private final List<Information> informationList;

	public Instance() {
		super();
		this.text = null;
		this.setFirst(null);
		this.links = new HashSet<>();
		// informationList = new ArrayList<>();
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public Set<String> getLinks() {
		return links;
	}

	public void addLink(String e) {
		links.add(e);
	}

	public void addLinks(Collection<String> links) {
		links.addAll(links);
	}

	public String getFirst() {
		return first;
	}

	public void setFirst(String first) {
		this.first = first;
	}

	/**
	 * public List<Information> getInformationList() { return
	 * Collections.unmodifiableList(informationList); }
	 * 
	 * public void addInformation(Information information) {
	 * informationList.add(information); }
	 **/
}
