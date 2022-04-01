""" creates watermarks """

from io import BytesIO
import math

from reportlab.pdfgen import canvas
# The size of the page supposedly A4
from reportlab.lib.pagesizes import A4
# The color of the watermark
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
FONTNAME = 'Helvetica-Bold'

def _get_text_height(fontname, fontsize):
    face = pdfmetrics.getFont(fontname).face
    ascent = (face.ascent * fontsize) / 1000.0
    descent = (face.descent * fontsize) / 1000.0
    return ascent # - descent

def _compute_font_size(wm_text, font_name=FONTNAME, pagesize=A4, margin_x=40, margin_y=40):
    FONTSIZE = 40
    text_width = pdfmetrics.stringWidth(wm_text, font_name, FONTSIZE)
    ratio = _get_text_height(font_name, FONTSIZE)/text_width
    # ys = fh/2/sin(a)
    # Y0-ys = fw*cos(a)
    # Y0 = fw*ratio/2/sin(a) + fw*cos(a) = fw(cos(a) + ratio/2/sin(a))
    X0 = pagesize[0] - 2*margin_x
    Y0 = pagesize[1] - 2*margin_y
    alpha = math.atan(X0/Y0)

    fw = Y0 / (math.cos(alpha) + ratio/2/math.sin(alpha))
    dX = fw*math.cos(alpha)
    return FONTSIZE * fw / text_width * 0.95, alpha

    alpha_degree = math.degrees(alpha)

    ROTATION_ANGLE = -math.degrees(math.atan(PAGESIZE[1]/PAGESIZE[0]))

    text_width = pdfmetrics.stringWidth(wm_text, FONTNAME, FONTSIZE)
    ratio = get_text_height(FONTNAME, FONTSIZE)/text_width

    # xt = math.sqrt((Y0-ys)*(Y0-ys) + X0*X0)
    # alpha = math.acos(ys/xt)
    # alpha1 = math.atan(ys/(ratio*(Y0 - X0 + ratio*Y0)))
    # print(alpha, alpha1)
    # print(ratio)
    FONTSIZE = FONTSIZE * fw / text_width * 0.95
    text_height = get_text_height(font_name, FONTSIZE)
    text_width = pdfmetrics.stringWidth(wm_text, font_name, FONTSIZE)

def create_watermark(wm_text, color=colors.lightgrey , font_name=FONTNAME, pagesize=A4, margin_x=40, margin_y=40, alpha=0.2):
    # The position attributes of the watermark
    # print(X0, Y0)
    # The rotation angle in order to display the watermark diagonally if needed
    X0 = pagesize[0] - 2*margin_x
    Y0 = pagesize[1] - 2*margin_y
    fontsize, alpha = _compute_font_size(
        wm_text,
        font_name=font_name,
        pagesize=pagesize,
        margin_x=margin_x,
        margin_y=margin_y)
    orientation_degree = - 90 + math.degrees(alpha)
    
    text_height = _get_text_height(font_name, fontsize)
    text_width = pdfmetrics.stringWidth(wm_text, font_name, fontsize)
    output_buffer = BytesIO()
    # Default Page Size = A4
    c = canvas.Canvas(output_buffer, pagesize=pagesize)
    # you can also add image instead of text
    # c.drawImage("logo.png", X, Y, 160, 160)
    # Set the size and type of the font
    c.setFont(font_name, fontsize)
    # Set the color
    if isinstance(color, tuple):
        color = (c/255 for c in color)
        c.setFillColorRGB(*color, alpha=alpha)
    else:
        c.setFillColor(color, alpha=alpha)
    # Rotate according to the configured parameter
    c.translate(pagesize[0]/2, pagesize[1]/2)
    c.rotate(orientation_degree)
    # c.rotate(45)
    # c.line(0, 0, 100, 0)
    # c.line(-text_width / 2, 0, text_width / 2 , 0)
    # c.line(0,- text_height/2 ,0, text_height/2)
    # Position according to the configured parameter
    c.drawString(-text_width/2, -text_height/2, wm_text)
    c.save()
    return output_buffer

if __name__ == "__main__":
    with open('wm.pdf', "wb") as wm_file:
        wm_file.write(create_watermark("ZAHLUNGSERINNERUNG").getbuffer())

