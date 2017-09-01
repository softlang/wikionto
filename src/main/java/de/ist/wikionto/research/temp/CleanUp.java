package de.ist.wikionto.research.temp;

public class CleanUp extends Transformation {

	public CleanUp(TransformationManager manager) {
		super(manager, "CleanUp");
		
		// TODO Auto-generated constructor stub
	}

	@Override
	public void transform() {
		log.logDate("Start " + this.getName());
		this.manager.createNewDatasetName(this.getName(),this.manager.getStoreName());
		this.manager.keySetFromRelevantCategories().stream()
			.filter(key -> !this.manager.getFromRelevantCategories(key))
			.forEach(name -> {
				this.log.logLn("Remove category " + name);
				TransformationUtil.removeClassifier(this.manager.getStore(), name);
			});
		this.manager.keySetFromRelevantArticles().stream()
			.filter(key -> !this.manager.getFromRelevantArticles(key))
			.forEach(name -> {
				this.log.logLn("Remove article " + name);
				TransformationUtil.removeInstance(this.manager.getStore(), name);
			});
		log.logDate("Finish " + this.getName());
	}

}
