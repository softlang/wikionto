package de.ist.wikionto.research;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ResultSet;

import de.ist.wikionto.triplestore.query.QueryUtil;

public abstract class Transformation {
	private String queryPath;
	
	public abstract void transform(Dataset dataset);
	
	public abstract boolean check(Dataset dataset);
	
	public ResultSet query(Dataset dataset){
		ResultSet rs = QueryUtil.executeQuery(dataset, queryPath);
		return rs;
	}
}
