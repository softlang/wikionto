package de.ist.wikionto.research.temp;

import de.ist.wikionto.research.MyLogger;

public enum Annotation {
	SEED,
	ISA,
	INFOBOX,
	SEMANTICDISTANT,
	CHILDRENBASED,
	REMOVED_SEMANTICDISTANT,
	REMOVED_CHILDRENBASED,
	REMOVED_ISA,
	REMOVED_FROM_STORE;
	
	public static MyLogger log = new MyLogger("logs/", "Annotations");
	
	private int count = 0;
	
	public void setCount(int i){
		this.count = i;
	}
	
	public int getCount(){
		return this.count;
	}
	
	
}
