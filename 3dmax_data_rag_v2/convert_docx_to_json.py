import zipfile
import os
import shutil
import imghdr
import tempfile
import re
from lxml import etree


def extract_and_replace_images(input_docx, output_docx, output_dir="media"):
    """
    Extract images from docx and replace them with their filenames by
    directly modifying the document's XML structure.

    Args:
        input_docx (str): Path to the input docx file
        output_docx (str): Path to save the modified docx file
        output_dir (str): Directory to save extracted media files
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory: {output_dir}")

    # Create a temporary directory for working with the docx
    temp_dir = tempfile.mkdtemp()

    try:
        # Extract all files from the docx (which is a zip file)
        with zipfile.ZipFile(input_docx, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find and extract media files
        media_dir = os.path.join(temp_dir, 'word', 'media')
        if os.path.exists(media_dir):
            media_files = [f for f in os.listdir(media_dir) if os.path.isfile(os.path.join(media_dir, f))]
            print(f"Found {len(media_files)} media files")

            # Extract and rename media files
            extracted_files = {}  # Map original filename to new filename
            for i, filename in enumerate(media_files):
                # Determine the file type
                file_path = os.path.join(media_dir, filename)
                extension = os.path.splitext(filename)[1].lower()

                if not extension or extension == '.bin':
                    # Try to detect file type
                    img_type = imghdr.what(file_path)
                    if img_type:
                        extension = f'.{img_type}'
                    else:
                        # Check if it's a GIF
                        with open(file_path, 'rb') as f:
                            if f.read(3) == b'GIF':
                                extension = '.gif'
                            else:
                                extension = '.bin'

                # Create new filename
                new_filename = f"3dmax_{i + 1:04d}{extension}"
                new_path = os.path.join(output_dir, new_filename)

                # Copy file
                shutil.copy(file_path, new_path)

                # Store mapping
                extracted_files[filename] = new_filename
                print(f"Extracted: {filename} -> {new_filename}")
        else:
            print("No media directory found!")
            return

        # Get the document.xml path
        document_xml_path = os.path.join(temp_dir, 'word', 'document.xml')

        # Modify document.xml to replace images with text
        if os.path.exists(document_xml_path):
            # Parse the XML
            parser = etree.XMLParser(recover=True)
            tree = etree.parse(document_xml_path, parser)
            root = tree.getroot()

            # Define namespaces
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
                'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
                'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
                'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
                'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'
            }

            # Find all drawing elements (which contain images)
            drawings = root.xpath('//w:drawing', namespaces=namespaces)
            print(f"Found {len(drawings)} drawing elements")

            # Process each drawing
            image_counter = 0
            for drawing in drawings:
                try:
                    # Find the blip element that references the image
                    blips = drawing.xpath('.//a:blip', namespaces=namespaces)
                    if not blips:
                        continue

                    # Get the relationship ID for the image
                    for ns in ['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}embed',
                               '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}link']:
                        if ns in blips[0].attrib:
                            rel_id = blips[0].attrib[ns]
                            break
                    else:
                        continue

                    # Get the parent paragraph
                    paragraph = drawing.getparent()
                    while paragraph is not None and paragraph.tag != '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p':
                        paragraph = paragraph.getparent()

                    if paragraph is None:
                        continue

                    # Create new run with text
                    if image_counter < len(extracted_files):
                        image_filename = list(extracted_files.values())[image_counter]
                    else:
                        image_filename = f"3dmax_unknown_{image_counter + 1:04d}"

                    # Create a new run element with the filename text
                    new_run = etree.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
                    text_element = etree.SubElement(new_run,
                                                    '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
                    text_element.text = image_filename

                    # Find the run containing the drawing
                    run = drawing.getparent()
                    while run is not None and run.tag != '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r':
                        run = run.getparent()

                    if run is not None and run.getparent() is not None:
                        # Replace the run containing the drawing with our new text run
                        run.getparent().replace(run, new_run)
                        print(f"Replaced image {image_counter + 1} with text: {image_filename}")

                    image_counter += 1

                except Exception as e:
                    print(f"Error processing drawing: {str(e)}")

            # Save the modified XML
            tree.write(document_xml_path, encoding='UTF-8', xml_declaration=True)
            print(f"Modified document.xml with {image_counter} replacements")

            # Create a new docx file from the modified content
            with zipfile.ZipFile(output_docx, 'w') as output_zip:
                # Add all files from temp directory to the new zip
                for root_dir, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        arcname = os.path.relpath(file_path, temp_dir)
                        output_zip.write(file_path, arcname)

            print(f"Created modified document: {output_docx}")
        else:
            print("document.xml not found!")

    except Exception as e:
        print(f"Error: {str(e)}")

    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print("Cleaned up temporary files")


if __name__ == "__main__":
    # Run extraction and replacement
    extract_and_replace_images(
        "data/test_doc_v2.docx",
        "data/test_doc_v2_no_images.docx",
        "media"
    )