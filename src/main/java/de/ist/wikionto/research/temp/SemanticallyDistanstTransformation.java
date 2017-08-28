package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.ResultSet;

public class SemanticallyDistanstTransformation extends Transformation {

	String queryClassifiers = "/sparql/smells/SemanticallyDistantClassifier.sparql";
	String queryInstances = "/sparql/smells/SemanticallyDistantInstance.sparql";
	boolean changed = true;

	public SemanticallyDistanstTransformation(TransformationManager manager) {
		super(manager,"SemanticallyDistanst");
	}

	@Override
	public void transform() {
		ResultSet classifierSet = this.query(this.manager.getStore(), queryClassifiers);
		ResultSet instanceSet = this.query(this.manager.getStore(), queryInstances);
		int i = 0;
		while (changed) {
			log.logLn("Iteration " + i + ":");
			log.logLn("name, number of reachable classifiers, number of classifiers");
			changed = false;
			classifierSet.forEachRemaining(x -> {
				String name = x.get("?cname").asLiteral().getString();
				int depth = x.get("?depth").asLiteral().getInt();
				int distant = x.get("?howManyDistantTypes").asLiteral().getInt();
				int reachable = x.get("?howManyReachableTypes").asLiteral().getInt();
				int difference = x.get("?difference").asLiteral().getInt();
				if (difference > reachable) {
					log.logLn("Classifier " + name + ", " + reachable + ", " + distant);
					TransformationUtil.removeClassifier(manager.getStore(), name);
					changed = true;
				}
			});
			instanceSet.forEachRemaining(x -> {
				String name = x.get("?iname").asLiteral().getString();
				int distant = x.get("?howManyDistantTypes").asLiteral().getInt();
				int reachable = x.get("?howManyReachableTypes").asLiteral().getInt();
				int difference = x.get("?difference").asLiteral().getInt();
				if (difference > reachable) {
					log.logLn("Instance " + name + ", " + reachable + ", " + distant);
					TransformationUtil.removeInstance(manager.getStore(), name);
					changed = true;
				}
			});
			classifierSet = this.query(this.manager.getStore(), queryClassifiers);
			instanceSet = this.query(this.manager.getStore(), queryInstances);
			i++;
		}
	}

}
