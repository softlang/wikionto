package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.triplestore.query.QueryUtil;

public abstract class Annotation {
	protected String name;
	protected TransformationManager manager;
	protected MyLogger log;

	public Annotation(TransformationManager manager,String name) {
		super();
		this.manager = manager;
		this.name = name;
		this.log = new MyLogger("logs/", this.name);
	}

	public abstract void annotate();
	
	public ResultSet query(Dataset dataset, String queryFile) {
		ResultSet rs = QueryUtil.executeQuery(dataset, queryFile);
		return rs;
	}
}
