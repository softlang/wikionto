package de.ist.wikionto.research.temp;

import de.ist.wikionto.research.MyLogger;

public enum Annotation {
	SEED,
	ISA,
	INFOBOX,
	SEMANTICDISTANT,
	CHILDRENBASED,
	RESULT,
	SEMANTICDISTANT_FALSE,
	CHILDRENBASED_FALSE,
	ISA_FALSE,
	REMOVED_FROM_STORE;
	
	public static MyLogger log = new MyLogger("logs/", "Annotations");
	
	private String text;
	private String classifier;
	private int iteration = 0;
	
	public void setIteration(int iteration){
		this.iteration = iteration;
	}
	
	public int getCount(){
		return this.iteration;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getClassifier() {
		return classifier;
	}

	public void setClassifier(String classifier) {
		this.classifier = classifier;
	}
	
	
	
	
}
