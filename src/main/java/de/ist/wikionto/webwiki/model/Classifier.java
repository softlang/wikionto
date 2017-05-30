/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki.model;

import java.util.Collection;
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
	private final Set<String> mainLinks;
	private String text;

	private int minDepth;

	public Classifier() {
		super();
		subclassifiers = Collections.synchronizedSet(new HashSet<>());
		instances = Collections.synchronizedSet(new HashSet<>());
		mainLinks = Collections.synchronizedSet(new HashSet<>());
	}

	public Set<Classifier> getSubclassifiers() {
		return Collections.unmodifiableSet(subclassifiers);
	}

	public void addMainLink(String e) {
		mainLinks.add(e);
	}

	public void addMainLinks(Collection<String> links) {

		mainLinks.addAll(links);
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getText() {
		return text;
	}

	public Set<String> getMainLinks() {
		return mainLinks;
	}

	public synchronized void addSubclassifier(Classifier sub) {
		if (!subclassifiers.contains(sub)) {
			subclassifiers.add(sub);
			sub.addCategory(getName());
		}
	}

	public Set<Instance> getInstances() {
		return Collections.unmodifiableSet(instances);
	}

	public synchronized void addInstance(Instance instance) {
		if (!instances.contains(instance)) {
			instances.add(instance);
		}
	}

	public int getMinDepth() {
		return minDepth;
	}

	public void setMinDepth(int minDepth) {
		if (this.minDepth == 0 || this.minDepth > minDepth) {
			this.minDepth = minDepth;
		}
	}
}
