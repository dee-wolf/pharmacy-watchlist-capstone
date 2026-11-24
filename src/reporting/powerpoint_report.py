from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from datetime import datetime
from pptx.oxml.xmlchemy import OxmlElement

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

def add_review_summary_slide(slide_deck, monthly_report, reviewed_count, reporting_month):
    matched_pharmacies = monthly_report[monthly_report["Final Status"] != "Not Participating"]
    unique_pharmacies = len(matched_pharmacies)
    reviewing_month_str = reporting_month.strftime("%B, %Y")
    boilerplate = f'We reviewed all {reviewed_count} pharmacies added to the Prime Watch List in {reviewing_month_str} for overlap with\nMedi-Cal enrolled pharmacies, {unique_pharmacies} unique pharmacies were identified.'
    slide = slide_deck.slides.add_slide(slide_deck.slide_layouts[6])
    summary_box = slide.shapes.add_textbox(left=Inches(0.75), top=Inches(0.75), width=Inches(11.83), height=Inches(1.5))
    summary_box.text_frame.text = boilerplate
    for paragraph in summary_box.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.LEFT
        paragraph.runs[0].font.size = Pt(18)
        paragraph.runs[0].font.color.rgb = RGBColor(31, 78, 121)
    summary_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    for start in range(0, len(matched_pharmacies), 5):
        current_five = matched_pharmacies.iloc[start:start + 5]
        if start == 0:
            pass
        else:
            slide = slide_deck.slides.add_slide(slide_deck.slide_layouts[6])
            continuation_box = slide.shapes.add_textbox(left=Inches(0.75), top=Inches(0.75), width=Inches(11.83), height=Inches(1.5))
            continuation_box.text_frame.text = "Pharmacies added to Watchlist: Continued"
            for paragraph in continuation_box.text_frame.paragraphs:
                paragraph.alignment = PP_ALIGN.LEFT
                paragraph.runs[0].font.size = Pt(18)
                paragraph.runs[0].font.color.rgb = RGBColor(31, 78, 121)
            continuation_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
        pharm_rows = len(current_five) + 1
        pharm_cols = 6
        pharm_table = slide.shapes.add_table(pharm_rows, pharm_cols, left=Inches(0.75), top=Inches(2.5), width=Inches(11.83), height=Inches(3.8)).table
        headers = ["NPI", "Pharmacy Name", "State", "12 Month Plan Paid", "12 Month Claim Count", "Notes/Recommendations"]
        for index, header in enumerate(headers):
            pharm_table.cell(0, index).text = header
            header_cell = pharm_table.cell(0, index)
            header_cell.fill.solid()
            header_cell.fill.fore_color.rgb = RGBColor(31, 78, 121)
            for paragraph in header_cell.text_frame.paragraphs:
                paragraph.runs[0].font.size = Pt(12)
                paragraph.runs[0].font.bold = True
                paragraph.runs[0].font.color.rgb = RGBColor(255, 255, 255)
                paragraph.alignment = PP_ALIGN.CENTER
        column_widths = [1.65, 2.25, 0.65, 1.45, 1.25, 4.58]
        for index, width in enumerate(column_widths):
            pharm_table.columns[index].width = Inches(width)
        for index, (row, pharmacy) in enumerate(current_five.iterrows(), start = 1):
            plan_paid = pharmacy["12 Month Plan Paid"]
            claim_count = pharmacy["12 Month Claim Count"]
            pharm_table.cell(index, 0).text = str(pharmacy["NPI"])
            pharm_table.cell(index, 1).text = str(pharmacy["Pharmacy Name"])
            pharm_table.cell(index, 2).text = "CA"
            pharm_table.cell(index, 3).text = f'${plan_paid:,.2f}'
            pharm_table.cell(index, 4).text = str(int(claim_count))
            pharm_table.cell(index, 5).text = ""
        for row in range(pharm_rows):
            for column in range(pharm_cols):
                pharm_table.cell(row, column).vertical_anchor = MSO_ANCHOR.MIDDLE
                pharm_table.cell(row, column).text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER
    return slide

def add_bullet(paragraph, level):
    pPr = paragraph._p.get_or_add_pPr()
    bullet = OxmlElement("a:buChar")
    bullet.set("char", "•")
    pPr.append(bullet)
    pPr.set("marL", str(457200 * (level + 1)))
    pPr.set("indent", "-228600")
    paragraph.level = level


def add_definitions_slide(slide_deck):
    slide = slide_deck.slides.add_slide(slide_deck.slide_layouts[6])
    title_box = slide.shapes.add_textbox(left=Inches(0.75), top=Inches(0.75), width=Inches(11.83), height=Inches(0.65))
    title_box.text_frame.text = "Watch List Reason definitions"
    for paragraph in title_box.text_frame.paragraphs:
        paragraph.alignment = PP_ALIGN.LEFT
        paragraph.runs[0].font.size = Pt(18)
        paragraph.runs[0].font.color.rgb = RGBColor(31, 78, 121)
    title_box.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    definitions_box = slide.shapes.add_textbox(left=Inches(0.75), top=Inches(1.6), width=Inches(11.83), height=Inches(5.5))
    definitions_box.text_frame.word_wrap = True
    definitions_box.text_frame.margin_left = Inches(0.1)
    definitions_box.text_frame.margin_right = Inches(0.1)
    fwa_paragraph = definitions_box.text_frame.paragraphs[0]
    fwa_paragraph.text = "FWA Issue/FWA Triage = Pharmacy is not currently contracted and was subject of FWA report."
    add_bullet(fwa_paragraph, 0)
    industry_paragraph = definitions_box.text_frame.add_paragraph()
    industry_paragraph.text = "Industry Alert = Pharmacy is not currently contracted and is the subject of a CMS Industry Fraud Alert"
    add_bullet(industry_paragraph, 0)
    denial_paragraph = definitions_box.text_frame.add_paragraph()
    denial_paragraph.text = "Network Denial/Network Denial (PTM) = Pharmacy was declined participation in networks through pre-credentialing process due to FWA."
    add_bullet(denial_paragraph, 0)
    termination_paragraph = definitions_box.text_frame.add_paragraph()
    add_bullet(termination_paragraph, 0)
    termination_paragraph.text = "Network Termination/Network Termination (PTM) = Pharmacy was terminated from networks due to FWA."
    factor_paragraph = definitions_box.text_frame.add_paragraph()
    factor_paragraph.text = "Network termination is considered based on the following factors, which may include but are not limited to:"
    add_bullet(factor_paragraph, 1)
    reason1_paragraph = definitions_box.text_frame.add_paragraph()
    reason1_paragraph.text = "Evidence of fraud, or intentional or willful waste or abuse, or admission of fraud or abuse."
    add_bullet(reason1_paragraph, 2)
    reason2_paragraph = definitions_box.text_frame.add_paragraph()
    reason2_paragraph.text = "Not purchasing sufficient quantity of product to support the quantities billed by pharmacy."
    add_bullet(reason2_paragraph, 2)
    reason3_paragraph = definitions_box.text_frame.add_paragraph()
    reason3_paragraph.text = "Patient safety concerns."
    add_bullet(reason3_paragraph, 2)
    reason4_paragraph = definitions_box.text_frame.add_paragraph()
    reason4_paragraph.text = "Non-compliance with applicable federal or state laws, the Pharmacy Participation Agreement or the Prime Provider Manual."
    add_bullet(reason4_paragraph, 2)
    reason5_paragraph = definitions_box.text_frame.add_paragraph()
    reason5_paragraph.text = "Non-compliance with corrective action plan(s)."
    add_bullet(reason5_paragraph, 2)
    rfi_paragraph = definitions_box.text_frame.add_paragraph()
    rfi_paragraph.text = "Request for Information = Pharmacy is not currently contracted and has had a Request for Information received from a government agency."
    add_bullet(rfi_paragraph, 0)
    ndt_paragraph = definitions_box.text_frame.add_paragraph()
    ndt_paragraph.text = "Network Denial or Termination = Pharmacy was declined participation or terminated from networks due to FWA."
    add_bullet(ndt_paragraph, 0)
    for paragraph in definitions_box.text_frame.paragraphs:
        for run in paragraph.runs:
            run.font.size = Pt(14)

if __name__ == "__main__":
    from src.generators.watchlist import generate_watchlist
    from src.generators.claims import generate_claims
    from src.processors.claims_processor import (
        load_claims,
        exclude_test_claims,
        aggregate_claims
    )
    from src.processors.watchlist_processor import (
        match_enrollment,
        merge_claims_with_watchlist,
        assign_final_status
    )
    from src.reporting.excel_report import filter_reporting_month
    reporting_month = datetime.strptime("2026-11", "%Y-%m")
    watchlist = generate_watchlist(
        reporting_month=reporting_month.strftime("%Y-%m")
    )
    claims = generate_claims(watchlist)
    network = load_claims("data/raw/enrolled_pharmacies.xlsx")
    filtered_claims = exclude_test_claims(claims)
    aggregated_claims = aggregate_claims(filtered_claims)
    enrollment_match = match_enrollment(watchlist, network)
    merged_watchlist = merge_claims_with_watchlist(
        enrollment_match, aggregated_claims
    )
    merged_watchlist = assign_final_status(merged_watchlist)
    monthly_report = filter_reporting_month(
        merged_watchlist, reporting_month
    )
    reviewed_count = len(monthly_report)
    presentation = create_presentation()
    add_title_slide(presentation, reporting_month)
    add_review_summary_slide(
        presentation,
        monthly_report,
        reviewed_count,
        reporting_month
    )
    add_definitions_slide(presentation)
    presentation.save(f'output/{reporting_month}_presentation.pptx')
