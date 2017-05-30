package de.ist.wikionto.research;

public class InstanceCheck {
	private String text;
	private String title;
	/*
	 * true iff title contains a signal word
	 */
	private Boolean titleCheck;
	/*
	 * true iff infobox contains a signal word
	 */
	private Boolean infoCheck;
	/*
	 * true iff first 4 text lines contains is-a + a signal word
	 */
	private Boolean textCheck;

	public InstanceCheck(String title, String text) {
		this.text = text;
		this.title = title;
		this.check();
	}

	public void check() {
		this.titleCheck = ArticleChecker.checkTitle(this.title);
		this.infoCheck = ArticleChecker.checkInfoBox(this.text);
		this.textCheck = ArticleChecker.checkText(this.text);
	}

	public boolean result() {
		return infoCheck || textCheck;
	}

	public String getText() {
		return text;
	}

	public void setText(String text) {
		this.text = text;
	}

	public String getTitle() {
		return title;
	}

	public void setTitle(String title) {
		this.title = title;
	}

	public Boolean getTitleCheck() {
		return titleCheck;
	}

	public Boolean getInfoCheck() {
		return infoCheck;
	}

	public Boolean getTextCheck() {
		return textCheck;
	}

}
