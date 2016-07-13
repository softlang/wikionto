package de.ist.clonto.webwiki;

import static org.junit.Assert.*;

import java.io.IOException;

import org.junit.Test;

public class WikiTest {

	@Test
	public void testGetCategoriesPage() {
		Wiki w = new Wiki();
		String[] cs;
		try {
			cs = w.getCategories("Haskell (programming language)",false,true);
			assertEquals(9,cs.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetCategoriesCategory(){
		Wiki w = new Wiki();
		try {
			String[] cs = w.getCategories("Category:Computer languages",false,true);
			assertEquals(3,cs.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetArticles(){
		Wiki w = new Wiki();
		try {
			String[] is = w.getCategoryMembers("Category:Computer languages", Wiki.MAIN_NAMESPACE);
			assertEquals(19,is.length);
		} catch (IOException e) {
			assertFalse(true);
		}
	}
	
	@Test
	public void testGetMain(){
		Wiki w = new Wiki();
		try {
			String[] ls = w.getLinksOnPage("Category:Computer languages");
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
