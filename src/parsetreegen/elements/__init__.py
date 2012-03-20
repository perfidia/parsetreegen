from pysvg.core import BaseElement;

class Marker(BaseElement):
    def __init__(self, id, refX = "10", refY = "12.5", markerWidth = "9", markerHeight = "30", markerUnits = "strokeWidth", orient = "auto"):
        BaseElement.__init__(self, 'marker');
        
        self.setAttribute("id", id);
        self.setAttribute("viewBox", "0 0 30 30");
        self.setAttribute("refX", refX);
        self.setAttribute("refY", refY);
        self.setAttribute("markerUnits", markerUnits);
        self.setAttribute("markerWidth", markerWidth);
        self.setAttribute("markerHeight", markerHeight);
        self.setAttribute("orient", orient);
        
        self.addElement(Path("M0.3125 0.625 9.3125 12.625 0.3125 24.625 21.3125 12.625 Z"));
      
      
class Path(BaseElement):
    def __init__(self, d):
        BaseElement.__init__(self, 'path');
        
        self.setAttribute("style", "stroke-width:1;stroke:black;fill:black;opacity:1");
        self.setAttribute("d", d);