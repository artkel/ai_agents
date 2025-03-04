import json
import os


def merge_json_files(file1_path, file2_path, output_path):
    """
    Merge two JSON files containing 3ds Max documentation sections

    Args:
        file1_path: Path to the first JSON file (sections 1-2)
        file2_path: Path to the second JSON file (section 3 with Q&A)
        output_path: Path to save the merged JSON file
    """
    # Load the first JSON file (sections 1-2)
    print(f"Reading first JSON file: {file1_path}")
    with open(file1_path, 'r', encoding='utf-8') as f1:
        data1 = json.load(f1)

    # Load the second JSON file (section 3)
    print(f"Reading second JSON file: {file2_path}")
    with open(file2_path, 'r', encoding='utf-8') as f2:
        data2 = json.load(f2)

    # Create a new structure for the merged data
    merged_data = {"sections": []}

    # Track sections added from each file
    sections_from_file1 = set()
    sections_from_file2 = set()

    # Process sections from the first file
    for section in data1.get("sections", []):
        section_id = section.get("id")
        sections_from_file1.add(section_id)

        # Add this section to the merged data
        if section.get("content"):
            merged_data["sections"].append(section)
            print(f"Added section {section_id} from file 1 with {len(section.get('content', []))} content items")

    # Process sections from the second file
    for section in data2.get("sections", []):
        section_id = section.get("id")
        sections_from_file2.add(section_id)

        # If this section already exists in the merged data, skip it
        if section_id in sections_from_file1:
            print(f"Section {section_id} already exists from file 1, skipping...")
            continue

        # Otherwise, add this section to the merged data
        if section.get("subcategories") and len(section.get("subcategories")) > 0:
            merged_data["sections"].append(section)
            subcat_count = len(section.get("subcategories", []))
            qa_count = sum(len(subcat.get("content", [])) for subcat in section.get("subcategories", []))
            print(f"Added section {section_id} from file 2 with {subcat_count} subcategories and {qa_count} Q&A items")

    # Sort sections by ID
    merged_data["sections"].sort(key=lambda x: x.get("id"))

    # Write the merged data to the output file
    with open(output_path, 'w', encoding='utf-8') as f_out:
        json.dump(merged_data, f_out, ensure_ascii=False, indent=2)

    print(f"\nMerging complete!")
    print(f"Sections in file 1: {', '.join(str(sid) for sid in sorted(sections_from_file1))}")
    print(f"Sections in file 2: {', '.join(str(sid) for sid in sorted(sections_from_file2))}")
    print(f"Merged JSON saved to: {output_path}")


def main():
    # File paths
    file1_path = "3ds_max_sections_1_2.json"  # First file with sections 1-2
    file2_path = "3ds_max_qa.json"  # Second file with section 3 (Q&A)
    output_path = "3ds_max_complete.json"  # Output merged file

    # Check if input files exist
    if not os.path.exists(file1_path):
        print(f"Error: File not found at {file1_path}")
        return

    if not os.path.exists(file2_path):
        print(f"Error: File not found at {file2_path}")
        return

    # Merge the files
    merge_json_files(file1_path, file2_path, output_path)


if __name__ == "__main__":
    main()