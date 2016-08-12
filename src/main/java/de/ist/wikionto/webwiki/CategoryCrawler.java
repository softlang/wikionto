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
 *
 *         This runnable processes a category: 1) It retrieves subcategories. 2)
 *         It retrieves contained articles and processes them. 3) It retrieves
 *         supercategories.
 *
 *         Requests to the Wikipedia API are repeated until they are successful.
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
		while (true) {
			try {
				subcats = new Wiki().getCategoryMembers(type.getName(), Wiki.CATEGORY_NAMESPACE);
				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processSubCategories for " + type.getName());
			}
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
		while (true) {
			try {
				articles = new Wiki().getCategoryMembers(type.getName(), Wiki.MAIN_NAMESPACE);
				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processEntities for " + type.getName());
				e.printStackTrace();
			}
		}

		for (String name : articles) {
			if (name.contains("List of")) {
				continue;
			}
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
		while (true) {
			try {
				cs = w.getCategories(name, false, true);
				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processEntity for :" + name);
			}
		}
		for (String c : cs) {
			entity.addClassifier(c.replace("Category:", ""));
		}
		return entity;
	}

	private void processCategory() {
		Wiki w = new Wiki();
		String[] supercatgories = null;
		while (true) {
			try {
				supercatgories = w.getCategories("Category:" + type.getName(), false, true);
				assert supercatgories.length > 0;
				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processCategory for :" + type.getName());
			}
		}
		for (String c : supercatgories) {
			type.addClassifier(c.replace("Category:", ""));
		}
	}

}
