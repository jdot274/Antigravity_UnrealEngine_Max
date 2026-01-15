import os
import re

def audit_ui_linkage(file_path):
    print(f"🔍 Auditing UI Linkage: {os.path.basename(file_path)}")
    with open(file_path, 'r') as f:
        content = f.read()

    # Find all interactive-looking elements (buttons, drop-rows, menu-items)
    # We look for onclick or uiCommand calls
    interactive_elements = re.findall(r'<(button|div|span)[^>]+class=["\'][^"\']*(btn|item|row)[^"\']*["\'][^>]*>', content)
    
    total_found = len(interactive_elements)
    linked_count = 0
    failures = []

    # Regex for onclick or any linked action
    # We specifically look for onclick="...uiCommand..." or unique functions
    tags = re.finditer(r'<(button|div|span)([^>]+)>', content)
    
    for match in tags:
        tag_type = match.group(1)
        attrs = match.group(2)
        
        # Filter for only UI elements we care about
        if 'btn' in attrs or 'item' in attrs or 'row' in attrs or 'onclick' in attrs:
            if 'onclick' in attrs:
                linked_count += 1
            else:
                # Potential failure
                label_match = re.search(r'>(.*?)<', content[match.end():match.end()+100])
                label = label_match.group(1).strip() if label_match else "Unknown Label"
                failures.append(f"MISSING LINK: <{tag_type}> {label}")

    success_rate = (linked_count / total_found * 100) if total_found > 0 else 100
    print(f"✅ Audit Complete: {linked_count}/{total_found} elements linked ({success_rate:.1f}%)")
    
    if failures:
        print("❌ FAILURES DETECTED:")
        for f in failures:
            print(f"  - {f}")
    
    return success_rate, failures

if __name__ == "__main__":
    controller_path = "shader_overlay/engine_controller.html"
    editor_path = "shader_overlay/editor_ui.html"
    
    c_score, c_fails = audit_ui_linkage(controller_path)
    e_score, e_fails = audit_ui_linkage(editor_path)
    
    total_score = (c_score + e_score) / 2
    print(f"\n🏆 FINAL UI SCORE: {total_score:.1f}%")
    
    if total_score < 100:
        exit(1)
    else:
        exit(0)
