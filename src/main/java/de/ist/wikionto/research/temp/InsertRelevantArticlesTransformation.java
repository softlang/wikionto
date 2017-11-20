package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class ArticleAnnotation extends Annotation{
	private String query = "/sparql/queries/getAllReachableArticles.sparql";
	
	public ArticleAnnotation(WikiOntoPipeline manager) {
		super(manager, "");
		
	}

	@Override
	public void execute() {
		Dataset store = this.manager.getStore();
		ResultSet rs = QueryUtil.executeQuery(store, query);
		store.begin(ReadWrite.WRITE);
		Model model = store.getDefaultModel();
		Property relevantP = model.createProperty("http://myWikiTax.de/relevant");
		rs.forEachRemaining(qs -> {
			String name = qs.get("?name").asLiteral().getString();
			Resource instance = qs.get("?instance").asResource();
			model.add(instance, relevantP, this.manager.getFromRelevantArticles(name).toString());
		});
		store.commit();
		store.end();
	}

}
