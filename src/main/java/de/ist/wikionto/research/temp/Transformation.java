package de.ist.wikionto.research.temp;

import de.ist.wikionto.research.MyLogger;

public abstract class Transformation extends PipelineElement{

	public Transformation(WikiOntoPipeline manager,String name) {
		super(manager,name);
		log = new MyLogger("logs/", this.name);
		System.out.println("Start transformation " + name + "\n see log \"" + log.logPath() + "\"");

	}

}
