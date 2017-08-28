package de.ist.wikionto.research.temp;

import java.util.List;
import java.util.stream.Collectors;

public class HypernymAnnotation extends Annotation {
	private int i = 0;
	
	public HypernymAnnotation(TransformationManager manager) {
		super(manager,"Hypernym");
	}

	@Override
	public void annotate() {
		this.log.logDate("Start");
		this.log.logLn("begin Infobox");
		List<String> base = this.manager.getArticles().stream()
			.filter(name -> !manager.getSeed().contains(name))
			.collect(Collectors.toList());
		base.stream()
			.filter(manager.getInfoboxC()::contains)
			.forEach(name -> {
				i++;
				this.manager.putInRelevant(name, true);
				this.log.logLn("Mark " + name + " as relevant");
			});
		log.logLn("Total number of articles with programming language infobox: "+ i + "\nBegin text check:");
		i = 0;
		base.stream()
			.filter(x -> !manager.getInfoboxC().contains(x))
			.sorted()
			.forEach(name -> {
				if (manager.getTextC().contains(name)){
					i++;
					this.manager.putInRelevant(name, true);
					this.log.logLn("Mark " + name + " as relevant");
				} else {
					this.manager.putInRelevant(name, false);
					this.log.logLn("Mark " + name + " as irrelevant");
				}
			});
		log.logLn("Total number of articles with isA language relation: "+ i );
		this.log.logDate("Finish");
	}

}
