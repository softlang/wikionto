package de.ist.wikionto.research.temp;

import java.util.List;
import java.util.stream.Collectors;

import com.hp.hpl.jena.query.ResultSet;

public class SemanticallyDistanstAnnotation extends Annotation {
	int i = 0;
	double threshold = 0.5;
	String queryInstances = "/sparql/smells/SemanticallyDistantInstance.sparql";

	public SemanticallyDistanstAnnotation(TransformationManager manager) {
		super(manager,"SemanticallyDistanstInstances");
	}

	
	@Override
	public void annotate() {
		log.logDate("Start " + this.name);
		log.logLn("Threshold : " + threshold);
		log.logLn("name, number of reachable classifiers, number of classifiers");
		ResultSet instanceSet = this.query(this.manager.getStore(), queryInstances);
		List<String> base = 
			this.manager.getTextC().stream()
			.filter(x -> !manager.getSeed().contains(x))
			.filter(x -> !manager.getInfoboxC().contains(x))
			.collect(Collectors.toList());
		i = 0;
		instanceSet.forEachRemaining(qs -> {
			String name = qs.get("?iname").asLiteral().getString();
			int distant = qs.get("?howManyDistantTypes").asLiteral().getInt();
			int reachable = qs.get("?howManyReachableTypes").asLiteral().getInt();
			int difference = qs.get("?difference").asLiteral().getInt();
			Boolean check;
			if (distant > 0)
				check = reachable >= threshold * distant ;
			else 
				check = false;  
			if (base.contains(name)) {
				if (check) {
					i++;
					log.logLn("Instance " + name + ", " + reachable + ", " + distant);
					log.logLn("Mark " + name + " as relevant");
					manager.putInRelevantArticles(name, true);
				} else {
					log.logLn("Instance " + name + ", " + reachable + ", " + distant);
					log.logLn("Mark " + name + " as irrelevant");
					manager.putInRelevantArticles(name, false);
				}
			}
		});
		log.logLn("Total number of sematically distant checks: " + base.size());
		log.logLn("Number of relevant marked categories: " + i);
	}

}
