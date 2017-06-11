package de.ist.wikionto.research;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

public class MyLogger {
	FileWriter logger;
	boolean log = true;

	public MyLogger(String path) {
		try {
			// Replace because of Windows issues with ':'
			new File(path).mkdir();
			logger = new FileWriter(new File(path + new Date().toString().replaceAll(":", "") + ".log"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public MyLogger(String path, String name) {
		try {
			// Replace because of Windows issues with ':'
			new File(path).mkdir();
			logger = new FileWriter(new File(path + name + new Date().toString().replaceAll(":", "") + ".log"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public MyLogger(String path, String name, boolean log) {
		this.log = log;
		try {
			if (log)
				// Replace because of Windows issues with ':'
				logger = new FileWriter(new File(path + name + new Date().toString().replaceAll(":", "") + ".log"));
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void newLog(String name) {
		if (log) {
			try {
				logger.flush();
				logger.close();
				logger = new FileWriter(new File("log/" + name));
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}

	public void logLn(String msg) {
		if (log) {
			try {
				this.logger.write(msg + '\n');
				this.logger.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}
	}

	public void log(String msg) {
		if (log) {

			try {
				this.logger.write(msg);
				this.logger.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}

	public void logDate(String msg) {
		if (log) {
			Date d = new Date();
			try {
				this.logger.write(d.toString() + " : " + msg + "\n");
				this.logger.flush();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}

		}
	}

}
