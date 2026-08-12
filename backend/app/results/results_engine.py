import json
import csv
import io
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer

from app.models.assessment import AssessmentResult

class ResultsEngine:
    @staticmethod
    def generate_json(result: AssessmentResult) -> str:
        """Generate JSON report"""
        return result.model_dump_json(indent=2)

    @staticmethod
    def generate_csv(result: AssessmentResult) -> str:
        """Generate CSV report"""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow(["Metric", "Value"])
        
        # Basic info
        writer.writerow(["Session ID", result.session_id])
        writer.writerow(["Timestamp", result.timestamp.isoformat()])
        writer.writerow([])
        
        # Scores
        writer.writerow(["Functional Vision Score", result.functional_vision_score])
        writer.writerow(["Overall Accuracy", result.overall_accuracy])
        writer.writerow(["Average Response Time (ms)", result.average_response_time_ms])
        writer.writerow(["Fastest Response (ms)", result.fastest_response_ms])
        writer.writerow(["Objects Detected", result.objects_detected])
        writer.writerow(["Levels Completed", result.levels_completed])
        writer.writerow([])
        
        # Performance
        writer.writerow(["Performance Summary", result.performance_summary])
        writer.writerow(["Recommendation", result.recommendation])
        writer.writerow([])
        
        # Level results
        writer.writerow(["Level", "Scenes Completed", "Total Scenes", "Correct Answers", 
                         "Total Answers", "Avg Response Time (ms)", "Accuracy"])
        for lr in result.level_results:
            writer.writerow([
                lr.level.value,
                lr.scenes_completed,
                lr.total_scenes,
                lr.correct_answers,
                lr.total_answers,
                lr.average_response_time_ms,
                lr.accuracy
            ])
        
        return output.getvalue()

    @staticmethod
    def generate_pdf(result: AssessmentResult) -> bytes:
        """Generate PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=18)
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30
        )
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12
        )
        
        story = []
        
        # Title
        story.append(Paragraph("Functional Vision Assessment Report", title_style))
        story.append(Spacer(1, 12))
        
        # Session info
        story.append(Paragraph("Session Information", heading_style))
        session_data = [
            ["Session ID:", result.session_id],
            ["Date:", result.timestamp.strftime("%B %d, %Y at %I:%M %p")]
        ]
        session_table = Table(session_data, colWidths=[2*inch, 4*inch])
        session_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(session_table)
        story.append(Spacer(1, 24))
        
        # Overall score
        story.append(Paragraph("Overall Results", heading_style))
        score_data = [
            ["Functional Vision Score:", f"{result.functional_vision_score}/100"],
            ["Overall Accuracy:", f"{result.overall_accuracy}%"],
            ["Average Response Time:", f"{result.average_response_time_ms} ms"],
            ["Fastest Response:", f"{result.fastest_response_ms} ms"],
            ["Objects Detected:", str(result.objects_detected)],
            ["Levels Completed:", f"{result.levels_completed}/{len(result.level_results)}"]
        ]
        score_table = Table(score_data, colWidths=[2.5*inch, 2*inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ECF0F1')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#2C3E50')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 24))
        
        # Performance summary
        story.append(Paragraph("Performance Summary", heading_style))
        story.append(Paragraph(f"<b>{result.performance_summary}</b>", styles['Normal']))
        story.append(Spacer(1, 6))
        story.append(Paragraph(result.recommendation, styles['Normal']))
        story.append(Spacer(1, 24))
        
        # Level results
        story.append(Paragraph("Level-by-Level Results", heading_style))
        level_data = [["Level", "Completed", "Accuracy", "Avg Time"]]
        for lr in result.level_results:
            level_data.append([
                f"Level {lr.level.value}",
                f"{lr.scenes_completed}/{lr.total_scenes}",
                f"{lr.accuracy:.1f}%",
                f"{lr.average_response_time_ms:.0f} ms"
            ])
        
        level_table = Table(level_data, colWidths=[1*inch, 1.2*inch, 1.2*inch, 1.5*inch])
        level_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#34495E')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 9),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F8F9F9')]),
            ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#BDC3C7')),
        ]))
        story.append(level_table)
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
