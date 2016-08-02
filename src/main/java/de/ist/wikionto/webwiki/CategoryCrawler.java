/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki;

import java.io.IOException;

import de.ist.wikionto.webwiki.model.Classifier;
import de.ist.wikionto.webwiki.model.Instance;

/**
 *
 * @author Marcel
 */
public class CategoryCrawler implements Runnable {

	private final MyCrawlerManager manager;

	private final Classifier type;

	public CategoryCrawler(MyCrawlerManager manager, Classifier type) {
		this.manager = manager;
		this.type = type;
	}

	@Override
	public void run() {
		processCategory();

		processSubCategories();

		processEntities();

		manager.decthreadcounter();
	}

	/**
	 * Adds Subcategories to type and offers them to the manager's type queue.
	 */
	private void processSubCategories() {
		String[] subcats = null;
		try {
			subcats = (new Wiki()).getCategoryMembers(type.getName(), Wiki.CATEGORY_NAMESPACE);
		} catch (IOException e) {
			e.printStackTrace();
		}
		for (String name : subcats) {
			if (manager.isExcludedCategoryName(name.trim())) {
				continue;
			}
			String sname = name.replace("Category:", "").trim();
			Classifier subtype = manager.getClassifierFromClassifierMap(sname);
			if (null == subtype) {
				subtype = new Classifier();
				subtype.setName(sname);
				manager.putInClassifierMap(sname, subtype);
				manager.offerClassifier(subtype);
			}
			subtype.setMinDepth(type.getMinDepth() + 1);
			type.addSubclassifier(subtype);
		}
	}

	private void processEntities() {
		String[] articles = null;
		try {
			articles = (new Wiki()).getCategoryMembers(type.getName(), Wiki.MAIN_NAMESPACE);
		} catch (IOException e) {
			e.printStackTrace();
		}

		for (String name : articles) {
			if (name.contains("List of"))
				continue;
			Instance entity = manager.getInstanceFromInstanceMap(name);

			if (null == entity) {
				entity = processentity(name);
				manager.putInInstanceMap(name, entity);
			}
			type.addInstance(entity);
		}
	}

	private Instance processentity(String name) {
		Instance entity = new Instance();
		entity.setName(name);

		Wiki w = new Wiki();
		String[] cs;
		try {
			cs = w.getCategories(name, false, true);
			for (String c : cs) {
				entity.addClassifier(c.replace("Category:", ""));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}

		return entity;
	}

	private void processCategory() {
		Wiki w = new Wiki();
		String[] cs;
		try {
			cs = w.getCategories("Category:" + type.getName(), false, true);
			assert (cs.length > 0);
			for (String c : cs) {
				type.addClassifier(c.replace("Category:", ""));
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
