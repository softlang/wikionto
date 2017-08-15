package de.ist.wikionto.research.temp;

import java.util.HashMap;
import java.util.List;

import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class ChildrenBased extends Transformation {
	private double threshold = 0.8;
	HashMap<String, Boolean> classifiers = new HashMap<>();
	String query = "/sparql/queries/getAllClassifiers.sparql";

	public ChildrenBased(TransformationManager manager) {
		super(manager);
		this.name = "ChildrenBased";
		log = new MyLogger("logs/", this.name);
	}

	@Override
	public void transform() {
		ResultSet rs = query(this.manager.getOldStore(), query);
		rs.forEachRemaining(qs -> {
			String name = qs.get("?name").asLiteral().getString();
			System.out.println(name);
			List<String> ins = QueryUtil.getInstances(this.manager.getOldStore(), name);
			Boolean b = checkInstances2(ins);
			// System.out.println(name + " " + b);
			if (!b) {
				log.logLn("Remove Classifier " + name);
				TransformationUtil.removeClassifier(this.manager.getStore(), name);
			} else {
				log.logLn("Classifier " + name + " is relevant");
			}
		});

	}

	public boolean checkInstances(List<String> ins) {
		if (ins.size() > 0) {
			int i = 0;
			for (String s : ins)
				if (manager.getArticleChecks().get(s))
					i++;
			return (i / ins.size() >= threshold);
		} else
			return false;
	}

	public boolean checkInstances2(List<String> ins) {
		long n = ins.stream().filter(manager.getRelevant()::get).count();
		if (ins.size() > 0) {
			log.logLn(n + " " + ins.size());
			return n / ins.size() >= threshold;
		} else
			return true;
	}

	public double getThreshold() {
		return threshold;
	}

	public void setThreshold(double threshold) {
		this.threshold = threshold;
	}

	public HashMap<String, Boolean> getClassifiers() {
		return classifiers;
	}

	public void setClassifiers(HashMap<String, Boolean> classifiers) {
		this.classifiers = classifiers;
	}

}
