package com.irtex.lire.utils;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Iterator;

import org.apache.commons.io.filefilter.IOFileFilter;
import org.apache.commons.io.filefilter.TrueFileFilter;

import com.irtex.lire.constants.Constants;

import au.com.bytecode.opencsv.CSVWriter;

public class Utils {
	
	public static String[] doubleArrayToStringArray(double[] dArray) {
		if(dArray == null)
			return null;
		int dArraySize = dArray.length;
	    String[] str = new String[dArraySize];   
	    for(int i=0; i<dArraySize; i++) {
	    	str[i] = String.valueOf(dArray[i]);
	    }
		return str;
    }
	
	public static ArrayList<String> getAllImages(File directory) throws IOException {
        ArrayList<String> resultList = new ArrayList<String>(256);
        IOFileFilter includeSubdirectories = TrueFileFilter.INSTANCE;
        boolean descendIntoSubDirectories = true;
        if (!descendIntoSubDirectories) includeSubdirectories = null;
        Iterator<File> fileIterator = org.apache.commons.io.FileUtils.iterateFiles(directory, Constants.fileFilter, includeSubdirectories);
        while (fileIterator.hasNext()) {
            File next = fileIterator.next();
            resultList.add(next.getCanonicalPath());
        }
        if (resultList.size() > 0)
            return resultList;
        else
            return null;
    }
	
	public static void writeCsv(String[] globalFeature, String outFileName) throws IOException {
		CSVWriter csvWriter = new CSVWriter(new FileWriter(outFileName, true), Constants.outputFileSeperator, 
				CSVWriter.NO_QUOTE_CHARACTER);
		csvWriter.writeNext(globalFeature);
		csvWriter.close();
	}
	
	public static void deleteFileIfExists(String fileName) throws IOException {
		File file = new File(fileName);
		// Delete the output file if already exists
		Files.deleteIfExists(file.toPath());
	}
	
	public static void printErrorExit() {
        System.exit(1);
    }

}
