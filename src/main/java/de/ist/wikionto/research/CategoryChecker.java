package de.ist.wikionto.research;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;

import de.ist.wikionto.webwiki.Wiki;

public class CategoryChecker {

	private int maxDepth;
	private Wiki wiki;
	private FileWriter logger;
	private Set<String> exclusionset;
	private boolean loging;
	private Set<String> linkExclusionSet;

	/**
	 * 
	 * @param maxDepth
	 *            maximum Depth of subcategories
	 * @param exclusionset
	 *            set of excluded domain names
	 * @param linkExclusionSet
	 *            set of excluded wikilinks
	 * @param loging
	 *            if true
	 * @throws IOException
	 */
	public CategoryChecker(int maxDepth, Set<String> exclusionset, Set<String> linkExclusionSet, boolean loging)
			throws IOException {
		super();
		this.maxDepth = maxDepth;
		this.wiki = new Wiki();
		this.wiki.setResolveRedirects(true);
		this.exclusionset = exclusionset;
		this.linkExclusionSet = linkExclusionSet;
		this.loging = loging;
		Date d = new Date();
		if (loging) {
			File file = new File("logs/log_" + d.toString() + ".log");
			file.getParentFile().mkdirs();
			file.createNewFile();
			this.logger = new FileWriter(file);
		}

	}

	public void newLog(String name) throws IOException {
		if (loging) {
			logger.flush();
			logger.close();
			logger = new FileWriter(new File("log/" + name));
		}
	}

	public void logNewline(String msg) throws IOException {
		if (loging) {
			this.logger.write(msg + '\n');
			this.logger.flush();
		}
	}

	public void log(String msg) throws IOException {
		if (loging) {
			this.logger.write(msg);
			this.logger.flush();
		}
	}

	public void logDate(String msg) throws IOException {
		if (loging) {
			Date d = new Date();
			this.logger.write(d.toString() + " : " + msg + "\n");
			this.logger.flush();
		}
	}

	public Map<String, Set<String>> getCategoryLinkList(String root) throws IOException {
		this.logNewline("Category : wikilinks");
		Map<String, Set<String>> result = new HashMap<String, Set<String>>();
		Set<String> cats = new TreeSet<String>();
		gatherCategories(root, cats, 0);
		cats.forEach(cat -> result.put(cat, this.getLinks(cat)));
		int multiple = 0;
		int empty = 0;
		for (Set<String> links : result.values()) {
			if (links.size() == 0)
				empty++;
			else if (links.size() > 1)
				multiple++;
		}
		this.logNewline("Total Number of categories : " + cats.size());
		this.logNewline("Number of categories without links: " + empty);
		this.logNewline("Number of categories with multiple links: " + multiple);
		return result;
	}

	public void gatherCategories(String cat, Set<String> set, int depth) throws IOException {
		if (depth <= this.maxDepth && set.add(cat)) {
			if (isExcluded(cat, this.exclusionset)) {
				set.remove(cat);

			} else {
				// this.logNewline(cat);
				for (String s : wiki.getCategoryMembers(cat, false, Wiki.CATEGORY_NAMESPACE)) {
					gatherCategories(s, set, depth + 1);
				}
			}
		} else {
			return;
		}

	}

	public boolean isExcluded(String cat, Set<String> exclusionSet) {
		for (String s : exclusionSet)
			if (cat.toLowerCase().contains(s.toLowerCase())) {
				return true;
			}
		return false;
	}

	public Set<String> getLinks(String site) {
		Set<String> result = new HashSet<>();
		String[] resolved;
		String[] links;

		try {
			links = this.wiki.getLinksOnPage(site);
			resolved = this.wiki.resolveRedirects(links);
			for (int i = 0; i < links.length; i++) {
				String link;
				if (resolved[i] == null)
					link = links[i];
				else
					link = resolved[i];
				if (!result.contains(link) && !isExcluded(link, this.linkExclusionSet)) {
					result.add(link);
				}
			}

		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;

	}

	@Deprecated
	public List<String> reduceLinks(String[] links) {
		LinkedList<String> l = new LinkedList<String>();
		for (String link : links) {
			boolean b = true;
			for (String s : this.linkExclusionSet) {
				if (link.toLowerCase().contains(s.toLowerCase())) {
					b = false;
				}

			}
			if (b)
				l.add(link);
		}
		return l;
	}

	public Map<String, Boolean> checkCategory(String cat) throws IOException {
		Map<String, Boolean> result = new HashMap<>();
		String[] articles = this.wiki.getCategoryMembers(cat, this.wiki.MAIN_NAMESPACE);
		Set<String> catLinks = this.getLinks(cat);
		for (String article : articles) {
			Set<String> artLinks = this.getLinks(article);
			boolean res = checkArticle(artLinks, catLinks);
			result.put(article, res);
			this.logNewline(article + " links " + cat + " : " + res);
		}
		return result;
	}

	public boolean checkArticle(Set<String> artLinks, Set<String> catLinks) throws IOException {
		// wäre es nicht schlauer zu sehen ob der Links was mit dem Category
		// namen zutun hat?
		boolean result = false;
		for (String link : artLinks) {
			if (catLinks.contains(link))
				result = true;
		}
		return result;
	}

	public void checkCategories(Set<String> categories) throws IOException {
		HashMap<String, Set<String>> articleLinkMap = new HashMap<>();
		int i = 0;
		int j = 0;
		for (String category : categories) {
			Set<String> catLinks = this.getLinks(category);
			String[] articles = this.wiki.getCategoryMembers(category, this.wiki.MAIN_NAMESPACE);
			for (String article : articles) {
				boolean res = false;
				i++;
				if (articleLinkMap.containsKey(article)) {
					Set<String> artLinks = articleLinkMap.get(article);
					res = this.checkArticle(artLinks, catLinks);
				} else {
					Set<String> artLinks = this.getLinks(article);
					articleLinkMap.put(article, artLinks);
					res = this.checkArticle(artLinks, catLinks);
				}
				this.logNewline("Article \"" + article + "\"" + "Catgegory \"" + category + "\"  : " + res);
				if (res)
					j++;
			}
		}
		this.logNewline("Total articles : " + i);
		this.logNewline("Total articles with link : " + j);
	}

	public Set<String> getLinks(String[] links, String[] resolved) {
		Set<String> set = new HashSet<>();
		int i = 0;
		while (i < links.length) {
			if (resolved[i] == null) {
				set.add(links[i]);
			} else {
				set.add(resolved[i]);
			}
			i++;
		}
		return set;
	}

	public static void main(String[] args) throws IOException {
		Set<String> exclusionset = new HashSet<>();
		exclusionset.add("Data types");
		exclusionset.add("Programming language topics");
		exclusionset.add("Web services");
		exclusionset.add("User BASIC");
		exclusionset.add("Lists of computer languages");
		exclusionset.add("Programming languages by creation date");
		exclusionset.add("Uncategorized programming languages");
		exclusionset.add("Wikipedia");
		exclusionset.add("Articles");
		exclusionset.add("software");
		exclusionset.add("Software that");
		exclusionset.add("Software for");
		exclusionset.add("Software programmed");
		exclusionset.add("Software written");
		exclusionset.add("Software by");
		exclusionset.add("conference");
		Set<String> linkExclusionSet = new HashSet<>();
		linkExclusionSet.add("Help:");
		// linkExclusionSet.add("Category");
		linkExclusionSet.add("Wikipedia");
		CategoryChecker c = new CategoryChecker(3, exclusionset, linkExclusionSet, false);
		System.out.println("Start");
		c.logDate("start");
		// c.checkCategory("Category:C_programming_language_family");
		Set<String> cats = new HashSet<String>();
		// c.gatherCategories("Category:Computer_languages", cats, 0);
		// c.checkCategories(cats);
		c.logDate("end");
		System.out.println("End");
		// String[] as = c.wiki.whatLinksHere("C_(programming_language)", true);
		// ystem.out.println(Arrays.toString(b));
		// System.out.println(c.wiki.resolveRedirects(c.wiki.getLinksOnPage("C_(programming_language)")).length);
		// System.out.println(c.wiki.);
		System.out.println(Arrays.toString(c.wiki.resolveRedirects(c.wiki.getLinksOnPage("C (programming language)"))));
	}

}
