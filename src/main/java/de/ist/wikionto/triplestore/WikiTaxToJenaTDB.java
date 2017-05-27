/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.triplestore;

import java.util.HashMap;
import java.util.Map;
import java.util.Set;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.research.MyLogger;
import de.ist.wikionto.webwiki.model.Classifier;
import de.ist.wikionto.webwiki.model.Element;
import de.ist.wikionto.webwiki.model.Instance;

/**
 *
 * @author Marcel
 * @author Matthias
 */
public class WikiTaxToJenaTDB {

	private static MyLogger l = new MyLogger("logs/", "ToJena");
	private static final Model pModel = ModelFactory.createDefaultModel();
	private static final String URI = "http://myWikiTax.de/";
	private static final String cURI = URI + "Classifier#";
	private static final String iURI = URI + "Instance#";
	private static final Property nameP = pModel.createProperty(URI + "name");
	private static final Property depthP = pModel.createProperty(URI + "depth");
	private static final Property ciP = pModel.createProperty(URI + "classifies");
	private static final Property ccP = pModel.createProperty(URI + "hasSubclassifier");
	private static final Property defP = pModel.createProperty(URI + "definedBy");
	private static final Property linkP = pModel.createProperty(URI + "linksTo");
	private static final Property textP = pModel.createProperty(URI + "hasText");

	private static Model model;

	private static Map<String, Resource> classResMap;
	private static Map<String, Resource> instanceResMap;
	private static int maxDepth;

	public static void createTripleStore(Classifier root, int max) {
		maxDepth = max;
		String directory = "./" + root.getName().replaceAll(" ", "");
		Dataset dataset = TDBFactory.createDataset(directory);

		dataset.begin(ReadWrite.WRITE);
		model = dataset.getDefaultModel();
		classResMap = new HashMap<>();
		instanceResMap = new HashMap<>();

		Resource rootResource = model.getResource(cURI + classResMap.size());
		classResMap.put(root.getName(), rootResource);
		rootResource.addProperty(nameP, root.getName());
		rootResource.addProperty(depthP, Integer.toString(root.getMinDepth()));

		transformClassifier(root);
		System.out.println("Remaining after depth filter: #C:" + classResMap.size() + ", #I:" + instanceResMap.size());

		dataset.commit();
		dataset.end();
	}

	private static void transformClassifier(Classifier classifier) {
		transformText(classifier);
		transformDescription(classifier);
		transformInstances(classifier);
		transformLinks(classifier);
		transformClassifiers(classifier, false);
		transformSubClassifiers(classifier);
	}
	
	private static void transformText(Classifier element) {
		String text = element.getText();
		Resource resource = classResMap.get(element.getName());
		if (!resource.hasProperty(textP)){
			if (text != null) {
				resource.addProperty(textP, text);
			}
		}
	}
	
	private static void transformDescription(Classifier classifier) {
		Instance description = classifier.getDescription();
		if (description != null) {
			Resource classifierResource = classResMap.get(classifier.getName());
			Resource descriptionResource;
			if (instanceResMap.containsKey(description.getName())) {
				descriptionResource = instanceResMap.get(description.getName());
			} else {
				descriptionResource = model.getResource(iURI + instanceResMap.size());
				instanceResMap.put(description.getName(), descriptionResource);
				descriptionResource.addProperty(nameP, description.getName());
				descriptionResource.addProperty(textP, classifier.getDescription().getText());
			}
			classifierResource.addProperty(defP, descriptionResource);
		}
	}
	
	private static void transformInstances(Classifier classifier) {
		Set<Instance> instances = classifier.getInstances();
		Resource classifierResource = classResMap.get(classifier.getName());
		Resource instanceResource;
		for (Instance instance : instances) {
			if (instanceResMap.containsKey(instance.getName())) {
				instanceResource = instanceResMap.get(instance.getName());
			} else {
				instanceResource = model.getResource(iURI + instanceResMap.size());
				instanceResMap.put(instance.getName(), instanceResource);
				instanceResource.addProperty(nameP, instance.getName());
				// l.logLn("instance hasText " + instance.getName() + " with
				// length" + instance.getText().length());
				transformText(instance); //This would only happen if it was not processed before
				transformLinks(instance);
				transformClassifiers(instance, true);
			}
			classifierResource.addProperty(ciP, instanceResource);
		}
	}
	
	private static void transformText(Instance element) {
		String text = element.getText();
		Resource resource = instanceResMap.get(element.getName());
		if (!resource.hasProperty(textP))
			if (text != null)
				resource.addProperty(textP, text);
	}
	
	private static void transformLinks(Instance instance) {
		Resource resource = instanceResMap.get(instance.getName());
		instance.getLinks().forEach(link -> resource.addProperty(linkP, link));
	}

	private static void transformLinks(Classifier classifier) {
		Resource resource = classResMap.get(classifier.getName());
		classifier.getMainLinks().forEach(link -> resource.addProperty(linkP, link));
	}

	private static void transformClassifiers(Element element, boolean isInstance) {
		for (String classifier : element.getAllClassifiers()) {
			String className = classifier.replaceAll(" ", "_");
			Resource classifierResource;
			if (!classResMap.containsKey(className)) {
				classifierResource = model.createResource(cURI + classResMap.size());
				classResMap.put(className, classifierResource);
				classifierResource.addProperty(nameP, className);
			} else {
				classifierResource = classResMap.get(className);
			}
			if (isInstance) {
				Resource elementResource = instanceResMap.get(element.getName());
				classifierResource.addProperty(ciP, elementResource);
			} else {
				Resource elementResource = classResMap.get(element.getName());
				classifierResource.addProperty(ccP, elementResource);
			}
		}
	}
	
	private static void transformSubClassifiers(Classifier classifier) {
		if (classifier.getMinDepth() == maxDepth)
			return;
		Set<Classifier> subCs = classifier.getSubclassifiers();
		Resource classifierResource = classResMap.get(classifier.getName());
		for (Classifier subC : subCs) {
			Resource subClassifierResource;
			if (classResMap.containsKey(subC.getName())) {
				subClassifierResource = classResMap.get(subC.getName());
				if (!subClassifierResource.hasProperty(depthP)){
					subClassifierResource.addProperty(depthP, Integer.toString(subC.getMinDepth()));
				}
			} else {
				subClassifierResource = model.getResource(cURI + classResMap.size());
				classResMap.put(subC.getName(), subClassifierResource);
				subClassifierResource.addProperty(nameP, subC.getName());
				subClassifierResource.addProperty(depthP, Integer.toString(subC.getMinDepth()));
				transformClassifier(subC);
			}
			classifierResource.addProperty(ccP, subClassifierResource);
		}
	}

}
