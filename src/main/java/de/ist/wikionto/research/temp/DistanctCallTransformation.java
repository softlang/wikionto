package de.ist.wikionto.research.temp;

import java.util.HashMap;
import java.util.List;

import com.hp.hpl.jena.query.QuerySolution;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;

public class DistanctCallTransformation extends Transformation {
	private double threshold = 0.8;
	HashMap<String, Boolean> classifiers = new HashMap<>();

	public DistanctCallTransformation(TransformationManager manager) {
		super(manager, "/sparql/queries/getAllClassifiers.sparql");
		this.name = "DistanctCall";
		log = new MyLogger("logs/", "DistanctCall");
	}

	@Override
	public void transform(QuerySolution qs) {
		String name = qs.get("?name").asLiteral().getString();
		List<String> ins = QueryUtil.getInstances(this.manager.getOldStore(), name);
		List<String> cls = QueryUtil.getClassifiers(this.manager.getOldStore(), name);
		boolean insCheck = checkInstances(name, ins);
		boolean classCheck = checkClassifiers(name, cls);
		// this.log.logLn(name + " " + classifiers.keySet().containsAll(cls));

		// this.log.logLn("Category " + name + " valid\n Instance check :" +
		// insCheck);

	}

	@Override
	public boolean check(QuerySolution qs) {
		String name = qs.get("?name").asLiteral().getString();
		List<String> ins = QueryUtil.getInstances(this.manager.getOldStore(), name);
		List<String> cls = QueryUtil.getClassifiers(this.manager.getOldStore(), name);
		System.out.println(ins);
		return false;
	}

	public boolean checkInstances(String name, List<String> ins) {
		if (ins.size() > 0) {
			int i = 0;
			for (String s : ins)
				if (manager.getArticleChecks().get(s))
					i++;
			return (i / ins.size() >= threshold);
		} else
			return false;
	}

	public boolean checkClassifiers(String name, List<String> cls) {
		int i = 0;
		System.out.println(cls.size());
		System.out.println(classifiers.size());
		log.logLn(name + " " + cls.stream().allMatch(x -> classifiers.containsKey(x)));
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
