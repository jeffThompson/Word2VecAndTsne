
/*
VISUALIZE VECTOR SPACE
Jeff Thompson | 2016-17 | jeffreythompson.org

Creates a visualization of a 2D vector space.

*/

String modelFilename =  "../ModelsAndData/TimeMachine-2D-NORMALIZED-GRID.csv";
String outputFilename = "../ModelsAndData/TimeMachine-GRID.png";

boolean normalize =     true;        // normalize coordinates of data?
float minX =            0;           // if so, what are the min/max?
float maxX =            25;          // if not, assumes already normalized -1 to 1
float minY =            0;
float maxY =            26;

int margin =            100;          // space around visualization
int fontSize =          12;           // in px
String fontName =       "Arial";      // font to load (must be local)


void setup() {
  
  // create PGraphics to draw into
  println("- creating PGraphics context...");
  PGraphics pg = createGraphics(2000,2000);
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
    
    float x = Float.parseFloat(data[1]);
    float y = Float.parseFloat(data[2]);
    if (normalize) {
      x = map(x, minX,maxX, -1,1);
      y = map(y, minY,maxY, -1,1);
    }
    x *= (pg.width/2 - margin*2);
    y *= (pg.height/2 - margin*2);
    
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