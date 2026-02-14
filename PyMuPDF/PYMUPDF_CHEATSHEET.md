# PyMuPDF Quick Reference Cheat Sheet

## Opening & Saving
```python
import fitz

doc = fitz.open("file.pdf")              # Open
doc = fitz.open()                        # Create new
doc.save("output.pdf")                   # Save
doc.close()                              # Close

# Context manager (auto-closes)
with fitz.open("file.pdf") as doc:
    pass
```

## Pages
```python
page = doc[0]                            # Get page
page = doc.new_page()                    # Add page
doc.delete_page(0)                       # Delete page
doc.copy_page(0)                         # Copy page
page.set_rotation(90)                    # Rotate
print(len(doc))                          # Page count
```

## Text - Insert
```python
point = fitz.Point(50, 50)
page.insert_text(point, "Text", fontsize=14, color=(1,0,0))

rect = fitz.Rect(50, 50, 300, 200)
page.insert_textbox(rect, "Text", fontsize=11, align=0)
```

## Text - Extract
```python
text = page.get_text()                   # Simple
text = page.get_text("text")             # Preserve layout
blocks = page.get_text("blocks")         # Blocks
words = page.get_text("words")           # Words
dict_text = page.get_text("dict")        # Detailed

# Search
rects = page.search_for("term")
```

## Images
```python
# Insert
page.insert_image(rect, filename="img.png")

# Extract
for img in page.get_images():
    xref = img[0]
    base = doc.extract_image(xref)
    with open(f"img.{base['ext']}", "wb") as f:
        f.write(base["image"])

# Render page to image
pix = page.get_pixmap()
pix.save("page.png")
```

## Drawing
```python
shape = page.new_shape()

shape.draw_rect(rect)
shape.draw_circle(center, radius)
shape.draw_line(p1, p2)
shape.draw_polyline(points)

shape.finish(color=(1,0,0), fill=(1,1,0), width=2)
shape.commit()
```

## Annotations
```python
# Highlight
rects = page.search_for("text")
page.add_highlight_annot(rects)

# Free text
rect = fitz.Rect(50, 50, 300, 100)
page.add_freetext_annot(rect, "Note", fontsize=12)

# Shapes
page.add_rect_annot(rect)
page.add_circle_annot(rect)

# Ink (freehand)
ink = [[p1, p2, p3], [p4, p5, p6]]
page.add_ink_annot(ink)
```

## Merge & Split
```python
# Merge
result = fitz.open()
for pdf in ["a.pdf", "b.pdf"]:
    with fitz.open(pdf) as src:
        result.insert_pdf(src)
result.save("merged.pdf")

# Split
src = fitz.open("file.pdf")
for i in range(len(src)):
    dst = fitz.open()
    dst.insert_pdf(src, from_page=i, to_page=i)
    dst.save(f"page_{i}.pdf")
```

## Links
```python
# URL
link = {
    "kind": fitz.LINK_URI,
    "from": rect,
    "uri": "https://example.com"
}
page.insert_link(link)

# Internal
link = {
    "kind": fitz.LINK_GOTO,
    "from": rect,
    "page": 5
}
page.insert_link(link)
```

## Forms
```python
widget = fitz.Widget()
widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
widget.field_name = "name"
widget.rect = fitz.Rect(50, 50, 300, 70)
page.add_widget(widget)

# Read
for w in page.widgets():
    print(w.field_name, w.field_value)
```

## Encryption
```python
doc.save(
    "encrypted.pdf",
    encryption=fitz.PDF_ENCRYPT_AES_256,
    user_pw="user",
    owner_pw="owner",
    permissions=fitz.PDF_PERM_PRINT
)

# Open
if doc.needs_pass:
    doc.authenticate("password")
```

## Table of Contents
```python
toc = [
    [1, "Chapter 1", 1],
    [2, "Section 1.1", 1],
    [1, "Chapter 2", 5]
]
doc.set_toc(toc)

# Read
toc = doc.get_toc()
```

## Metadata
```python
meta = doc.metadata
doc.set_metadata({
    "title": "Title",
    "author": "Author"
})
```

## Redaction
```python
rects = page.search_for("secret")
for r in rects:
    page.add_redact_annot(r)
page.apply_redactions()
```

## Watermark
```python
text = "CONFIDENTIAL"
tw = fitz.TextWriter(page.rect)
tw.append(point, text, fontsize=50)
tw.write_text(page, color=(1,0,0), opacity=0.3, rotate=45)
```

## Common Rectangles
```python
rect = fitz.Rect(x0, y0, x1, y1)         # Custom
rect = page.rect                         # Whole page
a4 = fitz.paper_rect("a4")              # A4 size
letter = fitz.paper_rect("letter")      # Letter
```

## Common Points
```python
point = fitz.Point(x, y)
center = page.rect.center
```

## Colors (RGB 0-1)
```python
(0, 0, 0)      # Black
(1, 1, 1)      # White
(1, 0, 0)      # Red
(0, 1, 0)      # Green
(0, 0, 1)      # Blue
(1, 1, 0)      # Yellow
```

## Optimization
```python
doc.save(
    "optimized.pdf",
    garbage=4,        # Remove unused
    deflate=True,     # Compress
    clean=True,       # Clean contents
    linear=True       # Fast web view
)
```

## Error Handling
```python
try:
    doc = fitz.open("file.pdf")
    if doc.needs_pass:
        if not doc.authenticate(pwd):
            raise ValueError("Wrong password")
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'doc' in locals():
        doc.close()
```

## Useful Properties
```python
len(doc)                    # Page count
doc.page_count              # Page count
doc.metadata               # Metadata dict
doc.is_pdf                 # Is PDF?
doc.is_encrypted           # Is encrypted?
page.rect                  # Page rectangle
page.rotation              # Page rotation
page.mediabox              # Media box
```

## Font Names
```python
"helv"      # Helvetica
"helv-bold" # Helvetica Bold
"helv-oblique"  # Helvetica Oblique
"tiro"      # Times Roman
"tiro-bold"
"cour"      # Courier
"zadb"      # ZapfDingbats
"symb"      # Symbol
```

## Widget Types
```python
fitz.PDF_WIDGET_TYPE_TEXT
fitz.PDF_WIDGET_TYPE_CHECKBOX
fitz.PDF_WIDGET_TYPE_RADIOBUTTON
fitz.PDF_WIDGET_TYPE_COMBOBOX
fitz.PDF_WIDGET_TYPE_LISTBOX
fitz.PDF_WIDGET_TYPE_BUTTON
```

## Link Types
```python
fitz.LINK_URI          # URL
fitz.LINK_GOTO         # Internal page
fitz.LINK_LAUNCH       # File
fitz.LINK_NAMED        # Named destination
```

## Permissions
```python
fitz.PDF_PERM_PRINT
fitz.PDF_PERM_MODIFY
fitz.PDF_PERM_COPY
fitz.PDF_PERM_ANNOTATE
fitz.PDF_PERM_FORM
fitz.PDF_PERM_ACCESSIBILITY
fitz.PDF_PERM_ASSEMBLE
fitz.PDF_PERM_PRINT_HQ
```

## Encryption Methods
```python
fitz.PDF_ENCRYPT_NONE
fitz.PDF_ENCRYPT_RC4_40
fitz.PDF_ENCRYPT_RC4_128
fitz.PDF_ENCRYPT_AES_128
fitz.PDF_ENCRYPT_AES_256
```

## Useful Functions
```python
fitz.get_text_length(text, fontname, fontsize)
fitz.paper_rect("a4")
fitz.sRGB_to_pdf(r, g, b)
fitz.pdf_to_sRGB((r, g, b))
```

## Iteration Patterns
```python
# Pages
for page in doc:
    print(page.number)

# Annotations
for annot in page.annots():
    print(annot.type)

# Widgets
for widget in page.widgets():
    print(widget.field_name)

# Links
for link in page.get_links():
    print(link)
```

## Performance Tips
- ✅ Use context managers
- ✅ Close documents when done
- ✅ Reuse objects
- ✅ Batch operations
- ✅ Use garbage collection
- ✅ Cache pixmaps
- ✅ Use appropriate zoom
