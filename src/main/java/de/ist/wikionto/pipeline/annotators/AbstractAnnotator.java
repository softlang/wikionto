package de.ist.wikionto.research.temp;

public abstract class Annotator extends PipelineElement{

	public Annotator(WikiOntoPipeline manager,String name) {
		super(manager,name);
		System.out.println("Start annotation " + name + "\n see log \"" + log.logPath() + "\"");
	}	
	
	public Annotator(WikiOntoPipeline manager, String name, boolean log) {
		super(manager,name,log);
	}
}
