package de.ist.wikionto.research.temp;

import java.util.HashMap;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.query.ResultSet;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class InsertRelevantCategoriesTransformation extends Transformation{
	private String query = "/sparql/queries/classifier/getAllClassifiers.sparql";
	
	public InsertRelevantCategoriesTransformation(WikiOntoPipeline manager) {
		super(manager, "InsertRelevantCategories",false);
		
	}

	@Override
	public void execute() {
		Dataset store = this.manager.getStore();
		TransformationUtil.transformFile(store, "/deleteClassifierRelevantProperties.sparql", new HashMap<>());
		ResultSet rs = QueryUtil.executeQuery(store, query);
		rs.forEachRemaining(qs -> {
			String name = qs.get("?name").asLiteral().getString();
			HashMap<String, String> temp =  new HashMap<>();
			temp.put("?name", name);
			temp.put("?mark", this.manager.getBooleanFromRelevantCategories(name).toString());
			TransformationUtil.transformFile(store, "/InsertCategoryRelevantProperties.sparql", temp);
		});
//		store.begin(ReadWrite.WRITE);
//		Model model = store.getDefaultModel();
//		Property relevantP = model.createProperty("http://myWikiTax.de/relevant");
//		rs.forEachRemaining(qs -> {
//			String name = qs.get("?name").asLiteral().getString();
//			Resource category = qs.get("?classifier").asResource();
//			model.add(category, relevantP, this.manager.getOptionalFromRelevantCategories(name).orElse(true).toString());
//		});
//		store.commit();
//		store.end();
	}

}
