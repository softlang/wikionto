/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.triplestore.query;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.Query;
import com.hp.hpl.jena.query.QueryExecution;
import com.hp.hpl.jena.query.QueryExecutionFactory;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.query.ResultSetFormatter;
import com.hp.hpl.jena.sparql.algebra.Algebra;
import com.hp.hpl.jena.sparql.algebra.Op;

/**
 *
 * @author Marcel
 */
public class QueryProcessor {

	private final Query query;
	private final Dataset dataset;

	public QueryProcessor(Query query, Dataset dataset) {
		this.query = query;
		this.dataset = dataset;
	}

	public ResultSet query() {
		dataset.begin(ReadWrite.READ);
		Op op = Algebra.compile(query);
		op = Algebra.optimize(op);
		System.out.println("------------------");
		System.out.println(query);
		QueryExecution qe = QueryExecutionFactory.create(query, dataset);
		ResultSet results = qe.execSelect();
		System.out.println(results.hasNext());
		dataset.end();
		return results;
	}

	public void stream(QueryAreaStream qas) {
		ResultSet results = query();
		ResultSetFormatter.outputAsCSV(qas, results);
		qas.showText();
	}

}
