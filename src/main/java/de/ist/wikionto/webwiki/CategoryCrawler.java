/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.webwiki;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

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
		if (manager.getMaxDepth() == type.getMinDepth()) {
			return;
		}
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
		Set<String> artLinks = resolveLinks(articles);
		for (String name : artLinks) {
			if (name.contains("List of")) {
				continue;
			}
			Instance entity = manager.getInstanceFromInstanceMap(name);

			if (null == entity) {
				entity = processEntity(name);
				manager.putInInstanceMap(name, entity);
			}
			type.addInstance(entity);
		}
	}

	private Instance processEntity(String name) {
		Instance entity = new Instance();
		entity.setName(name);
		Set<String> links = new HashSet<>();
		Wiki w = new Wiki();
		String[] cs;
		while (true) {
			try {
				cs = w.getCategories(name, false, true);
				String text = w.getRenderedText(name);
				entity.setText(text);
				String first = getFirstSentence(text);
				entity.setFirst(first);
				links = this.resolveLinks(w.getLinksOnPage(name));
				entity.getLinks().addAll(links);
				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processEntity for :" + name);
			}
		}
		for (String c : cs) {
			entity.addCategory(c.replace("Category:", ""));
		}
		return entity;
	}

	private void processCategory() {
		Wiki w = new Wiki();
		String[] supercatgories = null;
		Set<String> links = new HashSet<>();
		while (true) {
			try {
				supercatgories = w.getCategories("Category:" + type.getName(), false, true);
				assert supercatgories.length > 0;
				String text = w.getRenderedText("Category:" + type.getName());
				type.setText(text);
				links = resolveLinks(w.getLinksOnPage("Category:" + type.getName()));
				type.getMainLinks().addAll(links);

				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processCategory for :" + type.getName());
			}
		}
		for (String c : supercatgories) {
			type.addCategory(c.replace("Category:", ""));
		}
	}

	private Set<String> resolveLinks(String[] links) {
		Set<String> set = new HashSet<>();
		Wiki wiki = new Wiki();
		while (true) {
			try {
				String[] resolved = wiki.resolveRedirects(links);
				for (int i = 0; i < links.length; i++) {
					if (resolved[i] == null) {
						set.add(links[i]);
					} else {
						set.add(resolved[i]);
					}
				}
				break;
			} catch (IOException e) {
				System.err.println("Connection issue at processLinks for :" + type.getName());
			}
		}
		return set;
	}

	private static String getFirstSentence(String html) {
		Document doc = Jsoup.parse(html);
		Elements es = doc.select("div.mw-parser-output");
		for (Element e : es) {
			Elements childs = e.children();
			for (Element child : childs) {
				if (child.select("img").isEmpty() && child.select("table").isEmpty() && !child.is("div.hatnote")
						&& !child.is("div.noprint") && !child.is("dl"))
					return child.text();
			}
		}
		return "";
	}

}
