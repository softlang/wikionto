package de.ist.wikionto.research.temp;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class GitSeed {

	public static List<String> readLanguages() {
		List<String> result = new ArrayList<>();
		try {
			BufferedReader br = new BufferedReader(new FileReader(new File("SEED.txt")));

			result = br.lines()
					.skip(3)
					.filter(x -> !x.contains("  type:"))
					.map(y -> {
						return y.replace(":", "").replace(" ", "").toLowerCase();
						})
					.collect(Collectors.toList());
			br.close();
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
		String result = wikiName.replaceAll("_", "").replaceAll("\\(.*?\\)", "").trim().toLowerCase();
		return result;
	}

}
