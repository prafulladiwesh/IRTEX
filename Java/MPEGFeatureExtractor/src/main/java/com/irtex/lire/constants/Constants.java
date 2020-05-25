package com.irtex.lire.constants;

import org.apache.commons.io.IOCase;
import org.apache.commons.io.filefilter.SuffixFileFilter;

public class Constants {
	
	public static final SuffixFileFilter fileFilter = new SuffixFileFilter(new String[]{".jpg", ".jpeg", ".png", ".gif"}, IOCase.INSENSITIVE);
	public static final String outputFileName = "out.csv";
	public static final String QUERY_FEATURE = "queryFeature.csv";
	public static final String OUTPUT_FEATURE = "outputFeature.csv";
	public static final char outputFileSeperator = ',';

}
