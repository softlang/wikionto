/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki.model;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;

/**
 *
 * @author Marcel
 */
public class Classifier extends Element {

	private final Set<Classifier> subclassifiers;
	private final Set<Instance> instances;
	private final Set<Element> mainLinks;
	private String text;

	private Instance description;

	private int minDepth;

	public Classifier() {
		super();
		subclassifiers = new HashSet<>();
		instances = new HashSet<>();
		text = null;
		mainLinks = new HashSet<>();
	}

	public Set<Classifier> getSubclassifiers() {
		return Collections.unmodifiableSet(subclassifiers);
	}

	public void addMainLink(Element e) {
		this.mainLinks.add(e);
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getText() {
		return text;
	}

	public Set<Element> getMainLinks() {
		return mainLinks;
	}

	public void addSubclassifier(Classifier sub) {
		if (!subclassifiers.contains(sub)) {
			subclassifiers.add(sub);
			sub.addClassifier(this.getName());
		}
	}

	public Set<Instance> getInstances() {
		return Collections.unmodifiableSet(instances);
	}

	public void addInstance(Instance instance) {
		if (!instances.contains(instance)) {
			instances.add(instance);
		}
	}

	public Instance getDescription() {
		return description;
	}

	public void setDescription(Instance description) {
		this.description = description;
	}

	public int getMinDepth() {
		return minDepth;
	}

	public void setMinDepth(int minDepth) {
		if (this.minDepth == 0 || this.minDepth > minDepth)
			this.minDepth = minDepth;
	}
}
