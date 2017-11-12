package de.ist.wikionto.research.temp;

import com.hp.hpl.jena.query.Dataset;
import de.ist.wikionto.research.MyLogger;

public abstract class Annotation extends PipelineElement{

	public Annotation(WikiOntoPipeline manager,String name) {
		super(manager,name);
		System.out.println("Start annotation " + name + "\n see log \"" + log.logPath() + "\"");
	}	
	
}
