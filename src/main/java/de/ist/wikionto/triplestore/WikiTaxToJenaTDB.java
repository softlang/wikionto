/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.wikionto.triplestore;

import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Map;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.query.ReadWrite;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.webwiki.model.Classifier;
import de.ist.wikionto.webwiki.model.Element;
import de.ist.wikionto.webwiki.model.Instance;

/**
 *
 * @author Marcel
 */
public class WikiTaxToJenaTDB {

    private static final String URI = "http://myWikiTax.de/";
    private static final String cURI = URI + "Classifier#";
    private static final String iURI = URI + "Instance#";
    private static final String nameURI = URI + "name";
    private static final String depthURI = URI + "depth";
    private static final String ciURI = URI + "classifies";
    private static final String ccURI = URI + "hasSubclassifier";
    private static final String defURI = URI + "definedBy";

    private static Model model;

    private static Map<String, Resource> classResMap;
    private static Map<String, Resource> instanceResMap;

    public static void createTripleStore(Classifier root) throws FileNotFoundException {
        String directory = "./"+root.getName().replaceAll(" ", "");
        Dataset dataset = TDBFactory.createDataset(directory);

        dataset.begin(ReadWrite.WRITE);
        model = dataset.getDefaultModel();
        classResMap = new HashMap<>();
        instanceResMap = new HashMap<>();

        Resource rootResource = model.getResource(cURI + classResMap.size());
        classResMap.put(root.getURIName(), rootResource);
        rootResource.addProperty(model.getProperty(nameURI), root.getName());
        rootResource.addProperty(model.getProperty(depthURI),
                Integer.toString(root.getMinDepth()));

        transformClassifier(root);

        // put outputstream instead of null
        dataset.commit();
        dataset.end();
    }

    private static void transformClassifier(Classifier classifier) {
    	if(classifier.getName().contains("OCaml software")){
    		System.out.println(classifier.getName());
    	}
        Resource classifierResource = classResMap.get(classifier.getURIName());

        if (null != classifier.getDescription()) {
            Resource descriptionResource;
            if (!instanceResMap.containsKey(classifier.getDescription().getURIName())) {
                descriptionResource = model.createResource(iURI + instanceResMap.size());
                descriptionResource.addProperty(model.getProperty(nameURI), classifier.getDescription().getName());
                instanceResMap.put(classifier.getDescription().getURIName(), descriptionResource);
                classifierResource.addProperty(model.getProperty(defURI), descriptionResource);
                transformInstance(classifier.getDescription());
            } else {
                descriptionResource = instanceResMap.get(classifier.getDescription().getURIName());
                classifierResource.addProperty(model.getProperty(defURI), descriptionResource);
            }

        }

        for (Instance instance : classifier.getInstances()) {
            Resource instanceResource;
            if (!instanceResMap.containsKey(instance.getURIName())) {
                instanceResource = model.createResource(iURI + instanceResMap.size());
                instanceResMap.put(instance.getURIName(), instanceResource);
                instanceResource.addProperty(model.getProperty(nameURI), instance.getName());
                classifierResource.addProperty(model.getProperty(ciURI), instanceResource);
                transformInstance(instance);
            } else {
                instanceResource = instanceResMap.get(instance.getURIName());
                classifierResource.addProperty(model.getProperty(ciURI), instanceResource);
            }

        }

        transformSubclassifiers(classifier);
        transformClassifiers(classifier, false);
    }

    private static void transformSubclassifiers(Classifier classifier) {
        for (Classifier subclass : classifier.getSubclassifiers()) {
        	System.out.println("Transforming subclassifier:"+subclass.getName());
            Resource subclassifierResource;
            if (!classResMap.containsKey(subclass.getURIName())) {
                subclassifierResource = model.createResource(cURI + classResMap.size());
                classResMap.put(subclass.getURIName(), subclassifierResource);
                subclassifierResource.addProperty(model.getProperty(nameURI), subclass.getName());
                transformClassifier(subclass);
            } else {
                subclassifierResource = classResMap.get(subclass.getURIName());
            }
            Resource typeResource = classResMap.get(classifier.getURIName());
            typeResource.addProperty(model.getProperty(ccURI), subclassifierResource);
            if(!subclassifierResource.hasProperty(model.getProperty(depthURI))){
                subclassifierResource.addProperty(model.getProperty(depthURI),
                        Integer.toString(subclass.getMinDepth()));
                transformClassifier(subclass);
            }
        }
    }

    private static void transformClassifiers(Element element, boolean isInstance) {
        for (String classifier : element.getAllClassifiers()) {
            Resource classifierResource;
            if (!classResMap.containsKey(replaceWhitespaceByUnderscore(classifier))) {
                classifierResource = model.createResource(cURI + classResMap.size());
                classResMap.put(replaceWhitespaceByUnderscore(classifier), classifierResource);
                classifierResource.addProperty(model.getProperty(nameURI), removeUnderscore(classifier));
            } else {
                classifierResource = classResMap.get(replaceWhitespaceByUnderscore(classifier));
            }
            if (isInstance) {
                Resource elementResource = instanceResMap.get(element.getURIName());
                classifierResource.addProperty(model.getProperty(ciURI), elementResource);
            } else {
                Resource elementResource = classResMap.get(element.getURIName());
                classifierResource.addProperty(model.getProperty(ccURI), elementResource);
            }
        }
    }

    private static void transformInstance(Instance entity) {
        transformClassifiers(entity, true);

        /**
        List<Information> informationList = entity.getInformationList();

        for (Information information : informationList) {
            Resource informationResource = model.createResource(iURI + informationcount);
            informationResource.addProperty(model.getProperty(URI + "name"), Integer.toString(informationcount));
            informationResource.addProperty(model.getProperty(URI + "topic"), information.getName());
            informationcount++;
            Resource entityResource = instanceResMap.get(entity.getURIName());
            entityResource.addProperty(model.getProperty(URI + "hasInformation"), informationResource);

            transformInformation(information, informationResource);
        }
        **/
    }

    /**
    private void transformInformation(Information information, Resource informationResource) {
        List<Property> properties = information.getProperties();
        for (Property property : properties) {
            Resource propertyResource = model.createResource(pURI + propertycount);
            propertycount++;
            propertyResource.addProperty(model.getProperty(URI + "name"), filterHTML(property.getName()));
            propertyResource.addProperty(model.getProperty(URI + "value"), filterHTML(property.getValue()));
            informationResource.addProperty(model.getProperty(URI + "hasProperty"), propertyResource);
        }
    }
    
    private String filterHTML(String text) {
        String result = Jsoup.parse(text).text().trim();
        return removeLteGte(result);
    }
    
    private String removeLteGte(String text) {
        return text.replaceAll("<", "").replaceAll(">", "");
    }
    **/

    private static String removeUnderscore(String supercat) {
        return supercat.replaceAll("_", " ");
    }

    private static String replaceWhitespaceByUnderscore(String supercat) {
        return supercat.replaceAll(" ", "_");
    }
}
