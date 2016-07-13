package de.ist.clonto.triplestore.transform;

import com.hp.hpl.jena.query.Dataset;
import com.hp.hpl.jena.tdb.TDBFactory;
import org.apache.commons.io.FileUtils;

import javax.swing.*;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Writer;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Created by heinz on 29.10.2015.
 */
public class Cleaner {

    private final Dataset dataset;
    private final File original;
    private final File logfile;

    public void repair(){
        List<String> lines = null;
        try {
            lines = FileUtils.readLines(original);
        } catch (IOException e) {
            e.printStackTrace();
        }
        String[] headlines = lines.get(0).split(",");
        for(int i=1;i<lines.size();i++){
            String line = lines.get(i);
            String text="";
            String[] parts = line.split(",");
            for(int j = 0;j<parts.length;j++)
                text += headlines[j] + " : " + parts[j] + "\n";
            String eval = JOptionPane.showInputDialog(null, text);

            Prune p = new Prune(dataset);
            if(eval.contains("2"))
                p.abandonType(null);
            else if(eval.contains("6"))
                this.executeAbandonEntity(parts[0]);

            String newline= line+",,"+eval;
            lines.set(i,newline);
        }
        //save in copied csv via replace
        try {
            Writer fw = new FileWriter(logfile);
            for (String line : lines) {
                fw.append(line + "\n");
            }
            fw.close();
        }catch (IOException e){
            e.printStackTrace();
        }
    }

    public Cleaner(File ofile, File log, Dataset dataset){
        original = ofile;
        logfile = log;
        this.dataset = dataset;
    }

    public static void main(String[] args0){
        JFileChooser fc = new JFileChooser();
        fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
        fc.setFileSelectionMode(JFileChooser.FILES_ONLY);
        int returnVal = fc.showOpenDialog(null);
        File csv = null;
        File newcsv = null;
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            csv = fc.getSelectedFile();
            newcsv = new File(csv.getPath().replace(csv.getName().split("\\.")[0], "Eval"+csv.getName().split("\\.")[0] ));
        }
        fc = new JFileChooser();
        fc.setCurrentDirectory(new File(System.getProperty("user.dir")));
        fc.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
        returnVal = fc.showOpenDialog(null);
        Dataset dataset = null;
        if (returnVal == JFileChooser.APPROVE_OPTION) {
            dataset = TDBFactory.createDataset(fc.getSelectedFile().toString());
        }
        new Cleaner(csv, newcsv, dataset).repair();
    }

    private void executeAbandonEntity(String name){
        if (null != name) {
            Map<String, String> pmap = new HashMap<>();
            pmap.put("name", name);
            TransformationProcessor proc = new TransformationProcessor(dataset);
            long size = proc.transform("abandonEntity.sparql", pmap);
            JOptionPane.showMessageDialog(null, "Transformation successful! \n Model size difference: " + size);
        } else {
            JOptionPane.showMessageDialog(null, "Transformation failed!");
        }
    }
}
