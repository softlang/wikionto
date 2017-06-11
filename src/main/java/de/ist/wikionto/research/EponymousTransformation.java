package de.ist.wikionto.research;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.QuerySolution;
import com.hp.hpl.jena.query.ResultSet;

public class EponymousTransformation extends ArticleChecker {

	public EponymousTransformation(TransformationManager tm, List<QuerySolution> qss) {
		super(tm, qss);
		queryPath = "/sparql/queries/getEponymousInstances.sparql";
		this.name = "Eponymous";

	}

	@Override
	public void transform(Dataset dataset) {
		// TODO Auto-generated method stub

	}

	public Map<String, Boolean> check(Dataset dataset) {
		Map<String, Boolean> result = new HashMap<>();
		ResultSet rs = this.query(dataset);
		return result;
	}

	@Override
	public void run() {
		for (QuerySolution qs : qss)
			check(qs);
		tm.decthreadcounter();

	}

	@Override
	public boolean check(QuerySolution qs) {
		String text = qs.get("?text").asLiteral().getString();
		String title = qs.get("?name").asLiteral().getString();
		String first = qs.get("?first").asLiteral().getString();
		boolean textC = this.checkText(first);
		boolean infoC = this.checkInfoBox(text);
		System.out.println(first + "\n" + title + ": " + this.checkText(first) + " ");
		tm.log.logLn(title + ":\n	textCheck: " + textC + "\n	infoboxCheck: " + infoC);
		return false;
	}

	@Override
	public Transformation newTransformation(TransformationManager tm, List<QuerySolution> qss) {
		return new EponymousTransformation(tm, qss);
	}

	public static void main(String[] args) {
		String text = "In the C++ programming language, the C++ Standard Library is a collection of classes and functions, which are written in the core language and part of the C++ ISO Standard itself.[1] The C++ Standard Library provides several generic containers, functions to utilize and manipulate these containers, function objects, generic strings and streams (including interactive and file I/O), support for some language features, and functions for everyday tasks such as finding the square root of a number. The C++ Standard Library also incorporates 18 headers of the ISO C90 C standard library ending with, but their use is deprecated.[2] No other headers in the C++ Standard Library end in Features of the C++ Standard Library are declared within the std namespace.";
		EponymousTransformation et = new EponymousTransformation(null, null);
		text = text.replaceAll("\\[.*?\\]", "");
		String[] all = text.split("\\. ", 0);
		text = all[0] + ".";
		System.out.println(text);
		System.out.println(et.stanford(text));
		System.out.println(et.checkText(text));
	}

}
