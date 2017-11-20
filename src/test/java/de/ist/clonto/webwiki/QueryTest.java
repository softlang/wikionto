package de.ist.clonto.webwiki;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.util.List;

import org.junit.BeforeClass;
import org.junit.Test;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

import de.ist.wikionto.triplestore.query.QueryUtil;

public class QueryTest {

	static Dataset dataset;

	@BeforeClass
	public static void setUp() throws Exception {
		// MyCrawlerManager cm = new MyCrawlerManager("OCaml programming
		// language family", new HashSet<>(), 99);
		// cm.start();
		String directory = "./OCamlprogramminglanguagefamily";
		dataset = TDBFactory.createDataset(directory);
	}

	@Test
	public void testgetInstances() {
		List<String> is = QueryUtil.getInstances(dataset, "OCaml software");
		assertEquals(18, is.size());
	}

	@Test
	public void testgetSubclassifiers() {
		List<String> ss = QueryUtil.getSubclassifiers(dataset, "OCaml software");
		assertEquals(1, ss.size());
		assertTrue(ss.get(0).equals("Free software programmed in OCaml"));
	}

	@Test
	public void testgetSuperclassifiers() {
		List<String> ss = QueryUtil.getSuperclassifiers(dataset, "OCaml software");
		assertEquals(2, ss.size());
		assertEquals("OCaml programming language family", ss.get(0));
		assertEquals("Software by programming language", ss.get(1));
	}

	@Test
	public void testgetClassifiers() {
		List<String> ss = QueryUtil.getClassifiersFromInstance(dataset, "OCaml");
		assertEquals(11, ss.size());
	}

	@Test
	public void testgetPathClassToClass() {
		List<String> ps = QueryUtil.getPathFromClassToClass(dataset, "OCaml programming language family",
				"Free software programmed in OCaml");
		assertEquals(2, ps.size());
		assertEquals("OCaml software", ps.get(0));
		assertEquals("Free software programmed in OCaml", ps.get(1));
	}

	@Test
	public void testgetPathClassToClass0() {
		List<String> ps = QueryUtil.getPathFromClassToClass(dataset, "OCaml programming language family",
				"OCaml software");
		assertEquals(1, ps.size());
		assertEquals("OCaml software", ps.get(0));
	}

	@Test
	public void testgetPathClassToInstance() {
		List<String> ps = QueryUtil.getPathFromClassToInstance(dataset, "OCaml programming language family",
				"MLDonkey");
		assertEquals(3, ps.size());
		assertEquals("OCaml software", ps.get(0));
		assertEquals("Free software programmed in OCaml", ps.get(1));
		assertEquals("MLDonkey", ps.get(2));
	}

	@Test
	public void testgetPathClassToInstance0() {
		List<String> ps = QueryUtil.getPathFromClassToInstance(dataset, "Free software programmed in OCaml",
				"MLDonkey");
		assertEquals(1, ps.size());
		assertEquals("MLDonkey", ps.get(0));
	}

}
