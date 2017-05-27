package de.ist.clonto.webwiki;

import static org.junit.Assert.*;

import java.io.IOException;

import org.junit.Test;

import de.ist.wikionto.webwiki.Wiki;

public class WikiTest {

	@Test
	public void testGetCategoriesPage() {
		Wiki w = new Wiki();
		String[] cs;
		try {
			cs = w.getCategories("Haskell (programming language)",false,true);
			assertEquals(8,cs.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetCategoriesCategory(){
		Wiki w = new Wiki();
		try {
			String[] cs = w.getSuperCategories("Computer languages");
			assertEquals(3,cs.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetSubcategories(){
		Wiki w = new Wiki();
		try {
			String[] cs = w.getCategoryMembers("Object-based programming languages",Wiki.CATEGORY_NAMESPACE);
			assertEquals(2,cs.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetArticles(){
		Wiki w = new Wiki();
		try {
			String[] is = w.getCategoryMembers("Computer languages", Wiki.MAIN_NAMESPACE);
			assertEquals(20,is.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetMain(){
		Wiki w = new Wiki();
		try {
			String[] ls = w.getLinksOnPage("Computer languages");
			assertEquals(1,ls.length);
			assertEquals("Computer language",ls[0]);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetTopic(){
		Wiki w = new Wiki();
		int count=0;
		try {
			String[] is = w.getTemplates("Haskell (programming language)", Wiki.TEMPLATE_NAMESPACE);
			for(String t : is){
				if(t.startsWith("Template:Infobox")){
					String topic = (String) t.subSequence(16, t.length());
					if(topic.length()>0){
						assertEquals("programming language",topic.trim());
						count++;
					}
				}
			}
			assertEquals(1,count);
		} catch (IOException e) {
			assertFalse(true);
		}
	}

}
