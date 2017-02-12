
/*
VISUALIZE VECTOR SPACE
Jeff Thompson | 2016-17 | jeffreythompson.org

Creates a visualization of a 2D vector space.

*/

String modelFilename =  "../WikipediaDump-POS-2D-NORMALIZED.csv";
String outputFilename = "../WikipediaDump-POS-2D-NORMALIZED.png";

int margin =            100;                    // space around visualization
int fontSize =          12;                     // in px
String fontName =       "CooperHewitt-Book";    // font to load (must be local)


void setup() {
  
  // create PGraphics to draw into
  println("- creating PGraphics context...");
  PGraphics pg = createGraphics(8000,8000);
  pg.beginDraw();
  pg.background(255);
  
  // font
  println("- loading font...");
  pg.textAlign(CENTER, CENTER);
  PFont font = createFont(fontName, fontSize);
  pg.textFont(font, fontSize);
  
  // draw words in place
  println("- drawing words...");
  pg.pushMatrix();
  pg.translate(pg.width/2, pg.height/2);
  String[] words = loadStrings(modelFilename);
  for (int i=0; i<words.length; i++) {
    String[] data = words[i].split(",");
    String word = data[0];
    float x = Float.parseFloat(data[1]) * (pg.width/2 - margin*2);
    float y = Float.parseFloat(data[2]) * (pg.height/2 - margin*2);
    
    pg.fill(0);
    pg.noStroke();
    pg.text(word, x,y);
  }
  pg.popMatrix();
  pg.endDraw();
  
  // save it and quit
  println("- saving to file...");
  pg.save(outputFilename);
  println("- done, bye");
  exit();
}