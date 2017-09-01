package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

public class EponymousTransformation extends Transformation {

	String queryPath = "/sparql/queries/getEponymousInstances.sparql";

	public EponymousTransformation(TransformationManager manager) {
		super(manager,"Eponymous");
	}

	@Override
	public void transform() {
		this.manager.createNewDatasetName(this.name, this.manager.getStoreName());
		this.log.logDate("Write transformation " + this.name + " to store " + this.manager.getStoreName());
		ResultSet rs = query(this.manager.getStore(), queryPath);
		rs.forEachRemaining(qs -> {
			boolean check = this.check(qs);
			String name = qs.get("?name").asLiteral().getString();
			if (check) {
				this.log.logLn("Delete Category " + name);
				TransformationUtil.removeClassifier(manager.getStore(), name);
			} else {
				this.log.logLn("Delete Article " + name);
				TransformationUtil.removeInstance(this.manager.getStore(), name);
			}
		});
		this.log.logDate("Finish Transformation " + this.name);
	}

	public boolean check(QuerySolution qs) {
		if (qs.contains("?name")) {
			String name = qs.get("?name").asLiteral().getString();
			// TODO Manage unknown articles
			return this.manager.getFromRelevantArticles(name);
		}
		return false;
	}

}
