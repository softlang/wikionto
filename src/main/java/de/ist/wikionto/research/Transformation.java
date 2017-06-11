package de.ist.wikionto.research;

import java.util.List;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.triplestore.query.QueryUtil;

public abstract class Transformation implements Runnable {
	protected String queryPath;

	protected TransformationManager tm;

	protected List<QuerySolution> qss;

	protected String name;

	public Transformation(TransformationManager tm, List<QuerySolution> qss) {
		this.tm = tm;
		this.qss = qss;
	}

	public String getQueryPath() {
		return queryPath;
	}

	public abstract void transform(Dataset dataset);

	public abstract boolean check(QuerySolution qs);

	public abstract Transformation newTransformation(TransformationManager tm, List<QuerySolution> qss);

	public ResultSet query(Dataset dataset) {
		ResultSet rs = QueryUtil.executeQuery(dataset, queryPath);
		return rs;
	}
}
