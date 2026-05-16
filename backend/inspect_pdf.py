import fitz  # PyMuPDF
import json

def inspect_pdf(pdf_path):
    """Analyze a PDF and print its drawing structure"""
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    print(f"PDF has {len(doc)} pages\n")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"\n{'='*50}")
        print(f"Page {page_num + 1}")
        print(f"Page size: {page.rect.width} x {page.rect.height}")
        
        # Extract all drawings (vector graphics) from this page
        drawings = page.get_drawings()
        print(f"Found {len(drawings)} drawing path(s)")
        
        all_lines = []
        
        for drawing_idx, drawing in enumerate(drawings):
            print(f"\n  Drawing {drawing_idx + 1}:")
            print(f"    - Color: {drawing.get('color', 'None')}")
            print(f"    - Fill: {drawing.get('fill', 'None')}")
            print(f"    - Width: {drawing.get('width', 1)}")
            print(f"    - Items: {len(drawing['items'])} operations")
            
            # Process each drawing item
            for item in drawing['items']:
                # item[0] is the operation type:
                # 'l' = line, 're' = rectangle, 'c' = bezier curve, 'qu' = quad
                if item[0] == 'l':  # Line segment
                    start = item[1]  # Point (x1, y1)
                    end = item[2]    # Point (x2, y2)
                    all_lines.append({
                        "x1": start.x,
                        "y1": start.y,
                        "x2": end.x,
                        "y2": end.y
                    })
                    print(f"      Line: ({start.x:.2f}, {start.y:.2f}) → ({end.x:.2f}, {end.y:.2f})")
                
                elif item[0] == 're':  # Rectangle
                    rect = item[1]
                    print(f"      Rectangle: {rect}")
                    # Convert rectangle to 4 lines (optional)
                    all_lines.extend(rectangle_to_lines(rect))
                
                elif item[0] == 'c':  # Bezier curve
                    print(f"      Bezier curve: {item[1]} → {item[2]} → {item[3]} → {item[4]}")
                    # For curves, you may want to flatten them into line segments
                    # (More advanced - leave for later if needed)
        
        print(f"\n  Total line segments extracted: {len(all_lines)}")
        
        # Save to JSON for inspection
        with open(f"page_{page_num}_lines.json", "w") as f:
            json.dump(all_lines, f, indent=2)
    
    doc.close()
    print("\n✓ Inspection complete. Check the generated JSON files.")


def rectangle_to_lines(rect):
    """Convert a rectangle (x0,y0,x1,y1) into 4 line segments"""
    x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
    return [
        {"x1": x0, "y1": y0, "x2": x1, "y2": y0},  # Top edge
        {"x1": x1, "y1": y0, "x2": x1, "y2": y1},  # Right edge
        {"x1": x1, "y1": y1, "x2": x0, "y2": y1},  # Bottom edge
        {"x1": x0, "y1": y1, "x2": x0, "y2": y0},  # Left edge
    ]


if __name__ == "__main__":
    # Replace with your actual PDF file path
    import sys
    if len(sys.argv) > 1:
        inspect_pdf(sys.argv[1])
    else:
        print("Usage: python inspect_pdf.py <path_to_pdf>")