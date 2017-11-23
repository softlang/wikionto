package de.ist.wikionto.research.temp;

import java.util.List;

public class RotationAnnotator extends PipelineElement {
	
	private List<PipelineElement> elements;
	private Boolean rotate = false;
	
	public RotationAnnotator(WikiOntoPipeline manager, List<PipelineElement> elements) {
		super(manager, "Rotate" + elements.stream().map(PipelineElement::getName).reduce("", (x,y) -> x+y) );
		this.elements = elements;
	}

	@Override
	public void execute() {
		elements.forEach(element -> {
			element.execute();
			if (element.hasChanged())
				rotate = true;
		});
		
	}

}
