from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from datetime import datetime

def create_presentation():
    slide_deck = Presentation()
    slide_deck.slide_width = Inches(13.333)
    slide_deck.slide_height = Inches(7.5)
    return slide_deck

def add_title_slide(slide_deck, reporting_month):
    reporting_month_slide_str = reporting_month.strftime("%B, %Y")
    slide_title = f"Appendix A: New Pharmacies Added to Prime Watchlist - {reporting_month_slide_str}"
    slide = slide_deck.slides.add_slide(slide_deck.slide_layouts[6])
    title_box = slide.shapes.add_textbox(left=Inches(1), top=Inches(2.5), width=Inches(11), height=Inches(1.5))
    title_box.text_frame.text=slide_title
    title_box.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    title_box.text_frame.paragraphs[0].runs[0].font.size = Pt(30)
    title_box.text_frame.paragraphs[0].runs[0].font.bold = True
    title_box.text_frame.paragraphs[0].runs[0].font.color.rgb = RGBColor(31, 78, 121)
    title_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    return slide










if __name__ == "__main__":
    presentation = create_presentation()
    reporting_month = "2026-11"
    reporting_month = datetime.strptime(reporting_month, "%Y-%m")
    add_title_slide(presentation, reporting_month)
    presentation.save("output/test_presentation.pptx")
