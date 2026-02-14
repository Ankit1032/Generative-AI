# PyMuPDF (fitz) Complete End-to-End Guide

## Table of Contents
1. [Introduction & Installation](#introduction)
2. [Opening & Creating Documents](#opening-documents)
3. [Text Operations](#text-operations)
4. [Image Operations](#image-operations)
5. [Drawing & Shapes](#drawing-shapes)
6. [Annotations](#annotations)
7. [Merging & Splitting](#merging-splitting)
8. [Page Manipulation](#page-manipulation)
9. [Watermarks & Overlays](#watermarks)
10. [Table of Contents](#toc)
11. [Links & Actions](#links)
12. [Form Fields](#forms)
13. [Encryption & Security](#encryption)
14. [Rendering to Images](#rendering)
15. [Metadata](#metadata)
16. [Redaction](#redaction)
17. [Advanced Features](#advanced)
18. [Complete Capabilities List](#capabilities)

---

## <a name="introduction"></a>1. Introduction & Installation

### What is PyMuPDF?
PyMuPDF is a Python binding for MuPDF, a lightweight PDF and XPS viewer. It's extremely fast and provides extensive capabilities for PDF manipulation.

### Installation
```bash
pip install pymupdf
```

### Import
```python
import fitz  # PyMuPDF uses 'fitz' as the module name
```

---

## <a name="opening-documents"></a>2. Opening & Creating Documents

### Open Existing PDF
```python
import fitz

# Open from file path
doc = fitz.open("document.pdf")

# Open from bytes
with open("document.pdf", "rb") as f:
    pdf_bytes = f.read()
doc = fitz.open(stream=pdf_bytes, filetype="pdf")

# Always close when done
doc.close()

# Or use context manager
with fitz.open("document.pdf") as doc:
    # Work with document
    pass
```

### Create New PDF
```python
# Create blank document
doc = fitz.open()

# Add a page
page = doc.new_page(width=595, height=842)  # A4 size

# Save
doc.save("new_document.pdf")
doc.close()
```

### Supported Formats
```python
# PyMuPDF can open:
# - PDF
# - XPS
# - EPUB
# - MOBI
# - FB2
# - CBZ
# - SVG
# - Images (PNG, JPG, BMP, etc.)

doc = fitz.open("image.png")
doc = fitz.open("ebook.epub")
```

### Basic Document Info
```python
print(f"Pages: {len(doc)}")
print(f"Page count: {doc.page_count}")
print(f"Metadata: {doc.metadata}")
print(f"Is PDF: {doc.is_pdf}")
print(f"Is encrypted: {doc.is_encrypted}")
print(f"Needs password: {doc.needs_pass}")

# Metadata keys: 'format', 'title', 'author', 'subject', 
# 'keywords', 'creator', 'producer', 'creationDate', 'modDate'
```

---

## <a name="text-operations"></a>3. Text Operations

### Insert Simple Text
```python
page = doc.new_page()

# Basic text insertion
point = fitz.Point(50, 50)  # x, y coordinates
page.insert_text(point, "Hello, World!", fontsize=14)

# With color (RGB, values 0-1)
page.insert_text(point, "Red text", fontsize=14, color=(1, 0, 0))

# With rotation
page.insert_text(point, "Rotated", fontsize=14, rotate=45)

# Different fonts
page.insert_text(point, "Helvetica", fontname="helv", fontsize=12)
page.insert_text(point, "Times", fontname="tiro", fontsize=12)
page.insert_text(point, "Courier", fontname="cour", fontsize=12)
```

### Insert Text in Rectangle (with wrapping)
```python
rect = fitz.Rect(50, 50, 300, 200)  # x0, y0, x1, y1

text = "This is a long text that will wrap within the rectangle. "
text *= 10

# align: 0=left, 1=center, 2=right
page.insert_textbox(
    rect, 
    text, 
    fontsize=11, 
    align=0,
    color=(0, 0, 0)
)
```

### Advanced Text Formatting
```python
# Using TextWriter for more control
tw = fitz.TextWriter(page.rect)

# Append text
point = fitz.Point(50, 50)
tw.append(point, "Formatted text", fontname="helv", fontsize=14)

# Write to page
tw.write_text(page, color=(0, 0, 1), opacity=0.8)

# Multi-line with specific positions
tw = fitz.TextWriter(page.rect)
tw.append((50, 100), "Line 1", fontsize=12)
tw.append((50, 120), "Line 2", fontsize=12)
tw.append((50, 140), "Line 3", fontsize=12)
tw.write_text(page)
```

### Extract Text
```python
page = doc[0]  # First page

# Simple extraction
text = page.get_text()

# Preserve layout
text = page.get_text("text")

# Get text blocks
blocks = page.get_text("blocks")
# Returns: (x0, y0, x1, y1, "text", block_no, block_type)

for block in blocks:
    print(f"Text: {block[4]}")
    print(f"Position: ({block[0]}, {block[1]})")

# Get detailed text dictionary
text_dict = page.get_text("dict")
# Contains: width, height, blocks with font information

for block in text_dict["blocks"]:
    if block["type"] == 0:  # Text block
        for line in block["lines"]:
            for span in line["spans"]:
                print(f"Text: {span['text']}")
                print(f"Font: {span['font']}")
                print(f"Size: {span['size']}")
                print(f"Color: {span['color']}")

# Get words with positions
words = page.get_text("words")
# Returns: (x0, y0, x1, y1, "word", block_no, line_no, word_no)

for word in words:
    x0, y0, x1, y1, text, *_ = word
    print(f"'{text}' at ({x0}, {y0})")

# Get as HTML/XML
html = page.get_text("html")
xml = page.get_text("xml")
xhtml = page.get_text("xhtml")
```

### Search Text
```python
# Search returns list of rectangles where text was found
rectangles = page.search_for("search term")

for rect in rectangles:
    print(f"Found at: {rect}")

# Case-insensitive search
rects = page.search_for("term", flags=fitz.TEXT_PRESERVE_WHITESPACE)

# Search with highlighting
for rect in page.search_for("important"):
    highlight = page.add_highlight_annot(rect)
```

---

## <a name="image-operations"></a>4. Image Operations

### Insert Images
```python
# Insert from file
rect = fitz.Rect(50, 50, 250, 250)
page.insert_image(rect, filename="image.png")

# Insert from bytes
with open("image.jpg", "rb") as f:
    img_bytes = f.read()
page.insert_image(rect, stream=img_bytes)

# Insert with rotation
page.insert_image(rect, filename="image.png", rotate=90)

# Overlay mode
page.insert_image(rect, filename="image.png", overlay=True)

# Keep aspect ratio
page.insert_image(rect, filename="image.png", keep_proportion=True)
```

### Extract Images
```python
# Get all images on page
image_list = page.get_images()

for img_index, img in enumerate(image_list):
    xref = img[0]  # Image reference number
    
    # Extract image
    base_image = doc.extract_image(xref)
    
    image_bytes = base_image["image"]
    image_ext = base_image["ext"]
    image_width = base_image["width"]
    image_height = base_image["height"]
    
    # Save image
    with open(f"image_{img_index}.{image_ext}", "wb") as f:
        f.write(image_bytes)

# Get image rectangles on page
for img in page.get_image_rects(xref):
    print(f"Image rect: {img}")
```

### Convert Page to Image
```python
# Get pixmap (raster image) of page
pix = page.get_pixmap()

# Save as PNG
pix.save("page.png")

# High resolution
zoom = 2.0  # Zoom factor
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)
pix.save("page_high_res.png")

# Specific area
rect = fitz.Rect(0, 0, 300, 300)
pix = page.get_pixmap(clip=rect)

# Different color space
pix = page.get_pixmap(colorspace=fitz.csGRAY)  # Grayscale
pix = page.get_pixmap(colorspace=fitz.csRGB)   # RGB

# As different format
pix.save("page.png", output="png")
pix.save("page.jpg", output="jpeg")
pix.save("page.pnm", output="pnm")
```

---

## <a name="drawing-shapes"></a>5. Drawing & Shapes

### Basic Shapes
```python
# Create shape object
shape = page.new_shape()

# Rectangle
rect = fitz.Rect(50, 50, 200, 150)
shape.draw_rect(rect)
shape.finish(
    color=(1, 0, 0),      # Stroke color (red)
    fill=(1, 1, 0),       # Fill color (yellow)
    width=2                # Line width
)

# Circle
center = fitz.Point(300, 100)
radius = 40
shape.draw_circle(center, radius)
shape.finish(color=(0, 0, 1), fill=(0.8, 0.8, 1))

# Oval
rect = fitz.Rect(400, 50, 550, 150)
shape.draw_oval(rect)
shape.finish(color=(0, 1, 0), fill=(0.8, 1, 0.8))

# Line
p1 = fitz.Point(50, 200)
p2 = fitz.Point(200, 250)
shape.draw_line(p1, p2)
shape.finish(color=(1, 0, 1), width=3)

# Polyline (connected lines)
points = [
    fitz.Point(50, 300),
    fitz.Point(100, 320),
    fitz.Point(150, 300),
    fitz.Point(200, 340)
]
shape.draw_polyline(points)
shape.finish(color=(0.5, 0.5, 0.5), width=2)

# Polygon (closed polyline with fill)
points = [
    fitz.Point(250, 300),
    fitz.Point(300, 280),
    fitz.Point(350, 300),
    fitz.Point(325, 350)
]
shape.draw_polygon(points)
shape.finish(color=(0, 0.5, 0.5), fill=(0.8, 1, 1))

# Bezier curve
p1 = fitz.Point(50, 400)
p2 = fitz.Point(150, 350)  # Control point 1
p3 = fitz.Point(250, 450)  # Control point 2
p4 = fitz.Point(350, 400)
shape.draw_bezier(p1, p2, p3, p4)
shape.finish(color=(0.5, 0, 0.5), width=2)

# Sector (pie slice)
center = fitz.Point(475, 400)
point_on_circle = center + (50, 0)
angle = 90
shape.draw_sector(center, point_on_circle, angle)
shape.finish(color=(1, 0.5, 0), fill=(1, 1, 0.8))

# Squiggle (wavy line)
shape.draw_squiggle(p1, p2)
shape.finish(color=(1, 0, 0), width=1)

# Commit all drawings
shape.commit()
```

### Advanced Drawing Options
```python
shape = page.new_shape()

# Dashed lines
shape.draw_line(p1, p2)
shape.finish(
    color=(0, 0, 0),
    width=2,
    dashes="[3 2]"  # 3 units on, 2 units off
)

# Rounded rectangles
rect = fitz.Rect(50, 50, 200, 150)
shape.draw_rect(rect)
shape.finish(
    color=(0, 0, 1),
    width=2,
    roundCap=True,  # Round line caps
    roundJoin=True  # Round line joins
)

# Different line cap styles
# 0 = butt, 1 = round, 2 = square
shape.draw_line(p1, p2)
shape.finish(color=(0, 0, 0), width=10, lineCap=1)

# Different line join styles
# 0 = miter, 1 = round, 2 = bevel
shape.draw_polyline(points)
shape.finish(color=(0, 0, 0), width=10, lineJoin=1)

shape.commit()
```

---

## <a name="annotations"></a>6. Annotations

### Text Annotations
```python
# Simple note icon
point = fitz.Point(50, 50)
annot = page.add_text_annot(point, "This is a note")

# Set icon type
annot.set_info(title="Author", content="Note content")
annot.update()

# Free text (text box)
rect = fitz.Rect(50, 100, 300, 150)
annot = page.add_freetext_annot(
    rect,
    "This is free text",
    fontsize=12,
    text_color=(0, 0, 1),
    fill_color=(1, 1, 0.8)
)
```

### Markup Annotations
```python
# Highlight
text_rects = page.search_for("highlight this")
if text_rects:
    annot = page.add_highlight_annot(text_rects)
    annot.set_colors(stroke=(1, 1, 0))  # Yellow
    annot.update()

# Underline
text_rects = page.search_for("underline this")
if text_rects:
    annot = page.add_underline_annot(text_rects)
    annot.set_colors(stroke=(0, 0, 1))  # Blue
    annot.update()

# Strikeout
text_rects = page.search_for("strike this")
if text_rects:
    annot = page.add_strikeout_annot(text_rects)
    annot.set_colors(stroke=(1, 0, 0))  # Red
    annot.update()

# Squiggly underline
text_rects = page.search_for("squiggly")
if text_rects:
    annot = page.add_squiggly_annot(text_rects)
    annot.set_colors(stroke=(0, 1, 0))  # Green
    annot.update()
```

### Shape Annotations
```python
# Rectangle annotation
rect = fitz.Rect(50, 200, 200, 250)
annot = page.add_rect_annot(rect)
annot.set_colors(stroke=(1, 0, 0), fill=(1, 1, 0.8))
annot.set_opacity(0.5)
annot.set_border(width=2, dashes=[3, 2])
annot.update()

# Circle annotation
rect = fitz.Rect(250, 200, 350, 300)
annot = page.add_circle_annot(rect)
annot.set_colors(stroke=(0, 0, 1))
annot.update()

# Polygon annotation
points = [
    fitz.Point(400, 200),
    fitz.Point(450, 220),
    fitz.Point(500, 200),
    fitz.Point(475, 250)
]
annot = page.add_polygon_annot(points)
annot.set_colors(stroke=(0, 1, 0), fill=(0.8, 1, 0.8))
annot.update()

# Polyline annotation
annot = page.add_polyline_annot(points)
annot.set_colors(stroke=(1, 0, 1))
annot.update()

# Line annotation
p1 = fitz.Point(50, 300)
p2 = fitz.Point(200, 350)
annot = page.add_line_annot(p1, p2)
annot.set_colors(stroke=(0.5, 0.5, 0.5))
annot.set_border(width=3)
annot.update()
```

### Ink Annotation (Freehand Drawing)
```python
# Multiple strokes
ink_list = [
    [fitz.Point(50, 400), fitz.Point(100, 410), fitz.Point(150, 400)],
    [fitz.Point(50, 420), fitz.Point(100, 430), fitz.Point(150, 420)]
]
annot = page.add_ink_annot(ink_list)
annot.set_colors(stroke=(1, 0, 0))
annot.set_border(width=2)
annot.update()
```

### Stamp Annotations
```python
rect = fitz.Rect(50, 450, 150, 500)

# Built-in stamps:
# 0=Approved, 1=AsIs, 2=Confidential, 3=Departmental,
# 4=Draft, 5=Experimental, 6=Expired, 7=Final,
# 8=ForComment, 9=ForPublicRelease, 10=NotApproved,
# 11=NotForPublicRelease, 12=Sold, 13=TopSecret
annot = page.add_stamp_annot(rect, stamp=0)  # Approved
annot.update()
```

### File Attachment
```python
point = fitz.Point(50, 550)
with open("attachment.txt", "rb") as f:
    file_content = f.read()

annot = page.add_file_annot(
    point,
    file_content,
    filename="attachment.txt",
    desc="Attached file"
)
```

### Working with Annotations
```python
# Get all annotations on page
annots = page.annots()

for annot in annots:
    print(f"Type: {annot.type}")
    print(f"Rect: {annot.rect}")
    print(f"Info: {annot.info}")
    
    # Modify annotation
    annot.set_opacity(0.7)
    annot.update()
    
    # Delete annotation
    # page.delete_annot(annot)

# Get specific annotation by index
annot = page.first_annot  # First annotation
annot = annot.next  # Next annotation
```

---

## <a name="merging-splitting"></a>7. Merging & Splitting

### Merge PDFs
```python
# Simple merge
result = fitz.open()

for pdf_path in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    with fitz.open(pdf_path) as doc:
        result.insert_pdf(doc)

result.save("merged.pdf")
result.close()

# Merge specific pages
result = fitz.open()
source = fitz.open("source.pdf")

# Insert pages 0, 2, 4
result.insert_pdf(source, from_page=0, to_page=0)
result.insert_pdf(source, from_page=2, to_page=2)
result.insert_pdf(source, from_page=4, to_page=4)

# Insert page range
result.insert_pdf(source, from_page=10, to_page=20)

# Insert at specific position
result.insert_pdf(source, from_page=0, to_page=5, start_at=3)

source.close()
result.save("partial_merge.pdf")
result.close()
```

### Split PDF
```python
source = fitz.open("source.pdf")

# Split into individual pages
for page_num in range(len(source)):
    new_doc = fitz.open()
    new_doc.insert_pdf(source, from_page=page_num, to_page=page_num)
    new_doc.save(f"page_{page_num + 1}.pdf")
    new_doc.close()

# Split into chunks
chunk_size = 5
for i in range(0, len(source), chunk_size):
    new_doc = fitz.open()
    end = min(i + chunk_size - 1, len(source) - 1)
    new_doc.insert_pdf(source, from_page=i, to_page=end)
    new_doc.save(f"chunk_{i // chunk_size + 1}.pdf")
    new_doc.close()

source.close()
```

---

## <a name="page-manipulation"></a>8. Page Manipulation

### Add, Delete, Move Pages
```python
doc = fitz.open()

# Add new page
page = doc.new_page()  # Default A4
page = doc.new_page(width=612, height=792)  # Custom size
page = doc.new_page(pno=0)  # Insert at beginning
page = doc.new_page(pno=1)  # Insert at position 1

# Delete page
doc.delete_page(0)  # Delete first page
doc.delete_pages(0, 2)  # Delete pages 0-2
doc.delete_pages([0, 2, 4])  # Delete specific pages

# Copy page
doc.copy_page(0)  # Copy to end
doc.copy_page(0, to=5)  # Copy to specific position

# Move page
doc.move_page(0, 5)  # Move page 0 to position 5

# Select pages (keep only specified pages)
doc.select([0, 2, 4, 6])  # Keep only these pages
```

### Page Properties
```python
page = doc[0]

# Get page size
rect = page.rect
print(f"Width: {rect.width}, Height: {rect.height}")

# Rotate page (90, 180, 270 degrees)
page.set_rotation(90)

# Get rotation
rotation = page.rotation

# Cropbox (visible area)
page.set_cropbox(fitz.Rect(50, 50, 500, 750))

# Mediabox (physical page size)
mediabox = page.mediabox

# Transformation matrix
page.set_rotation(45)  # Will use matrix
```

### Page Sizes (Standard Formats)
```python
# Get standard paper sizes
a4 = fitz.paper_rect("a4")  # 595 x 842
a3 = fitz.paper_rect("a3")
letter = fitz.paper_rect("letter")  # 612 x 792
legal = fitz.paper_rect("legal")

# Create page with standard size
page = doc.new_page(width=a4.width, height=a4.height)

# Available: a0-a10, b0-b10, c0-c10, letter, legal, ledger
```

---

## <a name="watermarks"></a>9. Watermarks & Overlays

### Text Watermark
```python
page = doc[0]

# Simple text watermark
text = "CONFIDENTIAL"
fontsize = 50

# Calculate center position
text_width = fitz.get_text_length(text, fontname="helv", fontsize=fontsize)
center_x = (page.rect.width - text_width) / 2
center_y = page.rect.height / 2

point = fitz.Point(center_x, center_y)

# Insert with transparency
tw = fitz.TextWriter(page.rect)
tw.append(point, text, fontname="helv", fontsize=fontsize)
tw.write_text(
    page,
    color=(1, 0, 0),
    opacity=0.3,
    rotate=45
)

# Or using insert_text with overlay
page.insert_text(
    point,
    text,
    fontsize=fontsize,
    color=(1, 0, 0),
    rotate=45,
    overlay=False  # False = behind content, True = over content
)
```

### Image Watermark
```python
# Insert image as watermark
rect = fitz.Rect(0, 0, page.rect.width, page.rect.height)
page.insert_image(
    rect,
    filename="watermark.png",
    overlay=False,  # Behind content
    keep_proportion=True,
    rotate=0
)
```

### Page Overlay
```python
# Overlay one page onto another
source = fitz.open("watermark.pdf")
watermark_page = source[0]

# Show watermark on target page
page.show_pdf_page(
    page.rect,
    source,
    0,  # Page number
    keep_proportion=True,
    overlay=True
)

source.close()
```

---

## <a name="toc"></a>10. Table of Contents (Bookmarks)

### Create TOC
```python
doc = fitz.open()

# Add pages
for i in range(10):
    page = doc.new_page()
    page.insert_text((50, 50), f"Chapter {i+1}", fontsize=24)

# Create table of contents
toc = [
    [1, "Chapter 1", 1],        # [level, title, page]
    [2, "Section 1.1", 1],      # Level 2 = subsection
    [2, "Section 1.2", 2],
    [1, "Chapter 2", 3],
    [2, "Section 2.1", 3],
    [2, "Section 2.2", 4],
    [3, "Subsection 2.2.1", 4], # Level 3 = sub-subsection
    [1, "Chapter 3", 5],
]

doc.set_toc(toc)
doc.save("with_toc.pdf")
```

### Read TOC
```python
doc = fitz.open("with_toc.pdf")
toc = doc.get_toc()

for entry in toc:
    level, title, page = entry
    indent = "  " * (level - 1)
    print(f"{indent}{title} -> page {page}")

# Simple: returns [[level, title, page], ...]
```

### Modify TOC
```python
toc = doc.get_toc()

# Add new entry
toc.append([1, "Appendix", 15])

# Modify existing
toc[0][1] = "New Chapter Title"

# Remove entry
toc.pop(3)

# Update TOC
doc.set_toc(toc)
```

---

## <a name="links"></a>11. Links & Actions

### External Links (URLs)
```python
page = doc[0]

# Add text
page.insert_text((50, 50), "Click here for website", fontsize=14)

# Create link rectangle
rect = fitz.Rect(50, 40, 200, 60)

# Add link
link = {
    "kind": fitz.LINK_URI,
    "from": rect,
    "uri": "https://www.example.com"
}
page.insert_link(link)
```

### Internal Links (Page Navigation)
```python
# Link to another page
rect = fitz.Rect(50, 100, 200, 120)
link = {
    "kind": fitz.LINK_GOTO,
    "from": rect,
    "page": 5,  # Target page (0-indexed)
    "to": fitz.Point(0, 0)  # Position on target page
}
page.insert_link(link)

# Link with zoom
link = {
    "kind": fitz.LINK_GOTO,
    "from": rect,
    "page": 5,
    "zoom": 2.0  # Zoom level
}
page.insert_link(link)
```

### Named Destinations
```python
# Create named destination
link = {
    "kind": fitz.LINK_NAMED,
    "from": rect,
    "name": "destination_name"
}
page.insert_link(link)
```

### File Links
```python
# Link to another file
link = {
    "kind": fitz.LINK_LAUNCH,
    "from": rect,
    "file": "other_document.pdf"
}
page.insert_link(link)
```

### Get Existing Links
```python
links = page.get_links()

for link in links:
    print(f"Type: {link['kind']}")
    print(f"Rect: {link['from']}")
    if link['kind'] == fitz.LINK_URI:
        print(f"URL: {link['uri']}")
    elif link['kind'] == fitz.LINK_GOTO:
        print(f"Page: {link['page']}")
```

### Delete Links
```python
# Delete specific link by id
page.delete_link(link)

# Delete all links
for link in page.get_links():
    page.delete_link(link)
```

---

## <a name="forms"></a>12. Form Fields

### Create Form Fields
```python
page = doc[0]

# Text field
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
widget.field_name = "name"
widget.field_label = "Full Name:"
widget.rect = fitz.Rect(50, 50, 300, 70)
widget.field_value = ""
widget.text_maxlen = 50
widget.text_fontsize = 12
annot = page.add_widget(widget)

# Multiline text
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
widget.field_name = "comments"
widget.rect = fitz.Rect(50, 100, 300, 200)
widget.field_flags = fitz.PDF_FIELD_IS_MULTILINE
annot = page.add_widget(widget)

# Checkbox
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
widget.field_name = "agree"
widget.rect = fitz.Rect(50, 220, 70, 240)
widget.field_value = False
annot = page.add_widget(widget)

# Radio button group
for i, option in enumerate(["Option 1", "Option 2", "Option 3"]):
    widget = fitz.Widget()
    widget.field_type = fitz.PDF_WIDGET_TYPE_RADIOBUTTON
    widget.field_name = "choice"  # Same name for group
    widget.rect = fitz.Rect(50, 260 + i*30, 70, 280 + i*30)
    widget.button_caption = option
    annot = page.add_widget(widget)

# Dropdown/Combobox
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_COMBOBOX
widget.field_name = "country"
widget.rect = fitz.Rect(50, 400, 250, 420)
widget.choice_values = ["USA", "UK", "Canada", "Australia"]
widget.field_value = "USA"  # Default
annot = page.add_widget(widget)

# List box
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_LISTBOX
widget.field_name = "colors"
widget.rect = fitz.Rect(50, 450, 250, 550)
widget.choice_values = ["Red", "Green", "Blue", "Yellow"]
annot = page.add_widget(widget)

# Button
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_BUTTON
widget.field_name = "submit"
widget.rect = fitz.Rect(50, 570, 150, 600)
widget.button_caption = "Submit"
annot = page.add_widget(widget)
```

### Read Form Field Values
```python
# Get all widgets (form fields) on page
for widget in page.widgets():
    print(f"Field name: {widget.field_name}")
    print(f"Field type: {widget.field_type}")
    print(f"Field value: {widget.field_value}")
    print(f"Rect: {widget.rect}")

# Get specific field
for widget in page.widgets():
    if widget.field_name == "name":
        value = widget.field_value
```

### Modify Form Fields
```python
for widget in page.widgets():
    if widget.field_name == "name":
        widget.field_value = "John Doe"
        widget.update()
    
    if widget.field_name == "agree":
        widget.field_value = True
        widget.update()
```

---

## <a name="encryption"></a>13. Encryption & Security

### Encrypt PDF
```python
doc = fitz.open("document.pdf")

# Save with encryption
doc.save(
    "encrypted.pdf",
    encryption=fitz.PDF_ENCRYPT_AES_256,  # AES-256 encryption
    user_pw="user_password",               # User password
    owner_pw="owner_password",             # Owner password
    permissions=fitz.PDF_PERM_PRINT | fitz.PDF_PERM_COPY
)

# Encryption methods:
# fitz.PDF_ENCRYPT_NONE
# fitz.PDF_ENCRYPT_RC4_40
# fitz.PDF_ENCRYPT_RC4_128
# fitz.PDF_ENCRYPT_AES_128
# fitz.PDF_ENCRYPT_AES_256

# Permissions:
# fitz.PDF_PERM_PRINT
# fitz.PDF_PERM_MODIFY
# fitz.PDF_PERM_COPY
# fitz.PDF_PERM_ANNOTATE
# fitz.PDF_PERM_FORM
# fitz.PDF_PERM_ACCESSIBILITY
# fitz.PDF_PERM_ASSEMBLE
# fitz.PDF_PERM_PRINT_HQ
```

### Open Encrypted PDF
```python
doc = fitz.open("encrypted.pdf")

if doc.needs_pass:
    success = doc.authenticate("user_password")
    if success:
        print("Authentication successful")
    else:
        print("Wrong password")

# Check encryption
print(f"Is encrypted: {doc.is_encrypted}")
print(f"Encryption method: {doc.encryption_method}")
```

### Remove Encryption
```python
doc = fitz.open("encrypted.pdf")
doc.authenticate("owner_password")

# Save without encryption
doc.save("decrypted.pdf", encryption=fitz.PDF_ENCRYPT_NONE)
```

---

## <a name="rendering"></a>14. Rendering to Images

### Render Page to PNG
```python
page = doc[0]

# Basic rendering
pix = page.get_pixmap()
pix.save("page.png")

# High resolution
zoom = 2.0
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)
pix.save("page_hires.png")

# Different DPI
dpi = 300
zoom = dpi / 72  # 72 is default DPI
mat = fitz.Matrix(zoom, zoom)
pix = page.get_pixmap(matrix=mat)
```

### Render Specific Area
```python
# Clip to rectangle
rect = fitz.Rect(0, 0, 300, 400)
pix = page.get_pixmap(clip=rect)
pix.save("area.png")
```

### Color Spaces
```python
# Grayscale
pix = page.get_pixmap(colorspace=fitz.csGRAY)

# RGB (default)
pix = page.get_pixmap(colorspace=fitz.csRGB)

# CMYK
pix = page.get_pixmap(colorspace=fitz.csCMYK)
```

### Transparent Background
```python
pix = page.get_pixmap(alpha=True)
```

### Save in Different Formats
```python
# PNG
pix.save("page.png", output="png")

# JPEG (lossy)
pix.save("page.jpg", output="jpeg", jpg_quality=95)

# PNM
pix.save("page.pnm", output="pnm")

# PAM
pix.save("page.pam", output="pam")

# PSD (Adobe)
pix.save("page.psd", output="psd")

# Get as bytes
png_bytes = pix.tobytes("png")
jpg_bytes = pix.tobytes("jpeg")
```

### Pixmap Properties
```python
print(f"Width: {pix.width}")
print(f"Height: {pix.height}")
print(f"Stride: {pix.stride}")
print(f"Size: {len(pix.samples)}")
print(f"Color space: {pix.colorspace}")
print(f"Has alpha: {pix.alpha}")
```

---

## <a name="metadata"></a>15. Metadata

### Read Metadata
```python
doc = fitz.open("document.pdf")
metadata = doc.metadata

print(f"Title: {metadata['title']}")
print(f"Author: {metadata['author']}")
print(f"Subject: {metadata['subject']}")
print(f"Keywords: {metadata['keywords']}")
print(f"Creator: {metadata['creator']}")
print(f"Producer: {metadata['producer']}")
print(f"Creation Date: {metadata['creationDate']}")
print(f"Modification Date: {metadata['modDate']}")
print(f"Format: {metadata['format']}")
print(f"Encryption: {metadata['encryption']}")
```

### Set Metadata
```python
doc.set_metadata({
    "title": "My Document",
    "author": "John Doe",
    "subject": "PyMuPDF Tutorial",
    "keywords": "PDF, Python, Tutorial",
    "creator": "Python Script",
    "producer": "PyMuPDF 1.23.0"
})

doc.save("with_metadata.pdf")
```

### Clear Metadata
```python
doc.set_metadata({})
```

---

## <a name="redaction"></a>16. Redaction

### Text Redaction
```python
page = doc[0]

# Find text to redact
areas = page.search_for("confidential")

# Add redaction annotations
for rect in areas:
    # Optionally expand rectangle
    rect.x1 += 50
    annot = page.add_redact_annot(rect)

# Apply redactions (permanently removes content)
page.apply_redactions()

doc.save("redacted.pdf")
```

### Area Redaction
```python
# Redact specific area
rect = fitz.Rect(100, 100, 300, 200)
annot = page.add_redact_annot(rect, fill=(0, 0, 0))  # Black fill
page.apply_redactions()
```

### Redaction with Overlay Text
```python
rect = fitz.Rect(100, 100, 300, 150)
annot = page.add_redact_annot(
    rect,
    text="REDACTED",
    fill=(0, 0, 0),
    text_color=(1, 1, 1)
)
page.apply_redactions()
```

### Find and Redact Pattern
```python
import re

# Get all text
text = page.get_text("dict")

# Pattern for SSN, phone, email, etc.
patterns = [
    r'\d{3}-\d{2}-\d{4}',  # SSN
    r'\d{3}-\d{3}-\d{4}',  # Phone
    r'[\w\.-]+@[\w\.-]+',  # Email
]

for block in text["blocks"]:
    if block["type"] == 0:
        for line in block["lines"]:
            for span in line["spans"]:
                for pattern in patterns:
                    if re.search(pattern, span["text"]):
                        bbox = span["bbox"]
                        rect = fitz.Rect(bbox)
                        page.add_redact_annot(rect)

page.apply_redactions()
```

---

## <a name="advanced"></a>17. Advanced Features

### Document Outline
```python
# Get outline (similar to TOC but different structure)
outline = doc.outline

# Process outline
def print_outline(outline, indent=0):
    for item in outline:
        print("  " * indent + item.title)
        if item.down:
            print_outline(item.down, indent + 1)
```

### Embedded Files
```python
# Embed file in PDF
with open("file.txt", "rb") as f:
    file_data = f.read()

doc.embfile_add(
    "attached_file.txt",
    file_data,
    filename="attached_file.txt",
    desc="Attached document"
)

# List embedded files
for name in doc.embfile_names():
    print(f"Embedded: {name}")

# Extract embedded file
file_data = doc.embfile_get(name)
```

### Layers (Optional Content Groups)
```python
# Get layers
layers = doc.layer_ui_configs()

for layer in layers:
    print(f"Layer: {layer['text']}")

# Set layer visibility
doc.set_layer(layer_name, on=True)
```

### JavaScript
```python
# Add JavaScript to document
js_code = """
app.alert("Hello from PDF!");
"""
doc.set_javascript("myScript", js_code)

# Get JavaScript
js = doc.get_javascript("myScript")

# Remove JavaScript
doc.del_javascript("myScript")
```

### Page Labels
```python
# Set page labels (different from page numbers)
labels = [
    {"startpage": 0, "prefix": "Cover-", "style": "r"},  # Roman
    {"startpage": 1, "prefix": "Intro-", "style": "a"},  # Alpha
    {"startpage": 5, "prefix": "Ch", "style": "D"}       # Decimal
]

doc.set_page_labels(labels)

# Get page label
label = doc.get_page_label(3)
```

### Permissions
```python
# Check permissions
print(f"Can print: {doc.permissions & fitz.PDF_PERM_PRINT}")
print(f"Can modify: {doc.permissions & fitz.PDF_PERM_MODIFY}")
print(f"Can copy: {doc.permissions & fitz.PDF_PERM_COPY}")
```

### XML Metadata (XMP)
```python
# Get XMP metadata
xmp = doc.xref_xml_metadata()

if xmp:
    xml_content = doc.xref_stream(xmp)
    print(xml_content.decode())

# Set XMP metadata
doc.set_xml_metadata(xml_string)
```

### Optimize PDF
```python
# Garbage collection (remove unused objects)
doc.save("optimized.pdf", garbage=4, deflate=True)

# Parameters:
# garbage: 0=none, 1=remove unused, 2=also PDFs, 3=also images, 4=all
# deflate: compress streams
# clean: clean up page contents
# linear: linearize (fast web view)
```

### PDF/A Conversion
```python
# Convert to PDF/A
oc = doc.convertToPDF()  # Get PDF bytes
doc_pdfa = fitz.open("pdf", oc)
doc_pdfa.save("pdfa.pdf")
```

---

## <a name="capabilities"></a>18. Complete Capabilities List

### What PyMuPDF Can Do

#### Document Operations
- ✅ Open PDF, XPS, EPUB, MOBI, FB2, CBZ, SVG, images
- ✅ Create new PDFs from scratch
- ✅ Save, save as, save incrementally
- ✅ Merge multiple PDFs
- ✅ Split PDFs
- ✅ Convert formats (PDF, XPS, etc.)
- ✅ Linearize (fast web view)
- ✅ Optimize and compress
- ✅ Encrypt and decrypt
- ✅ Set permissions

#### Page Operations
- ✅ Add, delete, copy, move pages
- ✅ Rotate pages
- ✅ Set page sizes and crops
- ✅ Extract pages to new PDFs
- ✅ Reorder pages

#### Text Operations
- ✅ Extract text (simple, blocks, words, characters)
- ✅ Extract text with formatting info
- ✅ Search text
- ✅ Insert text
- ✅ Format text (fonts, sizes, colors)
- ✅ Rotate text
- ✅ Text in rectangles with wrapping
- ✅ Get text positions and bounding boxes

#### Image Operations
- ✅ Insert images (PNG, JPG, BMP, etc.)
- ✅ Extract images
- ✅ Render pages to images
- ✅ Control resolution and quality
- ✅ Different color spaces
- ✅ Transparent rendering

#### Drawing & Shapes
- ✅ Draw lines, rectangles, circles
- ✅ Draw polygons, polylines
- ✅ Bezier curves
- ✅ Custom shapes
- ✅ Fill and stroke
- ✅ Line styles (dashed, width, caps, joins)

#### Annotations
- ✅ Text annotations
- ✅ Free text
- ✅ Highlight, underline, strikeout
- ✅ Shapes (rect, circle, polygon)
- ✅ Ink (freehand)
- ✅ Stamps
- ✅ File attachments
- ✅ Modify and delete annotations

#### Forms
- ✅ Create form fields (text, checkbox, radio, dropdown, etc.)
- ✅ Read form values
- ✅ Fill forms
- ✅ Flatten forms

#### Links & Navigation
- ✅ Add external links (URLs)
- ✅ Add internal links (pages)
- ✅ Named destinations
- ✅ File links
- ✅ Table of contents/bookmarks

#### Security
- ✅ Password protection (user/owner)
- ✅ Encryption (40-bit to AES-256)
- ✅ Set permissions
- ✅ Redaction

#### Metadata
- ✅ Read/write metadata
- ✅ XMP metadata
- ✅ Document properties

#### Advanced Features
- ✅ Embedded files
- ✅ JavaScript
- ✅ Layers (OCG)
- ✅ Page labels
- ✅ Digital signatures (read)
- ✅ PDF/A conversion
- ✅ Incremental saves

#### Performance
- ✅ Very fast processing
- ✅ Low memory footprint
- ✅ Efficient for large documents
- ✅ Multi-threading support

### Common Use Cases

1. **PDF Generation**: Create reports, invoices, certificates
2. **PDF Manipulation**: Merge, split, rotate, reorder
3. **Text Extraction**: Data mining, indexing, archiving
4. **Form Handling**: Fill, create, process forms
5. **Annotation**: Review, markup, commenting
6. **Watermarking**: Branding, security
7. **Redaction**: Privacy, compliance
8. **Conversion**: PDF to images, images to PDF
9. **Security**: Encryption, permissions
10. **Automation**: Batch processing, workflows

### Performance Tips

1. **Reuse document objects** instead of reopening
2. **Use context managers** for automatic cleanup
3. **Batch operations** when possible
4. **Use appropriate zoom** for rendering
5. **Enable garbage collection** when saving
6. **Use incremental saves** for large docs
7. **Close documents** when done
8. **Use pixmap caching** for repeated renders

### Common Patterns

```python
# Context manager pattern
with fitz.open("doc.pdf") as doc:
    for page in doc:
        # Process page
        pass

# Batch processing
for pdf_file in pdf_files:
    with fitz.open(pdf_file) as doc:
        # Process document
        doc.save(f"processed_{pdf_file}")

# Error handling
try:
    doc = fitz.open("file.pdf")
    if doc.needs_pass:
        if not doc.authenticate(password):
            raise ValueError("Wrong password")
    # Process
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'doc' in locals():
        doc.close()
```

---

## Installation & Version Info

```bash
# Install
pip install pymupdf

# Install with extras
pip install "pymupdf[full]"

# Check version
python -c "import fitz; print(fitz.__version__)"

# Get detailed version info
python -c "import fitz; print(fitz.VersionBind)"
```

## Documentation & Resources

- Official Docs: https://pymupdf.readthedocs.io/
- GitHub: https://github.com/pymupdf/PyMuPDF
- Examples: https://github.com/pymupdf/PyMuPDF-Utilities
- Discord: https://discord.gg/TSpYGBW4eq

---

This guide covers the essential and advanced features of PyMuPDF. The library is incredibly powerful and continues to evolve with new features regularly!
