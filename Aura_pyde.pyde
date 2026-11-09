
# Aura prototype - single colour gradient
# Click or drag inside the oval to show how you feel.

MAP_CX, MAP_CY = 640, 290
MAP_RX, MAP_RY = 170, 190

WORDS = [("tense", -0.25, 0.88), ("nervous", -0.48, 0.69), ("stressed", -0.60, 0.46),
         ("upset", -0.70, 0.21), ("alert", 0.21, 0.91), ("excited", 0.43, 0.75),
         ("elated", 0.60, 0.53), ("happy", 0.66, 0.25), ("sad", -0.70, -0.18),
         ("depressed", -0.58, -0.48), ("bored", -0.41, -0.76), ("contented", 0.71, -0.18),
         ("serene", 0.66, -0.41), ("relaxed", 0.54, -0.59), ("calm", 0.34, -0.77)]

valence = arousal = target_v = target_a = 0.5
phase = 0.0
cells = []

def setup():
    size(900, 540)
    colorMode(HSB, 360, 100, 100, 100)
    noStroke()
    ellipseMode(RADIUS)
    frameRate(30)

    for i in range(36):
        for j in range(36):
            v = (i + 0.5) / 36.0
            a = 1 - (j + 0.5) / 36.0
            if (2*v-1)**2 + (2*a-1)**2 <= 1:
                h, s, b = emotionColour(v, a)
                cells.append((MAP_CX-MAP_RX+i*MAP_RX/18.0,
                              MAP_CY-MAP_RY+j*MAP_RY/18.0, h, s, b))

def draw():
    global valence, arousal, phase

    valence = lerp(valence, target_v, 0.05)
    arousal = lerp(arousal, target_a, 0.05)
    phase += lerp(0.03, 0.1, arousal)

    h, s, b = emotionColour(valence, arousal)

    background(30, 8, 98)
    drawAura(230, 290, 110+12*sin(phase), h, s, b)
    drawMap()

def emotionColour(v, a):
    x = v*2-1
    y = a*2-1
    angle = degrees(atan2(y, x))
    strength = min(1.0, sqrt(x*x+y*y))

    h = (105-angle) % 360
    s = lerp(8, 50, strength)
    b = lerp(85, 100, a)

    return h, s, b

def drawAura(x, y, radius, h, s, b):

    # Create a gradient using one consistent hue
    layers = 120

    for i in range(layers):
        f = i / float(layers-1)
        r = radius * 1.25 * (1-f)

        # Fade the outer edge
        fade = constrain(f/0.22, 0, 1)
        alpha = 100 * fade

        # Change saturation and brightness, not hue
        saturation = lerp(10, 90, f)
        brightness = lerp(100, 65, f)

        fill(h, saturation, brightness, alpha)
        ellipse(x, y, r, r)

def drawMap():
    for x, y, h, s, b in cells:
        fill(h, s, b)
        rect(x, y, MAP_RX/18.0+1, MAP_RY/18.0+1)

    stroke(0, 0, 100, 60)
    noFill()
    ellipse(MAP_CX, MAP_CY, MAP_RX, MAP_RY)
    line(MAP_CX-MAP_RX, MAP_CY, MAP_CX+MAP_RX, MAP_CY)
    line(MAP_CX, MAP_CY-MAP_RY, MAP_CX, MAP_CY+MAP_RY)

    stroke(0, 0, 100)
    strokeWeight(2)
    ellipse(MAP_CX+(target_v*2-1)*MAP_RX,
            MAP_CY-(target_a*2-1)*MAP_RY, 8, 8)
    strokeWeight(1)
    noStroke()

    textSize(12)
    textAlign(CENTER, CENTER)
    fill(0, 0, 15, 75)

    for word, v, a in WORDS:
        text(word, MAP_CX+v*MAP_RX, MAP_CY-a*MAP_RY)

    fill(0, 0, 15, 80)
    text("ENERGISED", MAP_CX, MAP_CY-MAP_RY-18)
    text("CALM", MAP_CX, MAP_CY+MAP_RY+18)
    text("UNPLEASANT", MAP_CX-MAP_RX-50, MAP_CY)
    text("PLEASANT", MAP_CX+MAP_RX+45, MAP_CY)
    text("Click or drag inside the oval to show how you feel", MAP_CX, 40)

def mousePressed():
    setFeeling()

def mouseDragged():
    setFeeling()

def setFeeling():
    global target_v, target_a

    dx = (mouseX-MAP_CX)/float(MAP_RX)
    dy = (MAP_CY-mouseY)/float(MAP_RY)

    if dx*dx+dy*dy <= 1:
        target_v = (dx+1)/2.0
        target_a = (dy+1)/2.0
