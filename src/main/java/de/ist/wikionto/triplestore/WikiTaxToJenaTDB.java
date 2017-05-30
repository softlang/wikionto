package de.ist.wikionto.triplestore;

import java.io.File;
import java.io.IOException;
import java.util.Collection;
import java.util.HashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.commons.io.FileUtils;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.webwiki.model.Classifier;
import de.ist.wikionto.webwiki.model.Instance;

public class WikiTaxToJenaTDB {

	//private static MyLogger l = new MyLogger("logs/", "ToJena");
	private static final String URI = "http://myWikiTax.de/";
	private static final String cURI = URI + "Classifier#";
	private static final String iURI = URI + "Instance#";
	private static Model model;
	private static Property nameP;
	private static Property depthP;
	private static Property instanceOfP;
	private static Property isAP;
	private static Property catP;
	private static Property defP;
	private static Property linkP;
	private static Property textP;

	private static Map<String, Resource> classResources;
	private static Map<String, Resource> instanceResources;

	public static void createTripleStore(Collection<Classifier> classifiers, Collection<Instance> instances,
			Classifier root) {
		File dir = new File("./" + root.getName());
		if (dir.exists()) {
			try {
				FileUtils.cleanDirectory(dir);
			} catch (IOException ex) {
				Logger.getLogger(WikiTaxToJenaTDB.class.getName()).log(Level.SEVERE, null, ex);
			}
		} else {
			boolean success = dir.mkdirs();
			if (!success) {
				System.err.println("Creating target directory failed");
				System.exit(0);
			}
		}
		String directory = "./" + root.getName();
		Dataset dataset = TDBFactory.createDataset(directory);
		model = dataset.getDefaultModel();
		dataset.begin(ReadWrite.WRITE);
		nameP = model.createProperty(URI + "name");
		depthP = model.createProperty(URI + "depth");
		catP = model.createProperty(URI + "hasCategory");
		instanceOfP = model.createProperty(URI + "instanceOf");
		isAP = model.createProperty(URI + "isA");
		defP = model.createProperty(URI + "definedBy");
		linkP = model.createProperty(URI + "linksTo");
		textP = model.createProperty(URI + "hasText");

		classResources = new HashMap<>();
		instanceResources = new HashMap<>();

		//Readability over small performance difference
		classifiers.forEach(c -> createClassifier(c));
		instances.forEach(i -> createInstance(i));
		classifiers.forEach(c -> createTree(c));

		dataset.commit();
		dataset.end();
	}

	private static void createClassifier(Classifier c) {
		Resource res = model.getResource(cURI + classResources.size());
		classResources.put(c.getName(), res);
		res.addProperty(nameP, c.getName());
		res.addProperty(depthP, Integer.toString(c.getMinDepth()));
		res.addProperty(textP, c.getText());
		c.getCategories().stream().forEach(cat -> res.addProperty(catP, cat));
		c.getMainLinks().stream().forEach(l -> res.addProperty(defP, l));
	}

	private static void createInstance(Instance i) {
		Resource res = model.getResource(iURI + instanceResources.size());
		instanceResources.put(i.getName(), res);
		res.addProperty(nameP, i.getName());
		res.addProperty(textP, i.getText());
		i.getCategories().stream().forEach(cat -> res.addProperty(catP, cat));
		i.getLinks().stream().forEach(l -> res.addProperty(linkP, l));
	}

	private static void createTree(Classifier c) {
		assert classResources.containsKey(c.getName());
		Resource res = classResources.get(c.getName());
		c.getSubclassifiers().forEach(sub -> {
			assert classResources.containsKey(sub.getName());
			Resource subr = classResources.get(sub.getName());
			subr.addProperty(isAP, res);
		});
		c.getInstances().forEach(i -> {
			assert instanceResources.containsKey(i.getName());
			Resource ir = instanceResources.get(i.getName());
			ir.addProperty(instanceOfP, res);
		});
	}

}
