package de.ist.wikionto.research.temp;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import com.fasterxml.jackson.core.JsonParseException;
import com.fasterxml.jackson.databind.JsonMappingException;
import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;

public class GitSeed {

	public static List<String> readLanguages() {
		List<String> result = new ArrayList<>();
		try {
			BufferedReader br = new BufferedReader(new FileReader(new File("SEED.txt")));

			result = br.lines().skip(3).filter(x -> !x.contains("  type:")).map(y -> {
				return y.replace(":", "").toLowerCase();
			}).collect(Collectors.toList());

			// ArrayList<String> langs = new ArrayList<>();
			// int n = 1;
			// while (br.ready()) {
			// String s = br.readLine();
			// if (n % 2 == 1)
			// langs.add(s);
			// n++;
			// }
			br.close();
			// result = langs.stream().map(x -> {
			// return x.replace(":", "");
			// }).collect(Collectors.toList());

		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return result;
	}

	public static String matchWikiName(String wikiName) {
		String result = wikiName.replaceAll("_", " ").replaceAll("\\(.*?\\)", "").trim().toLowerCase();
		return result;
	}

	public static void main(String[] args) throws JsonParseException, JsonMappingException, IOException {
		Dataset store = TDBFactory.createDataset("Computer_languages");
		List<String> res = readLanguages();
		// res =
		// res.stream().map(String::toLowerCase).collect(Collectors.toList());
		// System.out.println(matchWikiName("C_(programming_language)"));
		Map<String, Boolean> wiki = new ArticleCheckManager().getArticleChecks(store);
		wiki.keySet().stream().map(GitSeed::matchWikiName).filter(res::contains).forEach(x -> System.out.println(x));
	}
}
