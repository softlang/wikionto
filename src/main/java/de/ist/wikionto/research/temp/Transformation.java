package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;

public abstract class Transformation {
	protected String queryPath;
	protected String name;
	MyLogger log;
	protected TransformationManager manager;
	protected ResultSet querySolutions;

	public Transformation(TransformationManager manager, String queryPath) {
		super();
		this.queryPath = queryPath;
		this.manager = manager;

	}

	public String getQueryPath() {
		return queryPath;
	}

	public abstract void transform(QuerySolution qs);

	public abstract boolean check(QuerySolution qs);

	public ResultSet query(Dataset dataset) {
		ResultSet rs = QueryUtil.executeQuery(dataset, queryPath);
		return rs;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

}
