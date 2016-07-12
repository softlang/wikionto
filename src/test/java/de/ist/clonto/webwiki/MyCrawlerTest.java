/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package de.ist.clonto.webwiki;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.junit.Assert.fail;
import info.bliki.api.Page;

import java.util.List;

import org.junit.After;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import de.ist.clonto.webwiki.model.Instance;
import de.ist.clonto.webwiki.model.Classifier;

/**
 *
 * @author Marcel
 */
public class MyCrawlerTest {

    public MyCrawlerTest() {
    }

    @BeforeClass
    public static void setUpClass() {
    }

    @AfterClass
    public static void tearDownClass() {
    }

    @Before
    public void setUp() {
    }

    @After
    public void tearDown() {
    }

    /**
     * Test of retrieveSuperCategories() of class MyCrawler.
     */
    @Test
    public void testSuperCategories() {
        System.out.println("supercategories of Category:SQL");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("Category:SQL");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        assertTrue(e.getAllClassifiers().size() == 2);
        assertTrue(e.getAllClassifiers().contains("Database management systems"));
        assertTrue(e.getAllClassifiers().contains("Query languages"));
    }

    @Test
    public void testSuperCategories1() {
        System.out.println("supercategories of Entity SQL");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("SQL");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        System.out.println(e.getAllClassifiers().size());
        assertTrue(e.getAllClassifiers().size() == 8);
        assertTrue(e.getAllClassifiers().contains("Articles with example SQL code"));
        assertTrue(e.getAllClassifiers().contains("Computer languages"));
        assertTrue(e.getAllClassifiers().contains("Data modeling languages"));
        assertTrue(e.getAllClassifiers().contains("Declarative programming languages"));
        assertTrue(e.getAllClassifiers().contains("Relational database management systems"));
        assertTrue(e.getAllClassifiers().contains("Query languages"));
        assertTrue(e.getAllClassifiers().contains("SQL"));
        assertTrue(e.getAllClassifiers().contains("Requests for audio pronunciation (English)"));
    }

    @Test
    public void testSuperCategories2() {
        System.out.println("supercategories of Type:Free compilers and interpreters");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("Category:Free_compilers_and_interpreters");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        assertTrue(e.getAllClassifiers().size() == 3);
        assertTrue(e.getAllClassifiers().contains("Free computer programming tools"));
        assertTrue(e.getAllClassifiers().contains("Compilers"));
        assertTrue(e.getAllClassifiers().contains("Interpreters (computing)"));
    }

    @Test
    public void testSuperCategories3() {
        System.out.println("supercategories of APL (programming language)");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("APL (programming language)");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        assertTrue(e.getAllClassifiers().size() == 8);
        assertTrue(e.getAllClassifiers().contains("Array programming languages"));
        assertTrue(e.getAllClassifiers().contains("Functional languages"));
        assertTrue(e.getAllClassifiers().contains("Dynamic programming languages"));
        assertTrue(e.getAllClassifiers().contains("APL programming language family"));
        assertTrue(e.getAllClassifiers().contains(".NET programming languages"));
        assertTrue(e.getAllClassifiers().contains("IBM software"));
        assertTrue(e.getAllClassifiers().contains("Command shells"));
        assertTrue(e.getAllClassifiers().contains("Programming languages created in 1964"));
    }

    @Test
    public void testSuperCategories4() {
        System.out.println("supercategories of C++");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("C++");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        assertEquals(9, e.getAllClassifiers().size());
        assertTrue(e.getAllClassifiers().contains("C++"));
        assertTrue(e.getAllClassifiers().contains("Algol programming language family"));
        assertTrue(e.getAllClassifiers().contains("C++ programming language family"));
        assertTrue(e.getAllClassifiers().contains("Class-based programming languages"));
        assertTrue(e.getAllClassifiers().contains("Cross-platform software"));
        assertTrue(e.getAllClassifiers().contains("Object-oriented programming languages"));
        assertTrue(e.getAllClassifiers().contains("Programming languages created in 1983"));
        assertTrue(e.getAllClassifiers().contains("Statically typed programming languages"));
        assertTrue(e.getAllClassifiers().contains("Programming languages with an ISO standard"));
    }

    @Test
    public void testSuperCategories5() {
        System.out.println("supercategories of JSLint");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("JSLint");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        assertEquals(2, e.getAllClassifiers().size());
        assertTrue(e.getAllClassifiers().contains("JavaScript programming tools"));
        assertTrue(e.getAllClassifiers().contains("Static program analysis tools"));
    }

    @Test
    public void testSuperCategories6() {
        System.out.println("supercategories of Type:LibreOffice");
        CategoryCrawler instance = new CategoryCrawler(null, null);
        Page page = WikipediaAPI.getFirstPage("Category:LibreOffice");
        Instance e = new Instance();
        instance.retrieveSuperCategories(page.toString(), e);
        assertEquals(5, e.getAllClassifiers().size());
        assertTrue(e.getAllClassifiers().contains("Cross-platform free software"));
        assertTrue(e.getAllClassifiers().contains("Free software programmed in C++"));
        assertTrue(e.getAllClassifiers().contains("Office suites for Linux"));
        assertTrue(e.getAllClassifiers().contains("OpenDocument"));
        assertTrue(e.getAllClassifiers().contains("Open-source office suites"));
    }

    /**
     * example for annotation with {{Cat more|(name)}}
     */
    @Test
    public void testMainEntityRetrieval1() {
        System.out.println("Main entity computer languages");
        Page page = WikipediaAPI.getFirstPage("Category:Computer languages");
        Classifier testcl = new Classifier();
        testcl.setName("Computer languages");
        CategoryCrawler instance = new CategoryCrawler(null, testcl);
        instance.retrieveMainEntity(page.toString());
        Instance entity = testcl.getDescription();
        String ename = entity.getName();
        assertEquals("Computer language", ename);
    }

    /**
     * example for annotation with {{Cat main|(name)}}
     */
    @Test
    public void testMainEntityRetrieval2() {
        System.out.println("Main entity XML");
        Page page = WikipediaAPI.getFirstPage("Category:XML");
        Classifier testcl = new Classifier();
        testcl.setName("XML");
        CategoryCrawler instance = new CategoryCrawler(null, testcl);
        instance.retrieveMainEntity(page.toString());
        Instance entity = testcl.getDescription();
        String ename = entity.getName();
        assertEquals("XML", ename);
    }

    /**
     * example for annotation with {{Cat main}}
     */
    @Test
    public void testMainEntityRetrieval3() {
        System.out.println("Main entity PostgreSQL");
        Page page = WikipediaAPI.getFirstPage("Category:PostgreSQL");
        Classifier testcl = new Classifier();
        testcl.setName("PostgreSQL");
        CategoryCrawler instance = new CategoryCrawler(null, testcl);
        instance.retrieveMainEntity(page.toString());
        Instance entity = testcl.getDescription();
        String ename = entity.getName();
        assertEquals("PostgreSQL", ename);
    }
}
