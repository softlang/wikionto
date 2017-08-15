package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.research.MyLogger;

public class EponymousTransformation extends Transformation {

	String queryPath = "/sparql/queries/getEponymousInstances.sparql";

	public EponymousTransformation(TransformationManager manager) {
		super(manager);
		this.name = "Eponymous";
		log = new MyLogger("logs/", "Eponymous");
	}

	@Override
	public void transform() {
		ResultSet rs = query(this.manager.getStore(), queryPath);
		rs.forEachRemaining(qs -> {
			boolean check = this.check(qs);
			String name = qs.get("?name").asLiteral().getString();
			if (check) {
				// System.out.println("Delete Category:" + name);
				this.log.logLn("Delete Category " + name);
				TransformationUtil.removeClassifier(manager.getStore(), name);
				// Map<String, String> pmap = new HashMap<>();
				// pmap.put("name", name);
				// long size = manager.transformFile(manager.getStore(),
				// "abandonClassifierObject.sparql", pmap);
				// size += manager.transformFile(manager.getStore(),
				// "abandonClassifierSubject.sparql", pmap);
				// System.out.println("Delete size " + size);
			} else {
				// System.out.println("Delete " + name);
				this.log.logLn("Delete Article " + name);
				TransformationUtil.removeInstance(this.manager.getStore(), name);
				// Map<String, String> pmap = new HashMap<>();
				// pmap.put("name", name);
				// long size = manager.transformFile(manager.getStore(),
				// "abandonInstanceObject.sparql", pmap);
				// size += manager.transformFile(manager.getStore(),
				// "abandonInstanceSubject.sparql", pmap);
				// System.out.println("Delete size " + size);
			}
		});
	}

	public boolean check(QuerySolution qs) {
		if (qs.contains("?name")) {
			String name = qs.get("?name").asLiteral().getString();
			// TODO Manage unknown articles
			return this.manager.getRelevant().get(name);
		}
		return false;
	}

}
