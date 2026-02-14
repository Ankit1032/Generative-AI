"""
PyMuPDF (fitz) Complete Guide
==============================
A comprehensive tutorial covering all PyMuPDF capabilities
"""

import fitz  # PyMuPDF
import os
from pathlib import Path

# ============================================================================
# PART 1: OPENING AND BASIC OPERATIONS
# ============================================================================

def open_documents():
    """Different ways to open PDF documents"""
    
    # Open existing PDF
    doc = fitz.open("example.pdf")
    
    # Open from bytes
    with open("example.pdf", "rb") as f:
        pdf_bytes = f.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    # Create new blank PDF
    doc = fitz.open()
    
    # Open other formats (images, EPUB, etc.)
    # doc = fitz.open("image.png")
    # doc = fitz.open("book.epub")
    
    return doc

def basic_document_info(doc):
    """Get basic document information"""
    
    print(f"Number of pages: {len(doc)}")
    print(f"Page count: {doc.page_count}")
    print(f"Metadata: {doc.metadata}")
    print(f"Is PDF: {doc.is_pdf}")
    print(f"Is encrypted: {doc.is_encrypted}")
    print(f"Needs password: {doc.needs_pass}")
    print(f"File size: {len(doc.tobytes())} bytes")
    
    # Metadata dictionary keys:
    # 'format', 'title', 'author', 'subject', 'keywords',
    # 'creator', 'producer', 'creationDate', 'modDate'

# ============================================================================
# PART 2: CREATING PDFs FROM SCRATCH
# ============================================================================

def create_simple_pdf():
    """Create a simple PDF with text"""
    
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size
    
    # Insert text
    text = "Hello, PyMuPDF!"
    point = fitz.Point(50, 50)
    page.insert_text(point, text, fontsize=20, color=(0, 0, 1))
    
    # Save
    doc.save("/home/claude/simple.pdf")
    doc.close()
    print("Created simple.pdf")

def create_multipage_pdf():
    """Create multi-page PDF with various content"""
    
    doc = fitz.open()
    
    for i in range(5):
        page = doc.new_page()
        
        # Add page number
        text = f"Page {i + 1}"
        page.insert_text((50, 50), text, fontsize=30)
        
        # Add some content
        content = f"This is the content of page {i + 1}.\n"
        content += "PyMuPDF makes PDF creation easy!"
        page.insert_text((50, 100), content, fontsize=12)
    
    doc.save("/home/claude/multipage.pdf")
    doc.close()
    print("Created multipage.pdf")

# ============================================================================
# PART 3: TEXT OPERATIONS
# ============================================================================

def extract_text_examples():
    """Various text extraction methods"""
    
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Sample text for extraction", fontsize=14)
    doc.save("/home/claude/text_sample.pdf")
    
    # Re-open to extract
    doc = fitz.open("/home/claude/text_sample.pdf")
    page = doc[0]
    
    # Method 1: Simple text extraction
    text = page.get_text()
    print("Simple extraction:", text)
    
    # Method 2: Preserve layout
    text = page.get_text("text")
    
    # Method 3: Get text as blocks
    blocks = page.get_text("blocks")
    # Returns: (x0, y0, x1, y1, "text", block_no, block_type)
    
    # Method 4: Get text as dict (most detailed)
    text_dict = page.get_text("dict")
    # Contains: width, height, blocks with detailed font info
    
    # Method 5: Get text as HTML
    html = page.get_text("html")
    
    # Method 6: Get text as XHTML
    xhtml = page.get_text("xhtml")
    
    # Method 7: Get text as XML
    xml = page.get_text("xml")
    
    # Method 8: Search for text
    search_results = page.search_for("Sample")
    print("Search results (rectangles):", search_results)
    
    doc.close()

def text_formatting_advanced():
    """Advanced text insertion with formatting"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Basic text with color
    page.insert_text((50, 50), "Red Text", fontsize=20, color=(1, 0, 0))
    
    # Text with different fonts
    # Built-in fonts: helv, tiro, cour, zadb, symb
    page.insert_text((50, 80), "Helvetica", fontname="helv", fontsize=12)
    page.insert_text((50, 100), "Courier", fontname="cour", fontsize=12)
    
    # Text rotation
    page.insert_text((50, 150), "Rotated 45°", fontsize=14, rotate=45)
    
    # Text with overlay
    rc = page.insert_text((50, 200), "Overlay text", fontsize=14, 
                          overlay=True, color=(0, 0, 1))
    
    # Multiline text
    text = "Line 1\nLine 2\nLine 3"
    page.insert_text((50, 250), text, fontsize=12)
    
    # Text in a rectangle (textbox)
    rect = fitz.Rect(50, 300, 300, 400)
    page.insert_textbox(rect, "This text will wrap within the rectangle. " * 10,
                       fontsize=11, align=0)  # 0=left, 1=center, 2=right
    
    doc.save("/home/claude/formatted_text.pdf")
    doc.close()
    print("Created formatted_text.pdf")

# ============================================================================
# PART 4: IMAGE OPERATIONS
# ============================================================================

def image_operations():
    """Working with images in PDFs"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # We'll create a simple image programmatically
    # In practice, you'd use actual image files
    
    # Insert image from file (if you have one)
    # rect = fitz.Rect(50, 50, 250, 250)
    # page.insert_image(rect, filename="image.png")
    
    # Insert image from bytes
    # with open("image.png", "rb") as f:
    #     img_bytes = f.read()
    # page.insert_image(rect, stream=img_bytes)
    
    # Extract images from existing PDF
    # for img_index, img in enumerate(page.get_images()):
    #     xref = img[0]
    #     base_image = doc.extract_image(xref)
    #     image_bytes = base_image["image"]
    #     image_ext = base_image["ext"]
    #     with open(f"image_{img_index}.{image_ext}", "wb") as f:
    #         f.write(image_bytes)
    
    doc.save("/home/claude/with_images.pdf")
    doc.close()

# ============================================================================
# PART 5: DRAWING AND SHAPES
# ============================================================================

def drawing_shapes():
    """Draw various shapes on PDF pages"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    shape = page.new_shape()
    
    # Draw rectangle
    rect = fitz.Rect(50, 50, 200, 150)
    shape.draw_rect(rect)
    shape.finish(color=(1, 0, 0), fill=(1, 1, 0), width=2)
    
    # Draw circle
    circle_center = fitz.Point(300, 100)
    shape.draw_circle(circle_center, 40)
    shape.finish(color=(0, 0, 1), fill=(0.8, 0.8, 1), width=1.5)
    
    # Draw line
    p1 = fitz.Point(50, 200)
    p2 = fitz.Point(200, 250)
    shape.draw_line(p1, p2)
    shape.finish(color=(0, 1, 0), width=3)
    
    # Draw polyline
    points = [fitz.Point(250, 200), fitz.Point(300, 220), 
              fitz.Point(350, 200), fitz.Point(400, 240)]
    shape.draw_polyline(points)
    shape.finish(color=(1, 0, 1), width=2)
    
    # Draw bezier curve
    p1 = fitz.Point(50, 300)
    p2 = fitz.Point(150, 250)
    p3 = fitz.Point(250, 350)
    p4 = fitz.Point(350, 300)
    shape.draw_bezier(p1, p2, p3, p4)
    shape.finish(color=(0.5, 0, 0.5), width=2)
    
    # Draw oval
    rect = fitz.Rect(400, 50, 550, 150)
    shape.draw_oval(rect)
    shape.finish(color=(1, 0.5, 0), fill=(1, 1, 0.8), width=2)
    
    # Draw sector (pie slice)
    center = fitz.Point(475, 350)
    shape.draw_sector(center, center + (50, 0), 90)
    shape.finish(color=(0, 0.5, 0.5), fill=(0.8, 1, 1), width=1)
    
    shape.commit()  # Apply all drawings
    
    doc.save("/home/claude/shapes.pdf")
    doc.close()
    print("Created shapes.pdf")

# ============================================================================
# PART 6: ANNOTATIONS
# ============================================================================

def add_annotations():
    """Add various types of annotations"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Text annotation (note icon)
    point = fitz.Point(50, 50)
    annot = page.add_text_annot(point, "This is a text annotation")
    
    # Free text annotation (text box)
    rect = fitz.Rect(50, 100, 300, 150)
    annot = page.add_freetext_annot(rect, "Free text annotation",
                                     fontsize=12, text_color=(0, 0, 1))
    
    # Highlight annotation
    # First, we need text to highlight
    page.insert_text((50, 200), "This text will be highlighted", fontsize=14)
    quads = page.search_for("text will be")
    if quads:
        annot = page.add_highlight_annot(quads)
    
    # Strikeout annotation
    page.insert_text((50, 250), "This text will be struck out", fontsize=14)
    quads = page.search_for("struck out")
    if quads:
        annot = page.add_strikeout_annot(quads)
    
    # Underline annotation
    page.insert_text((50, 300), "This text will be underlined", fontsize=14)
    quads = page.search_for("underlined")
    if quads:
        annot = page.add_underline_annot(quads)
    
    # Squiggly (wavy underline) annotation
    page.insert_text((50, 350), "This text will have squiggly underline", fontsize=14)
    quads = page.search_for("squiggly")
    if quads:
        annot = page.add_squiggly_annot(quads)
    
    # Rectangle annotation
    rect = fitz.Rect(50, 400, 200, 450)
    annot = page.add_rect_annot(rect)
    annot.set_colors(stroke=(1, 0, 0), fill=(1, 1, 0))
    annot.set_opacity(0.5)
    annot.update()
    
    # Circle annotation
    rect = fitz.Rect(250, 400, 350, 500)
    annot = page.add_circle_annot(rect)
    annot.set_colors(stroke=(0, 0, 1))
    annot.update()
    
    # Polygon annotation
    points = [fitz.Point(400, 400), fitz.Point(450, 420), 
              fitz.Point(500, 400), fitz.Point(475, 450)]
    annot = page.add_polygon_annot(points)
    annot.set_colors(stroke=(0, 1, 0), fill=(0.8, 1, 0.8))
    annot.update()
    
    # Ink annotation (freehand drawing)
    ink_list = [
        [fitz.Point(50, 550), fitz.Point(100, 560), fitz.Point(150, 550)],
        [fitz.Point(50, 570), fitz.Point(100, 580), fitz.Point(150, 570)]
    ]
    annot = page.add_ink_annot(ink_list)
    annot.set_colors(stroke=(1, 0, 1))
    annot.update()
    
    # Stamp annotation
    rect = fitz.Rect(250, 500, 350, 550)
    annot = page.add_stamp_annot(rect, stamp=0)  # 0 = "Approved"
    
    doc.save("/home/claude/annotations.pdf")
    doc.close()
    print("Created annotations.pdf")

# ============================================================================
# PART 7: MERGING AND SPLITTING PDFs
# ============================================================================

def merge_pdfs():
    """Merge multiple PDFs into one"""
    
    # Create sample PDFs first
    for i in range(3):
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((50, 50), f"Document {i+1}", fontsize=20)
        doc.save(f"/home/claude/doc_{i+1}.pdf")
        doc.close()
    
    # Merge them
    merged = fitz.open()
    
    for i in range(3):
        doc = fitz.open(f"/home/claude/doc_{i+1}.pdf")
        merged.insert_pdf(doc)
        doc.close()
    
    merged.save("/home/claude/merged.pdf")
    merged.close()
    print("Created merged.pdf")

def split_pdf():
    """Split a PDF into separate pages"""
    
    # Create a multi-page PDF first
    doc = fitz.open()
    for i in range(5):
        page = doc.new_page()
        page.insert_text((50, 50), f"Page {i+1}", fontsize=20)
    doc.save("/home/claude/to_split.pdf")
    doc.close()
    
    # Split it
    doc = fitz.open("/home/claude/to_split.pdf")
    
    for page_num in range(len(doc)):
        # Create new PDF with single page
        new_doc = fitz.open()
        new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)
        new_doc.save(f"/home/claude/page_{page_num+1}.pdf")
        new_doc.close()
    
    doc.close()
    print("Split PDF into individual pages")

# ============================================================================
# PART 8: PAGE MANIPULATION
# ============================================================================

def page_operations():
    """Various page manipulation operations"""
    
    doc = fitz.open()
    
    # Add pages of different sizes
    page1 = doc.new_page(width=595, height=842)  # A4
    page2 = doc.new_page(width=612, height=792)  # Letter
    page3 = doc.new_page(pno=1)  # Insert at position 1
    
    # Delete page
    doc.delete_page(2)
    
    # Copy page
    doc.copy_page(0)  # Copy page 0 to end
    
    # Move page
    doc.move_page(1, 0)  # Move page 1 to position 0
    
    # Rotate page
    page = doc[0]
    page.set_rotation(90)  # Rotate 90 degrees
    
    # Get page size
    rect = page.rect
    print(f"Page size: {rect.width} x {rect.height}")
    
    doc.save("/home/claude/page_ops.pdf")
    doc.close()

# ============================================================================
# PART 9: WATERMARKS AND OVERLAYS
# ============================================================================

def add_watermark():
    """Add watermark to PDF pages"""
    
    # Create source document
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Original content", fontsize=14)
    doc.save("/home/claude/original.pdf")
    doc.close()
    
    # Add watermark
    doc = fitz.open("/home/claude/original.pdf")
    page = doc[0]
    
    # Add text watermark
    text = "CONFIDENTIAL"
    fontsize = 50
    opacity = 0.3
    
    # Calculate center position
    text_width = fitz.get_text_length(text, fontname="helv", fontsize=fontsize)
    point = fitz.Point((page.rect.width - text_width) / 2, page.rect.height / 2)
    
    # Insert watermark
    tw = fitz.TextWriter(page.rect)
    tw.append(point, text, fontname="helv", fontsize=fontsize)
    tw.write_text(page, color=(1, 0, 0), opacity=opacity, rotate=45)
    
    doc.save("/home/claude/watermarked.pdf")
    doc.close()
    print("Created watermarked.pdf")

# ============================================================================
# PART 10: TABLES OF CONTENTS (BOOKMARKS)
# ============================================================================

def toc_operations():
    """Work with table of contents / bookmarks"""
    
    doc = fitz.open()
    
    # Create pages with headings
    for i in range(5):
        page = doc.new_page()
        page.insert_text((50, 50), f"Chapter {i+1}", fontsize=24)
        page.insert_text((50, 100), "Content for this chapter...", fontsize=12)
    
    # Create TOC
    toc = []
    for i in range(5):
        # [level, title, page_number]
        toc.append([1, f"Chapter {i+1}", i+1])
        # Add sub-entries
        toc.append([2, f"Section {i+1}.1", i+1])
        toc.append([2, f"Section {i+1}.2", i+1])
    
    doc.set_toc(toc)
    
    doc.save("/home/claude/with_toc.pdf")
    
    # Read TOC
    doc = fitz.open("/home/claude/with_toc.pdf")
    toc = doc.get_toc()
    print("Table of Contents:")
    for item in toc:
        level, title, page = item
        indent = "  " * (level - 1)
        print(f"{indent}{title} (page {page})")
    
    doc.close()

# ============================================================================
# PART 11: LINKS AND ACTIONS
# ============================================================================

def add_links():
    """Add hyperlinks and internal links"""
    
    doc = fitz.open()
    page1 = doc.new_page()
    page2 = doc.new_page()
    
    # Add text for links
    page1.insert_text((50, 50), "Click here for external link", fontsize=14)
    page1.insert_text((50, 100), "Click here to go to page 2", fontsize=14)
    
    # External link
    rect1 = fitz.Rect(50, 40, 250, 60)
    link = {
        "kind": fitz.LINK_URI,
        "from": rect1,
        "uri": "https://www.example.com"
    }
    page1.insert_link(link)
    
    # Internal link to page 2
    rect2 = fitz.Rect(50, 90, 250, 110)
    link = {
        "kind": fitz.LINK_GOTO,
        "from": rect2,
        "page": 1  # Zero-indexed
    }
    page1.insert_link(link)
    
    # Add some content to page 2
    page2.insert_text((50, 50), "You are now on page 2", fontsize=14)
    
    doc.save("/home/claude/with_links.pdf")
    doc.close()
    print("Created with_links.pdf")

# ============================================================================
# PART 12: FORM FIELDS
# ============================================================================

def create_form():
    """Create PDF form with various field types"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Add form fields
    widget = fitz.Widget()
    
    # Text field
    widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    widget.field_name = "name"
    widget.field_label = "Name:"
    widget.rect = fitz.Rect(50, 50, 300, 70)
    widget.field_value = ""
    widget.text_maxlen = 50
    page.insert_text((50, 45), "Name:", fontsize=12)
    annot = page.add_widget(widget)
    
    # Button (checkbox)
    widget = fitz.Widget()
    widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
    widget.field_name = "agree"
    widget.rect = fitz.Rect(50, 100, 70, 120)
    page.insert_text((75, 115), "I agree to terms", fontsize=12)
    annot = page.add_widget(widget)
    
    # Radio buttons
    for i, option in enumerate(["Option 1", "Option 2", "Option 3"]):
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_RADIOBUTTON
        widget.field_name = "choice"
        widget.rect = fitz.Rect(50, 150 + i*30, 70, 170 + i*30)
        widget.button_caption = option
        page.insert_text((75, 165 + i*30), option, fontsize=12)
        annot = page.add_widget(widget)
    
    # Dropdown (combo box)
    widget = fitz.Widget()
    widget.field_type = fitz.PDF_WIDGET_TYPE_COMBOBOX
    widget.field_name = "country"
    widget.rect = fitz.Rect(50, 270, 250, 290)
    widget.choice_values = ["USA", "UK", "Canada", "Australia"]
    page.insert_text((50, 265), "Country:", fontsize=12)
    annot = page.add_widget(widget)
    
    doc.save("/home/claude/form.pdf")
    doc.close()
    print("Created form.pdf")

# ============================================================================
# PART 13: ENCRYPTION AND SECURITY
# ============================================================================

def encrypt_pdf():
    """Encrypt and password-protect PDF"""
    
    # Create a PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "This is encrypted content", fontsize=14)
    
    # Save with encryption
    user_password = "user123"
    owner_password = "owner456"
    
    doc.save(
        "/home/claude/encrypted.pdf",
        encryption=fitz.PDF_ENCRYPT_AES_256,
        user_pw=user_password,
        owner_pw=owner_password,
        permissions=fitz.PDF_PERM_PRINT | fitz.PDF_PERM_COPY
    )
    doc.close()
    print("Created encrypted.pdf")
    
    # Open encrypted PDF
    doc = fitz.open("/home/claude/encrypted.pdf")
    if doc.needs_pass:
        doc.authenticate(user_password)
    
    # Now you can work with it
    print(f"Document is encrypted: {doc.is_encrypted}")
    doc.close()

# ============================================================================
# PART 14: RENDERING PAGES TO IMAGES
# ============================================================================

def render_to_images():
    """Render PDF pages as images"""
    
    # Create a sample PDF
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "This will become an image", fontsize=20)
    
    # Draw some shapes
    shape = page.new_shape()
    shape.draw_circle(fitz.Point(300, 200), 50)
    shape.finish(color=(1, 0, 0), fill=(1, 1, 0))
    shape.commit()
    
    doc.save("/home/claude/to_render.pdf")
    doc.close()
    
    # Render to image
    doc = fitz.open("/home/claude/to_render.pdf")
    page = doc[0]
    
    # Get pixmap (image) of page
    zoom = 2  # Increase resolution
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat)
    
    # Save as PNG
    pix.save("/home/claude/rendered_page.png")
    
    # Can also get specific area
    rect = fitz.Rect(0, 0, 300, 300)
    pix = page.get_pixmap(clip=rect)
    pix.save("/home/claude/rendered_area.png")
    
    doc.close()
    print("Rendered pages to images")

# ============================================================================
# PART 15: METADATA OPERATIONS
# ============================================================================

def metadata_operations():
    """Read and modify PDF metadata"""
    
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((50, 50), "Document with metadata", fontsize=14)
    
    # Set metadata
    doc.set_metadata({
        "title": "My Document Title",
        "author": "John Doe",
        "subject": "PyMuPDF Tutorial",
        "keywords": "PDF, Python, Tutorial",
        "creator": "PyMuPDF Script",
        "producer": "PyMuPDF",
    })
    
    doc.save("/home/claude/with_metadata.pdf")
    
    # Read metadata
    metadata = doc.metadata
    print("\nMetadata:")
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    doc.close()

# ============================================================================
# PART 16: ADVANCED TEXT EXTRACTION
# ============================================================================

def advanced_text_extraction():
    """Advanced text extraction with position and formatting"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Add various text
    page.insert_text((50, 50), "Header Text", fontsize=24, color=(1, 0, 0))
    page.insert_text((50, 100), "Body text in normal size", fontsize=12)
    page.insert_text((50, 150), "Bold text", fontsize=12, fontname="helv-bold")
    
    doc.save("/home/claude/text_extract.pdf")
    doc.close()
    
    # Extract with details
    doc = fitz.open("/home/claude/text_extract.pdf")
    page = doc[0]
    
    # Get text as dictionary with full details
    text_dict = page.get_text("dict")
    
    print("\nText blocks with details:")
    for block in text_dict["blocks"]:
        if block["type"] == 0:  # Text block
            for line in block["lines"]:
                for span in line["spans"]:
                    print(f"Text: '{span['text']}'")
                    print(f"  Font: {span['font']}")
                    print(f"  Size: {span['size']}")
                    print(f"  Color: {span['color']}")
                    print(f"  Position: ({span['bbox'][0]:.1f}, {span['bbox'][1]:.1f})")
    
    # Get text with bounding boxes
    words = page.get_text("words")
    print("\nWords with positions:")
    for word in words[:5]:  # First 5 words
        x0, y0, x1, y1, text, block_no, line_no, word_no = word
        print(f"'{text}' at ({x0:.1f}, {y0:.1f})")
    
    doc.close()

# ============================================================================
# PART 17: REDACTION
# ============================================================================

def redact_content():
    """Redact (permanently remove) content from PDF"""
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Add sensitive content
    page.insert_text((50, 50), "This is public information", fontsize=14)
    page.insert_text((50, 100), "This is CONFIDENTIAL data: SSN 123-45-6789", fontsize=14)
    page.insert_text((50, 150), "More public information", fontsize=14)
    
    doc.save("/home/claude/to_redact.pdf")
    doc.close()
    
    # Apply redaction
    doc = fitz.open("/home/claude/to_redact.pdf")
    page = doc[0]
    
    # Find text to redact
    areas = page.search_for("CONFIDENTIAL")
    
    # Add redaction annotations
    for rect in areas:
        # Expand rectangle to cover more
        rect.x0 -= 5
        rect.x1 += 200
        annot = page.add_redact_annot(rect, fill=(0, 0, 0))
    
    # Apply redactions (this permanently removes the content)
    page.apply_redactions()
    
    doc.save("/home/claude/redacted.pdf")
    doc.close()
    print("Created redacted.pdf")

# ============================================================================
# PART 18: USEFUL UTILITY FUNCTIONS
# ============================================================================

def utility_functions():
    """Various utility functions"""
    
    # Color conversions
    rgb = fitz.sRGB_to_pdf(128, 64, 192)  # Convert RGB to PDF color
    print(f"RGB to PDF: {rgb}")
    
    # Color to RGB
    pdf_color = (0.5, 0.25, 0.75)
    rgb = fitz.pdf_to_sRGB(pdf_color)
    print(f"PDF to RGB: {rgb}")
    
    # Get text length
    text = "Sample text"
    length = fitz.get_text_length(text, fontname="helv", fontsize=12)
    print(f"Text length: {length}")
    
    # Paper sizes
    a4 = fitz.paper_rect("a4")
    letter = fitz.paper_rect("letter")
    print(f"A4 size: {a4.width} x {a4.height}")
    print(f"Letter size: {letter.width} x {letter.height}")
    
    # Available paper formats:
    # "a0" through "a10", "b0" through "b10"
    # "c0" through "c10", "letter", "legal", "ledger"

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Run all examples"""
    
    print("=" * 60)
    print("PyMuPDF Complete Tutorial")
    print("=" * 60)
    
    print("\n1. Creating simple PDF...")
    create_simple_pdf()
    
    print("\n2. Creating multi-page PDF...")
    create_multipage_pdf()
    
    print("\n3. Drawing shapes...")
    drawing_shapes()
    
    print("\n4. Adding annotations...")
    add_annotations()
    
    print("\n5. Merging PDFs...")
    merge_pdfs()
    
    print("\n6. Splitting PDF...")
    split_pdf()
    
    print("\n7. Adding watermark...")
    add_watermark()
    
    print("\n8. Creating TOC...")
    toc_operations()
    
    print("\n9. Adding links...")
    add_links()
    
    print("\n10. Creating form...")
    create_form()
    
    print("\n11. Encrypting PDF...")
    encrypt_pdf()
    
    print("\n12. Rendering to images...")
    render_to_images()
    
    print("\n13. Working with metadata...")
    metadata_operations()
    
    print("\n14. Advanced text extraction...")
    advanced_text_extraction()
    
    print("\n15. Redacting content...")
    redact_content()
    
    print("\n16. Text formatting...")
    text_formatting_advanced()
    
    print("\n17. Utility functions...")
    utility_functions()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
