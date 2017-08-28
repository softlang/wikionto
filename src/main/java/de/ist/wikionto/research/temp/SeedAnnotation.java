package de.ist.wikionto.research.temp;

import java.util.List;

public class SeedAnnotation extends Annotation {

	public SeedAnnotation(TransformationManager manager) {
		super(manager,"GitSeed");
	}

	@Override
	public void annotate() {
		this.log.logDate("Start");
		List<String> seed = GitSeed.readLanguages();
		manager.getArticles().stream()
			.filter(x -> seed.contains(GitSeed.matchWikiName(x)))
			.sorted()
			.forEach(name -> {
				this.log.logLn("Seed " + name + " is relevant");
				this.manager.getSeed().add(name);
				this.manager.putInRelevant(name, true);
			});
		this.log.logDate("Finish");
	}

}
