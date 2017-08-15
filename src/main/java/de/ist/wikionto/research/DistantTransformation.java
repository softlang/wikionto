package de.ist.wikionto.research;

import java.util.List;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;

public class DistantTransformation extends ArticleChecker {
	static MyLogger log = new MyLogger("logs/", "DistantCall");

	public DistantTransformation(TransformationManager tm, List<QuerySolution> qss) {
		super(tm, qss);
		this.name = "DistantCall";
	}

	@Override
	public void run() {
		// TODO Auto-generated method stub

	}

	@Override
	public void transform(Dataset dataset, String name, Boolean check) {
		// TODO Auto-generated method stub

	}

	@Override
	public boolean check(QuerySolution qs) {
		// TODO Auto-generated method stub
		return false;
	}

	@Override
	public Transformation newTransformation(TransformationManager tm, List<QuerySolution> qss) {
		// TODO Auto-generated method stub
		return null;
	}

	public static void main(String[] args) {
		DistantTransformation dt = new DistantTransformation(null, null);

	}

}
