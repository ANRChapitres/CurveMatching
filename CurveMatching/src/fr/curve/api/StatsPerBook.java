package fr.curve.api;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import fr.curve.utils.ExportToCSV;
import fr.curve.utils.RomanNumbers;

public class StatsPerBook {

	public static void main(String[] args) {
		
		HashMap<String, List<String[]>> mapDesOeuvres=new HashMap<String, List<String[]>>();
		
		File folder = new File("./Fichiers");
		File repertoire[]=folder.listFiles();
		for (File file:repertoire){
			if (file.getName().contains(".txt")){
				String wholeText="";
				try {
					wholeText = new String(Files.readAllBytes(file.toPath()));
				} catch (IOException e) {
					e.printStackTrace();
				}	
				StringTokenizer tokenizerWholeText=new StringTokenizer(wholeText);
				int nombreTotalMotsParTexte=tokenizerWholeText.countTokens();
				
				String preTraitementChiffresRomains[]=wholeText.split("\\n");
				int index=0;
				@SuppressWarnings("unused")
				boolean aTraiter=false;
				for (String nombre:preTraitementChiffresRomains){
					Pattern p1=Pattern.compile("Chapitre [MDCLXVI]+\\b");
					Matcher m1=p1.matcher(nombre);
					Pattern p2=Pattern.compile("\\b.*[MDCLXVI]+\\b");
					Matcher m2=p2.matcher(nombre);
					int lastNumberFound=0;
					while (m1.find()){
						if (RomanNumbers.decode(m1.group().substring(m1.group().lastIndexOf(" ")))>lastNumberFound){
							preTraitementChiffresRomains[index]=nombre.replace(m1.group(), "Chapitre "+String.valueOf(RomanNumbers.decode(m1.group().substring(m1.group().lastIndexOf(" ")))));
							aTraiter=true;
							lastNumberFound=RomanNumbers.decode(m1.group().substring(m1.group().lastIndexOf(" ")));
						}
					}
					while (m2.find()){
						if (nombre.length()<8){
							preTraitementChiffresRomains[index]=nombre.replace(m2.group(), "Chapitre "+String.valueOf(RomanNumbers.decode(m2.group())));
							lastNumberFound=RomanNumbers.decode(m2.group());
						}
						aTraiter=true;
					}
					index++;
				}
				StringBuilder sb= new StringBuilder();

				for (String ligne:preTraitementChiffresRomains){
					sb.append(ligne+"\n");
				}
				
				wholeText=sb.toString();
				if (aTraiter=true){
					try {
						File fileTrans =new File("./Fichiers/"+file.getName());
						FileWriter writer = new FileWriter(fileTrans);
						writer.write(wholeText);
						writer.flush();
						writer.close();
					} catch (IOException e) {
						// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
				int nombreTotalDeChapitres=wholeText.split("Chapitre [0-9]+").length-1;
					String []Parties=wholeText.split("\nPartie [0-9]");
					ArrayList<String[]>chapitresParOeuvre=new ArrayList<String[]>();
				if (Parties.length>1&&nombreTotalDeChapitres>1){
					ArrayList<String>chapitresToutesParties=new ArrayList<String>();
					int chapitresPrecedents=0;
					for (String partie:Parties){
						partie=partie.replaceAll("[\\t\\n\\r]+", " ");
						String []chapitres=partie.split("Chapitre [0-9]+");
						for (String str:chapitres){
							if (!str.matches("[\\t\\n\\r\\s]+")&&!str.matches("[\\t\\n\\r\\s]*Partie [0-9]+[\\t\\n\\r\\s]*")&&!str.equals("")){	
								chapitresToutesParties.add(str);
							}
						}
						for(int counterChapitre=0; counterChapitre<chapitresToutesParties.size();counterChapitre++){
							if (chapitresToutesParties.size()>=(counterChapitre+chapitresPrecedents+1)){
								String numChapEtTxt[]=new String[5];
								numChapEtTxt[0]=String.valueOf(counterChapitre+chapitresPrecedents+1);//le numéro du chapitre
								numChapEtTxt[1]=chapitresToutesParties.get(counterChapitre+chapitresPrecedents);//le texte du chapitre
								StringTokenizer st = new StringTokenizer(chapitresToutesParties.get(counterChapitre+chapitresPrecedents));
								numChapEtTxt[2]=String.valueOf(st.countTokens());//le nombre de mots du chapitre
								numChapEtTxt[3]=String.valueOf(nombreTotalDeChapitres); //le nombre total de chapitres de l'oeuvre
								numChapEtTxt[4]=String.valueOf(nombreTotalMotsParTexte); //le nombre total de mots de l'oeuvre
								chapitresParOeuvre.add(numChapEtTxt);
							}
						}
						chapitresPrecedents=chapitresToutesParties.size();
					}
				}
				else if (Parties.length>1&&nombreTotalDeChapitres<1){
					String oeuvreParChapitres[]=wholeText.split("Partie [0-9]+");	
					nombreTotalDeChapitres=oeuvreParChapitres.length-1;
					for(int counterChapitre=0; counterChapitre<oeuvreParChapitres.length;counterChapitre++){
						if (!oeuvreParChapitres[counterChapitre].equals("")){
							oeuvreParChapitres[counterChapitre]=oeuvreParChapitres[counterChapitre].replaceAll("[\\t\\n\\r]+", " ");
							String numChapEtTxt[]=new String[5];
							numChapEtTxt[0]=String.valueOf(counterChapitre); //le numéro du chapitre
							numChapEtTxt[1]=oeuvreParChapitres[counterChapitre]; //le texte du chapitre
							StringTokenizer st = new StringTokenizer(oeuvreParChapitres[counterChapitre]);
							numChapEtTxt[2]=String.valueOf(st.countTokens()); //le nombre de mots du chapitre
							numChapEtTxt[3]=String.valueOf(nombreTotalDeChapitres); //le nombre total de chapitres de l'oeuvre
							numChapEtTxt[4]=String.valueOf(nombreTotalMotsParTexte); //le nombre total de mots de l'oeuvre
							chapitresParOeuvre.add(numChapEtTxt);
							
						}
					}
				}
				else{
					String oeuvreParChapitres[]=wholeText.split("Chapitre [0-9]+");	
					nombreTotalDeChapitres=oeuvreParChapitres.length-1;
					for(int counterChapitre=0; counterChapitre<oeuvreParChapitres.length;counterChapitre++){
						if (!oeuvreParChapitres[counterChapitre].equals("")){
							oeuvreParChapitres[counterChapitre]=oeuvreParChapitres[counterChapitre].replaceAll("[\\t\\n\\r]+", " ");
							String numChapEtTxt[]=new String[5];
							numChapEtTxt[0]=String.valueOf(counterChapitre); //le numéro du chapitre
							numChapEtTxt[1]=oeuvreParChapitres[counterChapitre]; //le texte du chapitre
							StringTokenizer st = new StringTokenizer(oeuvreParChapitres[counterChapitre]);
							numChapEtTxt[2]=String.valueOf(st.countTokens()); //le nombre de mots du chapitre
							numChapEtTxt[3]=String.valueOf(nombreTotalDeChapitres); //le nombre total de chapitres de l'oeuvre
							numChapEtTxt[4]=String.valueOf(nombreTotalMotsParTexte); //le nombre total de mots de l'oeuvre
							chapitresParOeuvre.add(numChapEtTxt);
						}
					}
				}
				mapDesOeuvres.put(file.getName(), chapitresParOeuvre);
			}
		}
		
		LinkedHashMap<String, List<float[]>> mapDesPourcentages=new LinkedHashMap<String, List<float[]>>();
		
		for (String fileName:mapDesOeuvres.keySet()){
			List<float[]>listeDesPourcentagesParTexte=new ArrayList<float[]>();
			List<String[]>cloneDesValeursAbsoluesParChapitre=new ArrayList<String[]>();
			cloneDesValeursAbsoluesParChapitre.addAll(mapDesOeuvres.get(fileName));
			for (int indexMap=0; indexMap<cloneDesValeursAbsoluesParChapitre.size(); indexMap++){
				String []tableauValeursParChapitre=cloneDesValeursAbsoluesParChapitre.get(indexMap);
				float []tableauDesStats=new float[3];
				tableauDesStats[0]=(Float.valueOf(tableauValeursParChapitre[0])*100)/Float.valueOf(tableauValeursParChapitre[3]); //numero relatif du chapitre
				tableauDesStats[1]=(Float.valueOf(tableauValeursParChapitre[2])*100)/Float.valueOf(tableauValeursParChapitre[4]); //nombre relatif de tokens
				tableauDesStats[2]=Float.valueOf(tableauValeursParChapitre[3]);
				
				listeDesPourcentagesParTexte.add(tableauDesStats);
			}
			mapDesPourcentages.put(fileName, listeDesPourcentagesParTexte);
			
		}
			ExportToCSV.exportToCSV("./CSVOutput/", "output",mapDesPourcentages);
	}
}