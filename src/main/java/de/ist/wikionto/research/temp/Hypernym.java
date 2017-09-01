package de.ist.wikionto.research.temp;

import java.util.List;

public class Hypernym extends Transformation {

	private String query = "/sparql/queries/getAllReachableInstances.sparql";

	public Hypernym(TransformationManager manager) {
		super(manager,"Hypernym");
	}

	@Override
	public void transform() {

		List<String> checks = manager.getArticles();
		// manager.getTextC().stream().filter(x ->
		// !manager.getSeed().contains(GitSeed.matchWikiName(x)))
		// .filter(x ->
		// !manager.getInfoboxC().contains(x)).collect(Collectors.toList());
		checks.stream().forEach(name -> {
			boolean check = this.check(name);
			manager.putInRelevantArticles(name, check);
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
		result = result || manager.getInfoboxC().contains(name);
		result = result || manager.getTextC().contains(name);
		return result;
	}

}
