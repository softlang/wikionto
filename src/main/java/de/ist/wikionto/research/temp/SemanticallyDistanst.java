package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.research.MyLogger;

public class SemanticallyDistanst extends Transformation {

	double threshold = 0.5;
	String queryInstances = "/sparql/smells/SemanticallyDistantInstance.sparql";

	public SemanticallyDistanst(TransformationManager manager) {
		super(manager);
		this.name = "SemanticallyDistanstInstances";
		log = new MyLogger("logs/", this.name);
	}

	@Override
	public void transform() {
		ResultSet instanceSet = this.query(this.manager.getStore(), queryInstances);
		int i = 0;
		log.logLn("Threshold : " + threshold);
		log.logLn("name, number of reachable classifiers, number of classifiers");

		instanceSet.forEachRemaining(x -> {
			String name = x.get("?iname").asLiteral().getString();
			int distant = x.get("?howManyDistantTypes").asLiteral().getInt();
			int reachable = x.get("?howManyReachableTypes").asLiteral().getInt();
			int difference = x.get("?difference").asLiteral().getInt();
			Boolean orig = this.manager.getArticleChecks().get(name);
			Boolean seed = this.manager.getSeed().contains(GitSeed.matchWikiName(name));
			if (!seed) {
				if (orig != null) {
					if (reachable < difference) {
						if (orig) {
							log.logLn("Instance " + name + ", " + reachable + ", " + distant);
							log.logLn("Mark " + name + " as irrelevant");
							manager.getRelevant().put(name, false);
						}
					}
				} else {
					log.logLn("Add Instance " + name + ", " + reachable + ", " + distant);
					boolean b = reachable / distant >= threshold;
					manager.getRelevant().put(name, b);
					if (b)
						log.logLn("Mark " + name + " as relevant");
					else
						log.logLn("Mark " + name + " as irrelevant");
				}
			} else {
				this.manager.getRelevant().put(name, true);
				log.logLn(name + " is SEED");
			}
		});

	}

}
