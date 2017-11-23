package de.ist.wikionto.research.temp;

import java.util.List;

public class SeedAnnotator extends Annotator {
	
	public SeedAnnotator(WikiOntoPipeline manager) {
		super(manager,"GitSeed");
	}

	@Override
	public void execute() {
		log.logDate("Start");
		List<String> seed = GitSeed.readLanguages();
		manager.getArticles().stream()
			.filter(x -> seed.contains(GitSeed.matchWikiName(x)))
			.sorted()
			.forEach(name -> {
				log.logLn("Seed " + name + " is relevant");
				this.manager.getSeed().add(name);
				this.manager.putInRelevantArticles(name, true);
				this.manager.addArticleAnnotation(name, Annotation.SEED);
			});
	
		log.logDate("Finish");
		log.close();
	}

	

}
