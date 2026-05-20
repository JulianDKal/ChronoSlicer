import pymupdf
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from typing import List, Dict, Any
import uuid
from pathlib import Path
import json

router = APIRouter()

# Inside your FastAPI endpoint
@router.get("/save_pdf")
async def create_pdf_from_json():
    with open(Path('uploads/page_0_lines.json'), 'r') as file:
        lines = json.load(file)
    # for line in lines:
    #     print(line)
    output_path = Path('uploads/laser_drawing.pdf')
    create_pdf_from_lines(lines, output_path)
    
    return FileResponse(output_path, filename="laser_drawing.pdf")


def create_pdf_from_lines(line_data, output_path="output.pdf"):
    # Create a new PDF document and add a blank page
    doc = pymupdf.open()

    # Get page dimensions (default A4: 595 x 842 points)
    page_width = 2880.0000
    page_height = 2015.4331

    # rect = pymupdf.Rect(0, 0, page_width, page_height)
    page = doc.new_page(width=page_width, height=page_height)
    
    shape = page.new_shape()
    
    for line in line_data:
        if line['type'] == 'l':
            x1 = line['x1']
            y1 = line['y1'] 
            x2 = line['x2']
            y2 = line['y2']
            shape.draw_line((x1, y1), (x2, y2))
        if line['type'] == 'c':
            x1 = line['x1']
            y1 = line['y1'] 
            x2 = line['x2']
            y2 = line['y2']
            x3 = line['x3']
            y3 = line['y3']
            x4 = line['x4']
            y4 = line['y4']
            shape.draw_bezier((x1, y1), (x2, y2), (x3, y3), (x4, y4))

        # Get color (default to black if not specified)
        color = line.get('color', '#000000')
        # Convert hex to RGB tuple (values 0-1)
        r = int(color[1:3], 16) / 255.0
        g = int(color[3:5], 16) / 255.0
        b = int(color[5:7], 16) / 255.0
        
        shape.finish(color=(r, g, b), width=0.1, closePath=False)
    
    shape.commit() 
    
    # Save the PDF
    doc.save(output_path)
    doc.close()
    
    return output_path