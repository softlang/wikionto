package de.ist.wikionto.research.temp;

import java.util.Map;

import de.ist.wikionto.research.MyLogger;

public class Hypernym extends Transformation {

	private String query = "/sparql/queries/getAllReachableInstances.sparql";

	public Hypernym(TransformationManager manager) {
		super(manager);
		this.name = "Hypernym";
		log = new MyLogger("logs/", this.name);
	}

	@Override
	public void transform() {

		Map<String, Boolean> checks = manager.getArticleChecks();
		checks.keySet().stream().forEach(name -> {
			boolean check = this.check(name);
			manager.getRelevant().put(name, check);
			if (check) {
				log.logLn("Mark " + name + " as relevant");
			} else {
				log.logLn("Mark " + name + " as irrelevant");
			}
		});
	}

	public boolean check(String name) {
		boolean result = false;
		// TODO Manage unknown articles
		result = manager.getSeed().contains(GitSeed.matchWikiName(name));
		return result || this.manager.getArticleChecks().get(name);
	}

}
