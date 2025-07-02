from url_validator import valid_url, is_reachable
from page_loader   import load_page_data
from accesibility_analyzer import check_contrast, check_typography, check_alt_text, check_heading_structure, check_link_buttons

# Get the URL
def get_url(): # User will be prompted to insert website link
    return input("🔗 Website URL: ").strip()

def check_site():
    url = get_url()
    print("You entered:", url)

    # syntax check
    if not valid_url(url):
        print("Invalid format! Must start with http:// or https://")
        return

    # reachability check
    if not is_reachable(url):
        print("Site not reachable. Check the address or your internet connection.")
        return

    print("Site is reachable!")

    # page_loader
    
    data = load_page_data(url)

    html = data["html"]
    texts = data["texts"]
    headings = data["headings"]
    images = data["images"]
    buttons = data["buttons"]

    print(f"HTML length: {len(html)}")
    print(f"Text elements: {len(texts)}")
    print(f"Headings: {len(headings)}")
    print(f"Images: {len(images)}")
    print(f"Links/Buttons: {len(buttons)}")


    # Run the contrast checker
    results = check_contrast(data["texts"])
    if not results:
        print("No contrast issues!")
    else:
        for contrast_result in results:
            label = contrast_result["tag"]
            if contrast_result["id"]:
                label += "#" + contrast_result["id"]
            elif contrast_result["classes"]:
                label += "." + contrast_result["classes"]

            # this print is still inside the for-loop
            print(
                label + " | " + contrast_result["snippet"] + " | " +
                str(contrast_result["ratio"]) + ":1 " +
                "AA=" + contrast_result["AA"] + " " +
                "AAA=" + contrast_result["AAA"]
            )
    
    # typography 
    
    typo_results = check_typography(data["texts"])
    print("Got total:", len(typo_results), "typography results")
    counts = {"Pass": 0, "Warning": 0}
    for it in typo_results:
        counts[it["WCAG"]] += 1
    print("Counts:", counts)

    print("Typography results:")

    for text_results in typo_results:
       tag = text_results.get ("tag") or "<no tag>"
       text_id = text_results.get("id")
       text_classes = text_results.get("classes")
       if text_id: 
        tag = tag + "#" + text_id
       if text_classes: 
        tag = tag + " . " + text_classes

        snippet = text_results["snippet"]
        size_px = text_results["size_px"]
        status  = text_results["WCAG"]
        print(f"{tag} | '{snippet}' | {size_px}px | WCAG={status}")
    
    # Alt check image 
    alt_results = check_alt_text(data["images"])
    print("Alt-text results:")
    for img_alt in alt_results:
        src_label = img_alt["src"].split("/")[-1]
        print(f"{src_label}: {img_alt['status']}")
    
    # Heading Checker
    heading_warnings = check_heading_structure(data["texts"])

    print("Heading structure warnings:")
    if not heading_warnings:
        print("All headings are in good order!")
    else:
        for warning in heading_warnings:
            print(" • " + warning)
    
    # Button checker
    btn_failures = check_link_buttons(data["buttons"])
    print("Missing link/button labels:")
    if not btn_failures:
        print("All buttons have text or aria-labels")
    else:
        for fail in btn_failures:
            print(f"{fail['label']}: {fail['status']}")

if __name__ == "__main__":
    check_site()

