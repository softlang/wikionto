package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.QuerySolution;

public class TransformationThread implements Runnable {
	private Transformation trans;
	private TransformationManager manager;
	private QuerySolution sol;

	public TransformationThread(Transformation trans, TransformationManager manager, QuerySolution sol) {
		this.trans = trans;
		this.manager = manager;
		this.sol = sol;
	}

	@Override
	public void run() {
		trans.transform(sol);
		manager.decthreadcounter();
	}

}
