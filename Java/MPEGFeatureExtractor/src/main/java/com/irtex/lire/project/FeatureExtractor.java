package com.irtex.lire.project;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import javax.imageio.ImageIO;

import org.apache.commons.lang3.ArrayUtils;

import com.irtex.lire.constants.Constants;
import com.irtex.lire.utils.Utils;

import net.semanticmetadata.lire.imageanalysis.features.GlobalFeature;
import net.semanticmetadata.lire.imageanalysis.features.global.CEDD;
import net.semanticmetadata.lire.imageanalysis.features.global.ColorLayout;
import net.semanticmetadata.lire.imageanalysis.features.global.EdgeHistogram;
import net.semanticmetadata.lire.imageanalysis.features.global.ScalableColor;

public class FeatureExtractor {
	
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
          				GlobalFeature f = null;
          				img = ImageIO.read(new FileInputStream(imgFileName));
          				createFeatures(img, imgFileName, f, fileName);
          			}
                } catch (Exception e) {
                	System.out.printf("Exception : " + e.getMessage());
                	Utils.printErrorExit();
                }
            }
        }
    }


	private static void createFeatures(BufferedImage img, String imgFileName, GlobalFeature f, String outFileName) throws IOException {
		double[] edgeHistogramFeature = edgeHistogramExtractor(img, f);
         
		double[] scalableColorFeature = scalableColorExtractor(img);
		      
		double[] colorLayoutrFeature = colorLayoutExtractor(img);
		
		double[] ceddFeature = ceddExtractor(img);
		
		double[] someFeature = ArrayUtils.addAll(edgeHistogramFeature, scalableColorFeature);
		double[] someMoreFeatures = ArrayUtils.addAll(someFeature, colorLayoutrFeature);
		double[] finalFeatures = ArrayUtils.addAll(someMoreFeatures, ceddFeature);
		
		String[] globalFeature = new String[] {imgFileName, Arrays.toString(finalFeatures).replace("[", "").replace("]", "").replaceAll("\\s+","")};
		Utils.writeCsv(globalFeature, outFileName);
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
