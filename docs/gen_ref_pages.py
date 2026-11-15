from pathlib import Path

import mkdocs_gen_files

# 1. Initialize the navigation generator
nav = mkdocs_gen_files.Nav()

src_dir = Path(__file__).parent.parent / "uv_lock_report"

# 3. Scan the source folder for Python files
for path in sorted(src_dir.rglob("*.py")):
    # Skip test files and test directories
    if "tests" in path.parts:
        continue


    # Get the relative parts of the module path
    module_path = path.relative_to(src_dir).with_suffix("")
    doc_path = path.relative_to(src_dir).with_suffix(".md")

    # Define where the virtual file will exist inside documentation
    full_doc_path = Path("reference", doc_path)

    parts = tuple(module_path.parts)

    # Handle init files cleanly
    if parts[-1] == "__init__":
        continue
        # parts = parts[:-1]
        # doc_path = doc_path.with_name("index.md")
        # full_doc_path = full_doc_path.with_name("index.md")
    if parts[-1] == "__main__":
        continue

    # Ignore empty edge cases
    if not parts:
        continue

    # Map the structural components to our navigation index
    nav[parts] = doc_path.as_posix()

    # 4. Open and write the virtual file on-the-fly
    with mkdocs_gen_files.open(full_doc_path, "w") as fd:
        print(full_doc_path)
        ident = ".".join(parts)
        fd.write(f"::: {ident}")  # Mkdocstrings structural syntax
        breakpoint()

    # Keep a valid "Edit this page" option targeting the raw python code
    mkdocs_gen_files.set_edit_path(
        full_doc_path, path.relative_to(src_dir.parent)
    )

# 5. Write out the dynamic literate navigation mapping file
with mkdocs_gen_files.open("reference/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
breakpoint()