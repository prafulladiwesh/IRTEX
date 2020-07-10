package com.irtex.lire.project;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;
import javax.imageio.ImageIO;
import com.irtex.lire.constants.Constants;
import com.irtex.lire.utils.Utils;

import net.semanticmetadata.lire.imageanalysis.features.GlobalFeature;
import net.semanticmetadata.lire.imageanalysis.features.global.CEDD;
import net.semanticmetadata.lire.imageanalysis.features.global.ColorLayout;
import net.semanticmetadata.lire.imageanalysis.features.global.EdgeHistogram;
import net.semanticmetadata.lire.imageanalysis.features.global.ScalableColor;

public class IndividualFeatureExtractor {
	
	public static void main(String[] args) {
		BufferedImage img = null;
        ArrayList<String> imageArrayList = null;       
        for (int i = 0; i < args.length; i++) {
            String arg = args[i];
            if (arg.startsWith("-i")) {
            	// To extract the query image features
                try {
                	String fileName = Constants.QUERY_FEATURE;
                	Utils.deleteFileIfExists(fileName);
                	
                    img = ImageIO.read(new FileInputStream(args[i + 1]));
                    GlobalFeature f = null;
                    createFeatures(img, args[i + 1], f, fileName);
                } catch (IOException e) {
                	System.out.printf("Exception : " + e.getMessage());
                	Utils.printErrorExit();
                }
            } else if (arg.startsWith("-f")) {
            	// To extract the data set features
                try {
                	String fileName = Constants.OUTPUT_FEATURE;
                	Utils.deleteFileIfExists(fileName);
                	
                	imageArrayList =  Utils.getAllImages(new File(args[i + 1]));
          			for(String imgFileName : imageArrayList) {
          				Path pathFileName = Paths.get(imgFileName).getFileName();
          				GlobalFeature f = null;
          				// img = ImageIO.read(new FileInputStream(imgFileName));
          				
          				try {
        					img = ImageIO.read(new FileInputStream(imgFileName));
        				}  catch (IllegalArgumentException illExp) {
        					// Exception in thrown in case of grayscale image
        					FileInputStream stream  = new FileInputStream(imgFileName);
        					img = Utils.readGrayScaleImage(stream);
        		    	}
          				img = Utils.resize(img, 64, 64);
          				createFeatures(img, pathFileName.toString(), f, fileName);
          			}
                } catch (Exception e) {
                	System.out.printf("Exception : " + e.getMessage());
                	Utils.printErrorExit();
                } 
            }
        }
        
        
//        try {
//        	String fileName = Constants.OUTPUT_FEATURE;
//        	File file = new File("pascal2009");
//			imageArrayList =  Utils.getAllImages(file);
//			System.out.printf("imageArrayList : "+imageArrayList);
//			for(String imgFileName : imageArrayList) {
//				System.out.println("imgFileName : "+imgFileName);
//				Path pathFileName = Paths.get(imgFileName).getFileName();
//				System.out.println("pathFileName :"+pathFileName);
//				GlobalFeature f = null;
//				try {
//					img = ImageIO.read(new FileInputStream(imgFileName));
//				}  catch (IllegalArgumentException illExp) {
//					// Exception in thrown in case of grayscale image
//					FileInputStream stream  = new FileInputStream(imgFileName);
//					img = Utils.readGrayScaleImage(stream);
//		    	}
//				// img = Utils.resize(img, 64, 64);
//				createFeatures(img, pathFileName.toString(), f, fileName);
//			}	
//        } catch (IOException e) {
//        	System.out.printf("Exception : "+ e.getMessage());
//        	e.printStackTrace();
//    	} catch (Exception exp) {
//    		System.out.println("Exception : "+ exp.getMessage());
//    		exp.printStackTrace();
//    	}
//        System.out.printf("FEATURE EXTRACTION COMPLETED SUCCESSFULLY!! \n");
    }

	private static void createFeatures(BufferedImage img, String imgFileName, GlobalFeature f, String outFileName) throws IOException {
		double[] edgeHistogramFeature = edgeHistogramExtractor(img, f);
		String[] edgeHistogram = new String[] {imgFileName, Arrays.toString(edgeHistogramFeature).replace("[", "").replace("]", "").replaceAll("\\s+","")};
		Utils.writeCsv(edgeHistogram, Constants.EHD_FEATURE);
         
		double[] scalableColorFeature = scalableColorExtractor(img);
		String[] scalableColor = new String[] {imgFileName, Arrays.toString(scalableColorFeature).replace("[", "").replace("]", "").replaceAll("\\s+","")};
		Utils.writeCsv(scalableColor, Constants.SCD_FEATURE);
		      
		double[] colorLayoutrFeature = colorLayoutExtractor(img);
		String[] colorLayout = new String[] {imgFileName, Arrays.toString(colorLayoutrFeature).replace("[", "").replace("]", "").replaceAll("\\s+","")};
		Utils.writeCsv(colorLayout, Constants.CLD_FEATURE);
		
		double[] ceddFeature = ceddExtractor(img);
		String[] cedd = new String[] {imgFileName, Arrays.toString(ceddFeature).replace("[", "").replace("]", "").replaceAll("\\s+","")};
		Utils.writeCsv(cedd, Constants.CEDD_FEATURE);
		
	}
	
	private static double[] edgeHistogramExtractor(BufferedImage img, GlobalFeature f) {
		if (f == null) {
			f = new EdgeHistogram();
		}
		f.extract(img);
		double[] edgeHistogramFeature = f.getFeatureVector();
		return edgeHistogramFeature;
	}

	private static double[] scalableColorExtractor(BufferedImage img) {
		GlobalFeature f = new ScalableColor();
		f.extract(img);
		double[] scalableColorFeature = f.getFeatureVector();
		return scalableColorFeature;
	}

	private static double[] colorLayoutExtractor(BufferedImage img) {
		GlobalFeature f = new ColorLayout();
		f.extract(img);
		double[] colorLayoutrFeature = f.getFeatureVector();
		return colorLayoutrFeature;
	}
	
	private static double[] ceddExtractor(BufferedImage img) {
		GlobalFeature f = new CEDD();
		f.extract(img);
		double[] ceddFeature = f.getFeatureVector();
		return ceddFeature;
	}

}
