package de.ist.clonto.webwiki;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

import java.io.IOException;
import java.util.HashSet;
import java.util.Iterator;
import java.util.Set;

import org.junit.BeforeClass;
import org.junit.Test;
import org.xml.sax.SAXException;

import de.ist.wikionto.webwiki.MyCrawlerManager;
import de.ist.wikionto.webwiki.model.Classifier;
import de.ist.wikionto.webwiki.model.Instance;

/**
 * This test covers the implemented extraction from Wikipedia's category graph.
 * As an example 'OCaml programming language family' was selected as the root to
 * have a small testable tree.
 * 
 * The tests work with the transient object graph that is later transformed into
 * the TDB format.
 * 
 * @author Marcel
 *
 */
public class CrawlerTest {

	private static Classifier r;

	@BeforeClass
	public static void setUp() throws SAXException, IOException, InterruptedException {
		Set<String> exclusionset = new HashSet<>();
		MyCrawlerManager cm = new MyCrawlerManager("OCaml programming language family", exclusionset);
		cm.start(6);
		r = cm.getRoot();
	}

	@Test
	public void testRootNames() {
		assertEquals("OCaml_programming_language_family", r.getName());
	}

	@Test
	public void testRootSuperclassifiers() {
		Set<String> superc = r.getAllClassifiers();
		assertEquals(3, superc.size());
	}

	@Test
	public void testRootInstances() {

		Set<Instance> inst = r.getInstances();
		for (Instance i : inst) {
			assertTrue(i.getName().equals("F Sharp (programming language)") || i.getName().equals("JoCaml")
					|| i.getName().equals("OCaml"));
		}
	}

	@Test
	public void testOCamlInstance() {
		Set<Instance> inst = r.getInstances();
		Iterator<Instance> it = inst.iterator();
		Instance i = null;
		while (it.hasNext()) {
			i = it.next();
			if (i.getName().equals("OCaml"))
				break;
		}
		Set<String> cs = i.getAllClassifiers();
		assertEquals(11, cs.size());
	}

	@Test
	public void testSubclassifierCount() {
		Set<Classifier> subc = r.getSubclassifiers();
		assertEquals(1, subc.size());

	}

	@Test
	public void testOCamlSoftwareContent() {
		Set<Classifier> subc = r.getSubclassifiers();
		Classifier s1 = subc.iterator().next();
		assertTrue(s1.getName().equals("OCaml software"));
	}

	@Test
	public void testOCamlSoftwareSuperclassifiers() {
		Set<Classifier> subc = r.getSubclassifiers();
		Classifier s1 = subc.iterator().next();
		Set<String> superc = s1.getAllClassifiers();
		assertEquals(2, superc.size());
	}
}
