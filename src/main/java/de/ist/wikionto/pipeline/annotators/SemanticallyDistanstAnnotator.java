package de.ist.wikionto.research.temp;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class SemanticallyDistanstAnnotator extends Annotator {
	int i = 0;
	double threshold = 0.5;
	String queryInstances = "/sparql/smells/SemanticallyDistantInstance.sparql";
	private int iteration = 0;
	int j = 0;
	
	public SemanticallyDistanstAnnotator(WikiOntoPipeline manager , int iteration) {
		super(manager,"SemanticallyDistanstInstances" + "Iteration" + iteration);
		this.iteration = iteration;
	}

	// needs Hypernym
	@Override
	public void execute() {	
		log.logDate("Start " + this.name + " Iteration " + iteration);
		this.changed = false;
		log.logLn("Threshold : " + threshold);
		log.logLn("name, number of reachable classifiers, number of classifiers");
		List<String> temp = new ArrayList<String>();
		ResultSet instanceSet = QueryUtil.executeQuery(this.manager.getStore(), queryInstances);
		List<String> base = 
			this.manager.getTextC().stream()
			.filter(x -> !manager.getSeed().contains(x))
			.filter(x -> !manager.getInfoboxC().contains(x))
			.filter(x -> this.manager.getBooleanFromRelevantArticles(x))
			.sorted()
			.collect(Collectors.toList());
		System.out.println("Only text checks: " + base.size());
		i = 0;
		instanceSet.forEachRemaining(qs -> {
			String name = qs.get("?iname").asLiteral().getString();
			int numberOfCats = qs.get("?howManyDistantTypes").asLiteral().getInt();
			int reachable = qs.get("?howManyReachableTypes").asLiteral().getInt();
			int unreachable = qs.get("?difference").asLiteral().getInt();
			Boolean check;
			if (numberOfCats > 0 && reachable > 0){
				check = reachable >= threshold * numberOfCats ;
			} else 
				check = false;  
			if (base.contains(name)) {
				j++;
				if (check) {
					i++;
					log.logLn("Instance " + name + ", " + reachable + ", " + numberOfCats);
					log.logLn("  Mark " + name + " as relevant");
					commitChangedValue(name, true);
					this.log.log("\n");
					manager.addArticleAnnotation(name, Annotation.SEMANTICDISTANT);
				} else {
					log.logLn("Instance " + name + ", " + reachable + ", " + numberOfCats);
					log.logLn("  Mark " + name + " as irrelevant");
					this.manager.getTextC().remove(name);
					commitChangedValue(name,false);
					this.log.log("\n");
					this.manager.addArticleAnnotation(name, Annotation.ISA_FALSE);
				}
			} else {
				if (check)
					temp.add(name);
			}
			
		});
	System.out.println("Checked semantically: " + j);
		log.logLn("Total number of sematically distant checks: " + base.size());
		log.logLn("Number of relevant marked categories: " + i);
		
		log.logDate("End");
		log.close();
	}
	
	private void commitChangedValue(String name, boolean result) {
		boolean old = this.manager.getBooleanFromRelevantArticles(name);
		if (old != result) {
			changed = true;
//			log.logLn("  Changed value");
			this.manager.putInRelevantArticles(name, result);
		}
	}

	public int getIteration() {
		return iteration;
	}
}
