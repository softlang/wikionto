package de.ist.wikionto.research.temp;

import de.ist.wikionto.research.MyLogger;

public abstract class PipelineElement {
	protected MyLogger log;
	protected WikiOntoPipeline manager;
	protected String name;

	public PipelineElement(WikiOntoPipeline manager, String name) {
		this.name = name;
		this.manager = manager;
		log = new MyLogger("logs/", name);
	}
	
	public PipelineElement(WikiOntoPipeline manager, String name, boolean log) {
		this.name = name;
		this.manager = manager;
		if (log)
		 this.log = new MyLogger("logs/", name);
	}
	
	public abstract void execute();

	public String getName() {
		return name;
	}

}
