package de.ist.wikionto.pipeline;

public enum Threshold {
	SEMANTIC(0.5),
	CHILDREN_ARTICLES(0.35),
	CHILDREN_CATEGORIES(0.35);
	
	private final double THRESHOLD;

	private Threshold(double threshold){
		this.THRESHOLD = threshold;
	}

	public double getThreshold() {
		return THRESHOLD;
	}
	
}
