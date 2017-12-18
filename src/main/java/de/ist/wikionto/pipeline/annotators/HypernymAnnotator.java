package de.ist.wikionto.research.temp;

import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;

import com.hp.hpl.jena.query.Dataset;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class HypernymAnnotator extends Annotator {
	private List<String> articles;
	private List<String> infoboxC;
	private List<String> textC;
	private List<String> base;
	private Dataset store;
	
	public HypernymAnnotator(WikiOntoPipeline manager) {
		super(manager,"Hypernym");
	}

	@Override
	public void execute() {
		log.logDate("Start");
		this.store = this.manager.getStore();
		try {
			this.articles = NewArticleCheckManager.getArticles(this.store);
			this.infoboxC = NewArticleCheckManager.getInfoboxChecks(this.store);
			this.textC = NewArticleCheckManager.getTextChecks(this.store);
		} catch (IOException e) {
			e.printStackTrace();
		}
		this.manager.setArticleChecks(articles);
		this.manager.setInfoboxC(infoboxC);
		this.manager.setTextC(textC);
		articles.forEach(x -> this.manager.putInRelevantArticles(x, false));
		executeInfobox();
		excuteContent();
		
		log.logDate("Finish");
		log.close();
	}

	private void excuteContent() {
		List<String> temp  = base.stream()
			.filter(x -> !infoboxC.contains(x))
			.sorted()
			.collect(Collectors.toList());
		temp.forEach(name -> {
				if (textC.contains(name)){
					this.manager.putInRelevantArticles(name, true);
					this.manager.addArticleAnnotation(name, Annotation.ISA);
					log.logLn("Mark " + name + " as relevant");
				} else {
					this.manager.putInRelevantArticles(name, false);
					log.logLn("Mark " + name + " as irrelevant");
				}
			});
		log.logLn("Total number of articles with isA language relation: "+ temp.size() );
	}

	private void executeInfobox() {
		log.logLn("begin Infobox");
		
		base = articles.stream()
			.filter(name -> !manager.getSeed().contains(name))
			.collect(Collectors.toList());
		List<String> temp = 
		base.stream()
			.filter(infoboxC::contains)
			.collect(Collectors.toList());
		temp.forEach(name -> {
				this.manager.putInRelevantArticles(name, true);
				this.manager.addArticleAnnotation(name,Annotation.INFOBOX);
				log.logLn("Mark " + name + " as relevant");
			});
		log.logLn("Total number of articles with programming language infobox: "+ temp.size() + "\n\nBegin text check:");
	}
	
	// assume: all classifiers are true
	private void executeCategories(){
		QueryUtil.getReachableClassifiers(this.manager.getStore()).stream()
			.forEach(name -> this.manager.putInRelevantCategories(name, true));
		
	}
}
